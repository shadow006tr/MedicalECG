import csv
import io
import math
import struct
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import os

matplotlib.use('Agg')


# Create a dictionary to collect all the information of the patient stored in the ECG file
def PatientData(inEcgFile, startLine, stopLine, inDb):
    with open(inEcgFile, "rb") as f:
        args = {}
        magicNumber = f.read(8)
        args['MagicNumber'] = magicNumber.decode('utf-8', errors='ignore')
        checksum = struct.unpack('h', f.read(2))[0]
        args['Checksum'] = checksum
        Var_length_block_size = struct.unpack('i', f.read(4))[0]
        args['Var length block size'] = Var_length_block_size
        Sample_Size_ECG = struct.unpack('i', f.read(4))[0]
        args['Sample Size ECG'] = Sample_Size_ECG
        Offset_var_length_block = struct.unpack('i', f.read(4))[0]
        args['Offset var lenght block'] = Offset_var_length_block
        Offset_ECG_block = struct.unpack('i', f.read(4))[0]
        args['Offset ECG block'] = Offset_ECG_block
        File_Version = struct.unpack('h', f.read(2))[0]
        args['File Version '] = File_Version
        First_Name = f.read(40)
        args['FirstName'] = clear_name(First_Name.decode('utf-8', errors='ignore'))
        Last_Name = f.read(40)
        args['LastName'] = clear_name(Last_Name.decode('utf-8', errors='ignore'))
        ID = f.read(20)
        args['ID'] = clear_name(ID.decode('utf-8', errors='ignore'))
        Sex = struct.unpack('h', f.read(2))[0]
        args['Sex'] = translate_sex(Sex)
        Race = struct.unpack('h', f.read(2))[0]
        args['Race'] = Race
        Birth_Date = []
        for idx in range(0, 3):
            Birth_Date.append(struct.unpack('H', f.read(2))[0])
        args['BirthDate'] = translate_date(Birth_Date)
        Record_Date = []
        for idx in range(0, 3):
            Record_Date.append(struct.unpack('H', f.read(2))[0])
        args['Record_Date '] = translate_date(Record_Date)
        File_Date = []
        for idx in range(0, 3):
            File_Date.append(struct.unpack('H', f.read(2))[0])
        args['File_Date '] = translate_date(File_Date)
        Start_Time = []
        for idx in range(0, 3):
            Start_Time.append(struct.unpack('H', f.read(2))[0])
        args['Start_Time '] = translate_hour(Start_Time)
        nLeads = struct.unpack('h', f.read(2))[0]
        args['nLeads'] = nLeads
        Lead_Spec = []
        for idx in range(0, 12):
            Lead_Spec.append(struct.unpack('H', f.read(2))[0])
        args['Lead_Spec '] = Lead_Spec
        Lead_Qual = []
        for idx in range(0, 12):
            Lead_Qual.append(struct.unpack('H', f.read(2))[0])
        args['Lead_Qual'] = Lead_Qual
        Resolution = []
        for idx in range(0, 12):
            Resolution.append(struct.unpack('h', f.read(2))[0])
        args['Resolution'] = Resolution
        Pacemaker = struct.unpack('H', f.read(2))[0]
        args['Pacemaker'] = Pacemaker
        Recorder = f.read(40)
        args['Recorder'] = clear_name(Recorder.decode('utf-8', errors='ignore'))
        Sampling_Rate = struct.unpack('H', f.read(2))[0]
        args['Sampling_Rate'] = Sampling_Rate
        Proprietary = f.read(80)
        args['Proprietary '] = clear_name(Proprietary.decode('utf-8', errors='ignore'))
        Copyright = f.read(80)
        args['Copyright '] = clear_name(Copyright.decode('utf-8', errors='ignore'))
        Reserved = f.read(88)
        args['Reserved '] = clear_name(Reserved.decode('utf-8', errors='ignore'))
        print(inEcgFile)
        outFile = inEcgFile.replace('ecg', 'csv')
        if inDb:  # if in the DB no need to parse
            pass
        else:
            with open(outFile,
                      'w') as exportFile:  # if the file is already created no need to
                # make the parsing step of the ECG data
                if os.stat(outFile).st_size > 0:
                    pass
                else:
                    print('Lead_Spec =', Lead_Spec)
                    if stopLine == 1:
                        readNLines = int(Sample_Size_ECG)
                    else:
                        readNLines = int(stopLine)
                    print('number of lines: ', readNLines)
                    print(' Working on Lines {}-{}'.format(startLine, readNLines))
                    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                    voltageFile = open("voltage.txt", 'a')
                    voltageFile.write('Resolution[0]: ' + Resolution[0].__str__() + '\n')
                    voltageFile.write('Sampling_Rate: ' + Sampling_Rate.__str__() + '\n')
                    lowVoltage = -20000000 / int(Resolution[0])
                    hiVoltage = 20000000 / int(Resolution[0])
                    voltageNormlize = 65535 / (hiVoltage - lowVoltage)
                    voltageFile.write('lowVoltage: ' + lowVoltage.__str__() + '\n')
                    voltageFile.write('hiVoltage: ' + hiVoltage.__str__() + '\n')
                    voltageFile.write('voltageNormlize: ' + voltageNormlize.__str__() + '\n')
                    voltageFile.close()
                    # print('Normalize Factor =', lowVoltage, hiVoltage, voltageNormlize)
                    print("\nCreating the CSV file...")
                    # bar = progressbar.ProgressBar(maxval=readNlines,
                    #                               widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
                    # bar.start()
                    check = [[] for _ in range(12)]
                    for i in range(0, readNLines):
                        # bar.update(i + 1)
                        orderedLeads = [None] * 12
                        data = []
                        for index, readOrdered in enumerate(Lead_Spec):
                            nextRead = (struct.unpack('h', f.read(2))[0])

                            if len(check[index - 5]) == 0 or nextRead not in check[index - 5]:
                                check[index - 5].append(nextRead)
                            if i < 200:
                                print(check)
                            if len(check[index - 5]) >= 20:
                                orderedLeads[readOrdered - 5] = nextRead
                                data.append(nextRead)

                        if i > int(startLine) and (orderedLeads.__contains__(None)) is False:
                            exportFile.writelines((str(orderedLeads)[1:-1]) + '\n')

        return args, outFile


