import csv

import numpy as np

from QRSDetectorOffline import QRSDetectorOffline

from .detection_fct import getPDX_for_negative
from .detection_fct import getPDX_for_positive
from .first_classification import detectCluster6d
from .first_kmeans import kMeansFilter6d
from .second_classification import secondKmeans


# from the csv file , create an array that contains the data of the selected lead
def get_selected_lead_samples(csv_file, lead_number):
    selectedLeadSamples = []
    lFile = ""
    while lFile == "":
        lFile = csv_file
        i = 0
        column = lead_number - 1

        try:
            with open(lFile, newline='\n') as csvFile:
                rows = csv.reader(csvFile, delimiter=',', quotechar='|')
                for row in rows:
                    i += 1
                    if column > 12 or column < 0:
                        print("number of leads not allowed")
                        break
                    # for now, we put a limit of 20000 but must be enlarged
                    if i < 20000:
                        selectedLeadSamples.append(int(row[column]))
                        continue
                    break
        except lFile.DoesNotExist:
            lFile = ""
            print("\nWrong path")

    return selectedLeadSamples


# get the samples and begin the analysis with the delimitation of the waves , the creation of the matrix and
# the first K_Means to take off the noises pulses and noises matrix
def get_clean_sample(csv_file, leads_number, start_index, end_index):
    # get samples from the CSV file according to the lead number/column
    selected_lead_samples = get_selected_lead_samples(csv_file, leads_number)
    selected_lead_samples_np = np.array(selected_lead_samples)
    selected_lead_samples_np_new = np.array(selected_lead_samples_np)

    minvec = min(selected_lead_samples_np)
    maxvec = max(selected_lead_samples_np)
    diff = maxvec - minvec

    for i in range (len(selected_lead_samples_np)):
        selected_lead_samples_np_new[i] = (selected_lead_samples_np[i] - minvec - diff / 8.0) * 5.0 / (diff * 10.0 / 8.0)

    f = open('leads_new.txt', 'a')
    selected_lead_samples_np_new.tofile(f, '\n', '%s')
    f.close()

    # call the function to get the matrix
    mat = getPDX(leads_number, selected_lead_samples_np[start_index:end_index], 0, end_index - start_index)
    a = np.copy(mat)
    # First K-means for removing the noises
    removedNoisesMatrix, removedNoisesPulses = kMeansFilter6d(mat, 0, len(a) - 1,
                                                              selected_lead_samples_np[start_index:end_index])
    return selected_lead_samples, selected_lead_samples_np, mat, removedNoisesMatrix, removedNoisesPulses


# main function for the analysis of the data
def ux(csv_file, leads_number, start_index, end_index):
    # get the samples and the pulses and the matrix without the noises
    selected_lead_samples, selectedLeadSamples, mat, removedNoisesMatrix, removedNoisesPulses = get_clean_sample(
        csv_file, leads_number, start_index, end_index)

    # call the function for first classification
    biggestClusterCentroids, labelsOfKMeans = detectCluster6d(removedNoisesMatrix)
    print('marrreeeeeeeee')
    # call the function for 2nd classification
    clusters = secondKmeans(removedNoisesMatrix, biggestClusterCentroids, labelsOfKMeans, removedNoisesPulses)

    # to get graph with the delegates
    # for each graph , creation of an array that contains the values around the delegates to draw a little graph
    for i in range(len(clusters)):
        print('delegate')
        print(clusters[i][4])
        delegate = clusters[i][4]
        delegate_list = selected_lead_samples[int(delegate) - 150: int(delegate) + 150]
        print('delegateList')
        clusters[i] = clusters[i] + (delegate_list,)

    print('\nEnd of analysis.')
    return clusters


# Function  to choose the right delimitation function for each lead
# We choose in function of the 97th percentile and the 92nd percentile
def getPDX(leads_number, samples, starting, vend):
    peaks = QRSDetectorOffline("fix").qrs_peaks_indices

    mean = np.mean(samples)

    print('Median' + str(mean) + '  for lead' + str(leads_number))
    std = np.std(samples)
    print('std ' + str(std) + '  for lead' + str(leads_number))
    percentile1 = np.percentile(samples, 97)
    percentile2 = np.percentile(samples, 92)

    # check the difference between percentiles 97 and 92
    print('percentile1 ' + str(percentile1) + ' for lead' + str(leads_number))
    print('percentile2 ' + str(percentile2) + ' for lead' + str(leads_number))

    # print('percentile2 ' + str(percentile2) + ' ' + str(leads_number))

    if percentile1 > 1000 and (percentile1 - percentile2) > 500:
        return getPDX_for_positive(samples, starting, vend, peaks)
    else:
        return getPDX_for_negative(samples, starting, vend, peaks)
