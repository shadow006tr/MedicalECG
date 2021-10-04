
import csv
import math
import warnings
import matplotlib.pyplot as plt
import numpy as np
import scipy
import seaborn as sns
from matplotlib import rcParams
from scipy.spatial import KDTree
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree



# The function that receives all the data and must delimit the different waves and give them the necessary properties for analysis
#Here is for the waves that the majority of the waves are "up" or "positive" waves
def getPDX_for_positive(samples, strtin, vend):


    subsetA = samples
    veclen = len(subsetA)

    if vend == -1:
        ends = veclen - 1
    else:
        ends = vend

    strt_ana = -1
    if strtin == -1:
        for i in range(0, ends - 5):
            if subsetA[i] != subsetA[i + 1] and subsetA[i + 1] != subsetA[i + 2] and subsetA[i + 2] != subsetA[
                i + 3] and subsetA[i + 4] != subsetA[i + 5] and subsetA[i + 5] != subsetA[i + 6]:
                strt_ana = i
                break
    else:
        strt_ana = strtin

    if strt_ana == -1:
        print("\nWaves not found")
        quit()
    strt = strt_ana + 41
    ends = ends - 41
    dx = np.diff(subsetA)
    adx = np.absolute(dx)

    pdx2 = np.maximum(0, dx)  # focus on the positive differences



    pdx1 = np.copy(pdx2)
    sum = 0
    count = 0

    # Idea for new classifiaction

    for i in range(strt,ends):
        if(pdx2[i] > 0):
            pdx1[i]=0
            count+=1
            sum+= pdx2[i]
        if(pdx2[i]== 0) :
            if(sum<800):# we don't analyze the small waves
                pdx1[i] = 0
                sum = 0
                count = 0
            else:
                if( subsetA[i] - subsetA[i+3] > 150 and subsetA[i] > 0 ):
                    pdx1[i] = sum
                    sum=0
                    count=0
                else :
                    continue
        else:
            continue

    vdx = np.copy(pdx2)

    for i in range(strt, ends + 1):
        vdx[i] = np.sum(pdx2[(i - 30):(i + 31)]) / 61.0



    vdx2 = np.copy(vdx)
    for i in range(strt, ends + 1):
        if (pdx1[i] > 1000 and pdx1[i] > 7 * vdx[i]) or (pdx1[i] > 15 * vdx[i] and pdx1[i] > 600) or (
                pdx1[i] > 400 and pdx1[i] * pdx1[i] / vdx[i] > 13500):
            vdx2[i] = pdx1[i]
        else:
            vdx2[i] = 0

    for i in range(0, strt):
        vdx2[i] = 0

    vdx3 = np.copy(vdx2)
    #
    # for i in range(strt, ends + 1):
    #     if (vdx3[i] != 0):
    #         if (subsetA[i] < 300):
    #             vdx3[i] = 0

    mat = np.zeros((veclen, 11))

    k = 0  # iw will be the number of waves
    for j in range(strt, ends + 1):
        # sleep(0.1)
        if vdx3[j] > 0:
            mat[k][0] = j  # first index of the wave
            mat[k][1] = vdx3[j]  # power of the waves
            mat[k][2] = subsetA[j]  # value at the beggining of the wave
            if k > 0:
                index_0= 1
                if(k>1):
                    index_0 = points_before0_for_positive(subsetA, int(mat[k - 1][0]))
                # print('index0' ,index_0)


                mat[k][3] = mat[k][0] - mat[k - 1][0]  # size of the wave ( number of points)
                mat[k][4] = '%.1f' % np.amin(
                    subsetA[int(mat[k - 1][0] + 1):int(mat[k][0] + 1)])  # minimum value in the wave
                if( index_0 <  mat[k][3]- 10 ):
                    mat[k][5] = '%.1f' % np.amax(
                        subsetA[int(mat[k - 1][0] + index_0):int(mat[k][0] + 1)])  # max value in the wave
                else:
                    mat[k][5] = '%.1f' % np.amax(
                        subsetA[int(mat[k - 1][0] + 2):int(mat[k][0] + 1)])  # max value in the wave

                mat[k][6] = '%.1f' % sumOfSlopes(
                    dx, int(mat[k - 1][0]), int(mat[k][0]))  # number of Slopes in a wave
                mat[k][7] = '%.1f' % (2000 * percentOfOutOfBoundSamples(
                    subsetA, int(mat[k - 1][0]), int(mat[k][0]), 1500))
                mat[k][8] = '%.1f' % np.median(
                    subsetA[int(mat[k - 1][0] + 1): int(mat[k][0] + 1)])  # median of the wave
                mat[k][9] = '%.1f' % np.std(subsetA[int(mat[k - 1][0] + 1): int(mat[k][0] + 1)])  # std of the wave
                arr_median = array_median(subsetA[int(mat[k - 1][0] + 1): int(mat[k][0] + 1)], mat[k][8])

                mat[k][10] = '%.1f' % integrate(arr_median, 1)  # area of the wave
            k = k + 1

    return mat[0:k]


