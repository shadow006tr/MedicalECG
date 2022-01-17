import numpy as np
from scipy.spatial import KDTree
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree


# Walk through:
# 1. check if the total of the pulses is at least 100, else terminate
# 2. do a K-MEANS as K = 1
# 3. find the distances from the center of the cluster using KD-Tree algorithm
# 4. percentileDist55 = 55th percentile of all distances, percentileDist2 = 2nd percentile of all distances
# 5. check for each pulse if the pulse is a noise or not by 2 criteria and then construct a new matrix with no noises
# 6. criterion 1: if detectNoisesWithRange is True don't add the pulse to the new matrix
# 7. criterion 2: if the distance of the selected pulse is bigger than percentileDist55 and
# 7. if number of neighbors in radius = percentileDist2 is smaller or equal to 0.2% of number pulses
# 7. then - don't add the pulse to the new matrix
# 8. else: add the pulse to the new matrix

def kMeansFilter6d(mat1, xx, yy, leadValues):
    X0 = mat1[xx:(yy + 1), 0]  # no. of sample
    X1 = mat1[xx:(yy + 1), 3]  # width
    X2 = mat1[xx:(yy + 1), 4]  # min
    X3 = mat1[xx:(yy + 1), 5]  # max
    X4 = mat1[xx:(yy + 1), 6]  # amount of slopes
    X6 = mat1[xx:(yy + 1), 1]  # power
    X7 = mat1[xx:(yy + 1), 8]  # median
    X8 = mat1[xx:(yy + 1), 9]  # standard deviation

    X = np.array(list(zip(X1, X2, X3, X4, X6, X7, X8)))

    if len(X) < 100:
        print("\nNo enough data.")
        # quit()

    dist_points_from_cluster_center = []
    no_of_clusters = 1
    k_model = KMeans(no_of_clusters)
    k_model.fit(X)
    dist_points_from_cluster_center.append(k_model.inertia_)
    print('WCSS = ')
    print(dist_points_from_cluster_center)
    centers = k_model.cluster_centers_

    tree = KDTree(X)
    arrQuery = centers
    print("\nThe center of the model with noises is:", centers)
    xSize = len(X)
    dist, ind = tree.query(arrQuery, k=xSize)

    # print("\nThe dist:", dist[0])
    percentileDist55 = np.percentile(
        dist[0], 55, interpolation='nearest')
    percentileDist2 = np.percentile(
        dist[0], 2, interpolation='nearest')
    print("The 2nd percentile:", percentileDist2, "; The 55th percentile:", percentileDist55)

    noNoisesX = []
    noNoisesSamples = []
    countPointsStayed = 0
    countNotAdded = 0
    countNotAddedFromRangeNoises = 0
    print("\nChecking the pulses to remove noises...")

    for i in range(0, xSize):
        # bar.update(i + 1)
        theSample = ind[0][i]
        thePoint = np.array(list(X[ind[0][i]]))
        if 3 < theSample < xSize - 3:
            if detectNoisesWithRange(int(X0[theSample - 4]), int(X0[theSample - 1]), int(X0[theSample]),
                                     int(X0[theSample + 3]), leadValues):
                countNotAddedFromRangeNoises = countNotAddedFromRangeNoises + 1
                continue

        if dist[0][i] > percentileDist55:

            counterInRadius = tree.query_radius([thePoint], percentileDist2, count_only=True)
            if counterInRadius > 0.002 * xSize:
                countPointsStayed = countPointsStayed + 1
                noNoisesX.append(thePoint)
                noNoisesSamples.append(X0[ind[0][i]])
            else:
                countNotAdded = countNotAdded + 1
        else:
            noNoisesX.append(list(X[ind[0][i]]))
            noNoisesSamples.append(X0[ind[0][i]])
    # bar.finish()
    print("\nTotal removed pulses:", countNotAdded + countNotAddedFromRangeNoises)
    print("\nSum of removed pulses from each sample close range:", countNotAddedFromRangeNoises)
    print("\nSum of removed pulses because similarities:", countNotAdded)
    print("Total not removed pulses with a bigger distance than the 55th percentile of the distance from the centroid:",
          countPointsStayed)
    noNoisesX = np.array(noNoisesX)
    print("The size of the remained matrix:", len(noNoisesX))
    print("Total remaining pulses:", len(noNoisesSamples))
    print("noNoiseX", noNoisesX[1])
    print("noNoiseSample", noNoisesSamples[1])

    return noNoisesX, noNoisesSamples


# target: to detect if the selected pulse's next 3 pulses and 3 pulses behind have more than 4% consecutive equal values
def detectNoisesWithRange(startILeft, endILeft, startIRight, endIRight, leadValues):
    counter = 0
    countZeroes = 0
    for i in range(startILeft + 1, endILeft + 1):
        counter = counter + 1
        if leadValues[i] == leadValues[i - 1]:
            countZeroes = countZeroes + 1
    for i in range(startIRight + 1, endIRight + 1):
        counter = counter + 1
        if leadValues[i] == leadValues[i - 1]:
            countZeroes = countZeroes + 1
    # print("zeroes counter =", countZeroes, leadValues[startILeft],
    # leadValues[endILeft], leadValues[startIRight], leadValues[endIRight])
    if countZeroes > 0.04 * counter:
        return True
    return False
