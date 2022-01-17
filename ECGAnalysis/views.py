# from .forms import LoginForm
import os

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from ECGAnalysis.models import RecordingFile
from ProjetFinal import settings
from .models import OverwriteStorage
from .static.py import help_functions as funcs
from .static.py import main_classification_fct as classification_fct

# Create your views here.

current_directory = os.getcwd()

# global variable for username
username = ''


def base(request):
    return render(request, 'ECGAnalysis/base.html')


# This will be the first page you see when you logged in.
# You can upload a ECG image from here and the program will analyze it.###


def greeting(request):
    print(current_directory)

    args = []
    for file in RecordingFile.objects.all():
        args.append(file.title)

    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        ECGFile = request.FILES['ECGFile']
        fs = OverwriteStorage()
        args, url = funcs.PatientData(
            settings.BASE_DIR + fs.url(ECGFile), 0, 50000, False)
        dictList = []
        for key, value in args.items():
            temp = [key, value]
            dictList.append(temp)
        check_files = RecordingFile.objects.filter(
            ecgfile=settings.BASE_DIR + fs.url(ECGFile))

        if len(check_files) == 0:  # no such ECG file in the DB
            print('vide')
            recording_file = RecordingFile(
                title=ECGFile.name, ecgfile=settings.BASE_DIR + fs.url(ECGFile),
                url=url, doctor=username, patient=args['FirstName'])
            recording_file.save()
            print(recording_file.url)
        else:
            recording_file = RecordingFile.objects.get(
                ecgfile=settings.BASE_DIR + fs.url(ECGFile))
            recording_file.url = url
            recording_file.save()
            print(' y en a ')

        innerGraph = funcs.uxplot(url)
        context = {'f': dictList, 'graph': innerGraph}
        response = render(request, 'ECGAnalysis/leads_interface.html', context)
        response.set_cookie('file', url)
        return response
    return render(request, 'ECGAnalysis/greeting.html')


# If i choose a file already in the DB, i get the file,
# get the patient's data ( no need to parse in a CSV file) and go to the
# the page with the 12 leads
def GoToMainPage(request, file):
    print(file)
    recording_file = RecordingFile.objects.filter(title=file)
    recording_file = recording_file[0]

    # already in the DB, we send True for DB param
    args, url = funcs.PatientData(recording_file.ecgfile, 0, 50000, True)
    dictlist = []
    for key, value in args.items():
        temp = [key, value]
        dictlist.append(temp)

    print('url', url)
    print('recording ', recording_file.url)
    mainGraph = funcs.uxplot(recording_file.url)
    context = {'f': dictlist, 'graph': mainGraph}
    response = render(request, 'ECGAnalysis/leads_interface.html', context)
    response.set_cookie('file', recording_file.url)
    return response


# Function that returns the analyse of the waves of  a selected lead (clusters )
# Provides from an AJAX request
@csrf_exempt
def analyze(request):
    url = request.COOKIES['file']
    lead_id = request.POST.get('lead_id', None)
    print(lead_id)
    print(url)
    clusters = classification_fct.ux(
        url, int(lead_id), 0, 20000)  # at 20000 for now
    print('Fin')
    data = {'clusters': clusters}
    print('la')
    print(data['clusters'][1][1])
    return JsonResponse(data)


# Function that gets the necessary data of the lead we decided to add to our page (graph,pulses,number of the lead)
# Provides from an AJAX request


def add_graph(request):
    url = request.COOKIES['file']
    lead_id = request.GET.get('lead_id', None)
    print('lead id', lead_id) \
        # get the clean samples and the clean matrix
    data, data_np, mat, removedNoisesMatrix, pulses = classification_fct.get_clean_sample(
        url, int(lead_id), 0, 20000)
    # get an array for debug option
    dataset_debug = funcs.dataset_debug_mode(
        data_np, len(data_np), pulses)
    context = {'lead_id': lead_id, 'data': data,
               'debug': dataset_debug, 'pulses': pulses}
    return JsonResponse(context)


# Function that gets the necessary data of the lead we choose(graph,pulses,number of the lead)
def graph(request, lead_id):
    url = request.COOKIES['file']
    # get the clean samples and the clean matrix
    data, data_np, mat, removedNoisesMatrix, pulses = classification_fct.get_clean_sample(
        url, lead_id, 0, 20000)

    # get an array for debug option
    dataset_debug = funcs.dataset_debug_mode(
        data_np, len(data_np), pulses)
    leads = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    # get the list of the leads without ours
    my_lead = list(filter(lambda x: x != lead_id, leads))
    context = {'data': data, 'debug': dataset_debug,
               'pulses': pulses, 'leads': my_lead, 'current_lead': lead_id}
    response = render(request, 'ECGAnalysis/visualisation_graph.html', context)
    response.set_cookie('lead_id', lead_id)
    response.set_cookie('file', url)
    return response