#Here is for the "down" or "negative" waves
def getPDX_for_negative(samples, strtin, vend):
    subsetA = samples
    veclen = len(subsetA)

    if vend == -1:
        ends = veclen - 1
    else:
        ends = vend

    strt_ana = -1
    if strtin == -1:
        for i in range(0, ends - 5):
            if subsetA[i] != subsetA[i + 1] and subsetA[i + 1] != subsetA[i + 2] and subsetA[i + 2] != subsetA[
                i + 3] and subsetA[i + 4] != subsetA[i + 5] and subsetA[i + 5] != subsetA[i + 6]:
                strt_ana = i
                break
    else:
        strt_ana = strtin

    if strt_ana == -1:
        print("\nWaves not found")
        quit()
    strt = strt_ana + 41
    ends = ends - 41
    dx = np.diff(subsetA)
    adx = np.absolute(dx)


    pdx2 = np.maximum(0, np.negative(dx)) # focus on the negative differences

    pdx1 = np.copy(pdx2)
    sum = 0
    for i in range(strt, ends):
        if (pdx2[i] > 0):
            pdx1[i] = 0
            sum += pdx2[i]
        if (pdx2[i] == 0):
            if (sum < 900):  # we don't analyze the small waves
                pdx1[i] = 0
                sum = 0
            else:
                if (subsetA[i + 3] - subsetA[i] > 150):  # to be sure that we did not arrive to a little descent in a big climb
                    pdx1[i] = sum # store the sum at the peak of the climb
                    sum = 0
                else:
                    continue
        else:
            continue



    vdx = np.copy(pdx2)

    for i in range(strt, ends + 1):
        vdx[i] = np.sum(pdx2[(i - 30):(i + 31)]) / 61.0





    vdx2 = np.copy(vdx)
    for i in range(strt, ends + 1):
        if (pdx1[i] > 1000 and pdx1[i] > 7 * vdx[i]) or (pdx1[i] > 15 * vdx[i] and pdx1[i] > 600) or (
                pdx1[i] > 400 and pdx1[i] * pdx1[i] / vdx[i] > 13500):
            vdx2[i] = pdx1[i]
        else:
            vdx2[i] = 0

    for i in range(0, strt):
        vdx2[i] = 0

    vdx3 = np.copy(vdx2)
    for i in range(strt, ends + 1):
        if (vdx3[i] != 0):
            if (subsetA[i] > - 400):
                vdx3[i] = 0


    mat = np.zeros((veclen, 11))

    k = 0  # iw will be the number of waves
    for j in range(strt, ends + 1):
        # sleep(0.1)
        if vdx3[j] > 0:
            mat[k][0] = j  # first index of the wave
            mat[k][1] = vdx3[j]  # power of the waves
            mat[k][2] = subsetA[j]  # value at the beginning of the wave
            if k > 0:
                index_0= 1
                if(k>1):
                    index_0 = points_before0_for_negative(subsetA, int(mat[k - 1][0]))
                # print('index0' ,index_0)
                mat[k][3] = mat[k][0] - mat[k - 1][0]  # size of the wave ( number of points)

                mat[k][5] = '%.1f' % np.amax(
                    subsetA[int(mat[k - 1][0] + 1):int(mat[k][0] + 1)])  # max value in the wave

                if( index_0 <  mat[k][3] -10 ):
                    mat[k][4] = '%.1f' % np.amin(
                        subsetA[int(mat[k - 1][0] + index_0):int(mat[k][0] + 1)])  # minimum value in the wave
                else :
                    mat[k][4] = '%.1f' % np.amin(
                        subsetA[int(mat[k - 1][0] + 2):int(mat[k][0] + 1)])  # minimum value in the wave

                mat[k][6] = '%.1f' % sumOfSlopes(
                    dx, int(mat[k - 1][0]), int(mat[k][0]))  # number of Slopes in a wave
                mat[k][7] = '%.1f' % (2000 * percentOfOutOfBoundSamples(
                    subsetA, int(mat[k - 1][0]), int(mat[k][0]), 1500))
                mat[k][8] = '%.1f' % np.median(
                    subsetA[int(mat[k - 1][0] + 1): int(mat[k][0] + 1)])  # median of the wave
                mat[k][9] = '%.1f' % np.std(subsetA[int(mat[k - 1][0] + 1): int(mat[k][0] + 1)])  # std of the wave
                arr_median = array_median(subsetA[int(mat[k - 1][0] + 1): int(mat[k][0] + 1)], mat[k][8])
                mat[k][10] = '%.1f' % integrate(arr_median, 1)  # area of the wave
            k = k + 1

    return mat[0:k]