def clear_name(name):
    return name.split('\x00', 1)[0]


def translate_sex(sex):
    if sex == 2:
        return "M"
    else:
        return "W"


def translate_date(date):
    return str(date[0]) + '/' + str(date[1]) + '/' + str(date[2])


def translate_hour(hour):
    return str(hour[0]) + ' : ' + str(hour[1]) + ' : ' + str(hour[2])


# little function to get little graphs for the 12  leads
def uxplot(csvFile):
    lFile = csvFile
    selectedValues = []
    for j in range(0, 12):
        selectedValues.append([])
    while lFile == csvFile:
        i = 0
        try:
            with open(lFile, newline='\n') as csvFile:
                rows = csv.reader(csvFile, delimiter=',', quotechar='|')
                counter = 0
                for row in rows:
                    counter += 1
                    if counter < 2000:
                        for j in range(0, 12):
                            selectedValues[j].append(int(row[j]))
            graphic = []
            for j in range(0, 12):
                print(j)
                arr = np.array(selectedValues[j])
                samplesSize = len(arr)
                print('Number of samples of column  ' + str(j) + ' :', samplesSize)
                graphic.append(graphCreator(arr))
            return graphic
        except:
            lFile = ""
            print("\nWrong path")


def plotValues(values, column):
    plt.plot(np.array(range(1100)), values[100:1200], 'k')
    plt.savefig("Graphs/graph#_" + str(column) + ".png", dpi=300, bbox_inches='tight')
    plt.show()


# Function to create a simple image of a graph for each lead(before the selection)
def graphCreator(values):
    fig = plt.figure()
    plt.plot(np.array(range(1100)), values[100:1200], 'k')
    imgdata = io.StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()

    return data


# target: to calculate the distance from point (x1, y1) to the line with a,b,c as its coefficients
def calc_distance(x1, y1, a, b, c):
    d = abs((a * x1 + b * y1 + c) / (math.sqrt(a * a + b * b)))
    return d


# wave split
def waveSplit(mat1, xx, yy, vectorLen, subsetA):
    x = int(mat1[xx][0])
    print("help_function :: x: ", x)
    y = int(mat1[yy][0] + 1)
    print("help_function :: y: ", y)

    scale = list(range(0, vectorLen))
    plotRange(scale, subsetA, x, y)
    plt.stem(mat1[xx:(yy + 1), 0], mat1[xx:(yy + 1), 2]
             * 10, linefmt='g-', markerfmt='ro')
    plt.stem(mat1[xx:(yy + 1), 0], mat1[xx:(yy + 1), 1],
             linefmt='y-', markerfmt='bo')
    plt.show()


def plotRange(A, B, x, y):
    plt.plot(A[x:y], B[x:y])


# Function that creates an array that allows us to delimit waves in a graph
def dataset_debug_mode(samples, sample_size, pulse):
    dataset = []
    a = np.array(pulse)
    percentile = np.percentile(samples, 97)
    percentile2 = np.percentile(samples, 92)
    # print('pulses_add',a)
    for i in range(sample_size):
        if i in a:
            if percentile > 1000 and (percentile - percentile2) > 500:
                dataset.append(3300)
            else:
                dataset.append((-2700))
        else:
            dataset.append(0)

    return dataset
