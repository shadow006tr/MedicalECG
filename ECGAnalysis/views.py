from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from ProjetFinal import settings

from django.utils  import  timezone
from ECGAnalysis.models import Doctor,RecordingFile
from .static.py import help_functions as funcs
from .static.py import main_classification_fct as classification_fct
from django.contrib.auth.forms import   UserCreationForm,AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.staticfiles.storage import staticfiles_storage
import json

# from .forms import LoginForm
import os

# Create your views here.

current_directory= os.getcwd()


# global variable for username
username = ''


#Returns the welcome page with the Authentication
#Contains also the POST metod to got to the home page if it is valid, else stay on the welcome page
def welcome(request):
    if (request.method == 'POST'):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user= form.get_user()
            # store the username in a global variable
            username = request.POST.get('username')
            login(request,user)
            print(current_directory)
            args = []
            for file in RecordingFile.objects.all():
                args.append(file.title)
            context = {'files': args}
            return render(request, 'HTML/home.html', context)

    form = AuthenticationForm()
    print(Doctor.objects.filter(name="Raph"))
    return render(request, 'HTML/welcome.html', {'form': form})


#Returns the page for sign up
#Post method to signup, if it is valid go the the home page, else stay on the sign up page
def signup(request):
    if (request.method == 'POST'):
        form = UserCreationForm(request.POST)
        print(request.POST.get('username'))
        print(request.POST.get('password1'))
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password1')
            doctor = Doctor(name=username,email=username+"@gmail.com",password=password)
            doctor.save()
            user=form.save()
            print(user)
            login(request,user)
            print(username)
            args = []
            for file in RecordingFile.objects.all():
                args.append(file.title)
            context = {'files': args}
            return render(request, 'HTML/home.html', context)
        else :
            print('problem')
            error = "The parameters you entered are not valid"
            return render(request, 'HTML/signUp.html', {'form': form, 'error': error})


    form = UserCreationForm
    error = ""
    return render(request, 'HTML/signUp.html', {'form': form, 'error': error})

def signOut(request):
    logout(request)
    form = AuthenticationForm()
    return render(request, 'HTML/welcome.html', {'form': form})


# Returns our home page with the selection of the ECG file
# Displays the ECG files from the Database
def home(request):
    print(current_directory)

    args = []
    for file in RecordingFile.objects.all():
        args.append(file.title)
    context = { 'files' :  args}

    return render(request, 'HTML/home.html',context)

# Function that parse an new  ECG file in a CSV file and returns the data of the patient
# with the page of our 12 leads in order to observe them
# Save the file in the DB, if already there , change its params if necessary
def Parser(request):
    counter = 0
    inp = request.POST.get('file')
    var =''
    print('input')

    # the file must be in the current directory if we want to get its past faster
    for r,d, f in os.walk(current_directory):  # change the hard drive, if you want
        for file in f:
            filepath = os.path.join(r, file)
            if file.endswith(inp):
                counter +=1
                var =os.path.join(r, file)
                print(os.path.join(r, file))
    print(counter)
    # at 50000 now but can be enlarged, we consider that every new file is not in the DB so  we send False for inDb param
    args,url =funcs.Patientdata(var,0,50000,False)

    dictlist =[]
    for key, value in args.items():
        temp = [key, value]
        dictlist.append(temp)
        temp= [key, str(value)]
    check_files = RecordingFile.objects.filter(ecgfile = var)


    if( len(check_files) == 0 ):  # no such ECG file in the DB
        print('vide')
        recording_file = RecordingFile(title=inp,ecgfile=var, url=url,doctor=username,patient=args['FirstName'])
        recording_file.save()
        print(recording_file.url)
    else :
        recording_file = RecordingFile.objects.get(ecgfile = var)
        recording_file.url = url
        recording_file.save()
        print(' y en a ')


    graph = funcs.uxplot(url)
    context = {'f': dictlist, 'graphique': graph }
    response = render(request, 'HTML/leads_interface.html', context)
    response.set_cookie('file', url)
    return response


# If i choose a file already in the DB, i get the file, get the patient's data ( no need to parse in a CSV file) and go to the
#the page with the 12 leads
def GoToMainPage(request, file):

    print(file)
    recording_file = RecordingFile.objects.filter(title=file)
    recording_file = recording_file[0]

    # already in the DB, we send True for DB param
    args, url = funcs.Patientdata(recording_file.ecgfile,0,50000,True)
    dictlist = []
    for key, value in args.items():
        temp = [key, value]
        dictlist.append(temp)

    print('url',url)
    print('recordingurl ',recording_file.url)
    # url = recording_file.ecgfile.re
    graph = funcs.uxplot(recording_file.url)
    context = {'f': dictlist, 'graphique': graph}
    response = render(request, 'HTML/leads_interface.html', context)
    response.set_cookie('file', recording_file.url)
    return response




# Function that returns the analyse of the waves of  a selected lead (clusters )
#Provides from an AJAX request
@csrf_exempt
def analyze(request):
    url = request.COOKIES['file']
    lead_id = request.POST.get('lead_id', None)
    print(lead_id)
    print(url)
    clusters = classification_fct.ux(url, int(lead_id), 0, 20000) # at 20000 for now
    print('Fin')
    data = {}
    data['clusters'] = clusters
    print('la')
    print(data['clusters'][1][1])
    return JsonResponse(data)

# Function that gets the necessary data of the lead we decided to add to our page (graph,pulses,number of the lead)
#Provides from an AJAX request
def add_graph(request):
    url = request.COOKIES['file']
    lead_id = request.GET.get('lead_id', None)
    print('lead id', lead_id) \
     # get the clean samples and the clean matrix
    data, data_np, mat, removedNoisesMatrix, pulses = classification_fct.get_clean_sample(url, int(lead_id), 0, 20000)
    # get an array for debug option
    dataset_debug = funcs.dataset_debug_mode(data_np,len(data_np), pulses,int(lead_id))
    context = {'lead_id': lead_id, 'data': data, 'debug': dataset_debug, 'pulses': pulses}
    return JsonResponse(context)




#Function that gets the necessary data of the lead we choose(graph,pulses,number of the lead)
def graph(request, lead_id):
    url = request.COOKIES['file']
    # get the clean samples and the clean matrix
    data, data_np, mat, removedNoisesMatrix, pulses = classification_fct.get_clean_sample(url, lead_id, 0, 20000)

    # get an array for debug option
    dataset_debug = funcs.dataset_debug_mode(data_np,len(data_np), pulses,lead_id)
    leads = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # get the list of the leads without ours
    my_lead = list(filter(lambda x: x != lead_id, leads))
    context = {'data': data, 'debug': dataset_debug, 'pulses': pulses, 'leads': my_lead , 'current_lead': lead_id}
    response = render(request, 'HTML/visualisation_graph.html', context)
    response.set_cookie('lead_id', lead_id)
    response.set_cookie('file', url)
    return response