#  ------- functions that help for the construction of matrix  --------

def sumOfPositiveSlopes(setA, startI, endI):
    counter = 0
    for i in range(startI, endI + 1):
        if setA[i] <= 0 and setA[i - 1] > 0:
            counter = counter + 1
    if setA[endI] > 0 and setA[i - 1] < 0:
        counter = counter + 1
    return counter



# Function for sumOfSlopes
def sumOfSlopes(setA, startI, endI):
    return sumOfPositiveSlopes(setA, startI, endI) + sumOfNegativeSlopes(setA, startI, endI)


def sumOfNegativeSlopes(setA, startI, endI):
    counter = 0
    for i in range(startI, endI + 1):
        if setA[i] >= 0 and setA[i - 1] < 0:
            counter = counter + 1
    if setA[endI] < 0 and setA[i - 1] > 0:
        counter = counter + 1
    return counter


def percentOfOutOfBoundSamples(setA, startI, endI, bound):
    counter = 0
    for i in range(startI, endI + 1):
        if setA[i] >= math.fabs(bound):
            counter = counter + 1
    rangeLength = endI + 1 - startI
    return 100 * counter / rangeLength


def array_median(values, median):
    return (np.array(values) - median)


# Function to calculate area with Simpson Method
def integrate(y_vals, h):
    i = 1
    total = y_vals[0] + y_vals[-1]
    for y in y_vals[1:-1]:
        if i % 2 == 0:
            total += 2 * y
        else:
            total += 4 * y
        i += 1
    return total * (h / 3.0)


#Function to manage the calculation of the right maximum
def points_before0_for_positive(samples,index):
    count = 0
    while(samples[index] > 0 and count< 20):
        index +=1
        count +=1
    return count

#Function to manage the calculation of the right minimum
def points_before0_for_negative(samples,index):
    count = 0
    while(samples[index] < 0 and count< 20):
        index +=1
        count +=1

    return count

def mean_confidence_interval(data, confidence=0.95):
    a = np.array(data)
    n = len(a)
    m, se = np.median(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n - 1)
    return m, m - h, m + h

#  ------- End functions that help  for the construction of matrix  --------