# Walkthrough:
# 1. classify the pulses to clusters from 'detectCluster6d' using the labels
# 2. construct a newer matrix without the biggest cluster
# 3. check if  number of remained pulses < 20 OR number of remained pulses < 4% of the lines of the no noises matrix - to terminate
# 4. once again try to find the optimal K of KMEANS, from 1 to 9 (included)
# 5. save the mean silhouette score, inertias, inertias ratios, centers and labels for each Kmeans from K = 1 till K = 9
# 6. make a line from 2 points: inertia of K=1 AND k=9
# 7. find the distances of each inertia from the line
# 8. check if we have too small clusters [if the cluster is bigger than 30 and 2% number of remained pulses then - it's not a tiny cluster]
# 8. but in the end we decide to find the optimum K according to the next cases:
# 8.1 if all the clusters are too small then - terminate
# 8.2 if according to elbow method K=2 AND InertiaOfKEqual2 / InertiaOfKEqual1  > 0.2
# 8.2 AND the mean silhouette score as K=2 < 0.7  then - we don't count on ELBOW method and we choose k=1
# 8.3 Else: we count on ELBOW method but we also print the optimum K by silhouette score
# 8.4 for 8.3 or 8.4 we find the closest pulse/s to the centroid/s
import gc
import numpy as np
from scipy.spatial import KDTree
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from .help_functions import calc_distance
import matplotlib.pyplot as plt


def secondKmeans(matrix1, arrCentroids, labelsKmeans, pulses):
    sizeMat1 = list(matrix1.shape)
    counters = []
    for k in arrCentroids:
        counters.append(0)
    print("\n secondKmean :: Starting to count clusters members...")
    print(sizeMat1[0])
    for i in range(0, sizeMat1[0]):
        for j in range(0, len(arrCentroids)):
            if labelsKmeans[i] == j:
                counters[j] = counters[j] + 1
                break
    print(" secondKmean :: The sizes of the clusters:", counters)
    indexOfBiggestCluster = counters.index(max(counters))
    print(" secondKmean :: The cluster with the max size is:", indexOfBiggestCluster + 1)



    # we take the biggest group and his information
    matrix_of_biggest_group = []
    matrix_of_biggest_group_pulse =[]
    # mat2 is the new matrix without the biggest group
    mat2 = []
    mat2Pulses = []
    print("\n secondKmean :: Starting to construct a new matrix without the biggest cluster...")

    for i in range(0, sizeMat1[0]):
        if labelsKmeans[i] != indexOfBiggestCluster:
            mat2.append(matrix1[i].tolist())
            mat2Pulses.append(pulses[i])
        else:
            matrix_of_biggest_group.append(matrix1[i].tolist())
            matrix_of_biggest_group_pulse.append(pulses[i])

    if len(mat2) < 20 or len(mat2) < 0.04 * sizeMat1[0]:
        print("\nNo diseases were found")
        return
        # quit()

    biggestcluster_centroid_array= []
    biggestcluster_centroid_array.append(arrCentroids[indexOfBiggestCluster])
    biggestcluster_optimumvalue, biggestcluster_optimumpulse,biggestcluster_matrix , biggestcluster_pulses = kmeansDetectClosestPointToCentroid(
        matrix_of_biggest_group,biggestcluster_centroid_array,matrix_of_biggest_group ,matrix_of_biggest_group_pulse,[len(matrix_of_biggest_group_pulse)])


    #creation an array for our clusters
    clusters = []
    clusters.append((biggestcluster_matrix[0], biggestcluster_pulses[0],len(matrix_of_biggest_group_pulse),biggestcluster_optimumvalue[0],biggestcluster_optimumpulse[0]))

    print("\n SecondKmeans :: The size of the new matrix without the biggest cluster:", len(mat2))

    matrix1 = 0
    dist_points_from_cluster_center = []
    centers = []
    X = mat2
    K = range(1, 10)
    sil_avgs = []
    labelsK = []

    # Elbow method in association with silhouette score
    for no_of_clusters in K:
        k_model = KMeans(n_clusters=no_of_clusters)
        k_model.fit(X)
        dist_points_from_cluster_center.append(k_model.inertia_)
        centers.append(k_model.cluster_centers_)
        labelsK.append(k_model.labels_)
        if no_of_clusters != 1:
            gc.collect()
            sil_avgs.append(silhouette_score(X, k_model.labels_))
        else:
            sil_avgs.append(0)

    print("SecondKmeans :: Inertias:", dist_points_from_cluster_center)
    print("SecondKmeans :: Silhouette averages:", sil_avgs)


    # plt.plot(K, dist_points_from_cluster_center)
    # plt.plot([K[0], K[8]], [dist_points_from_cluster_center[0],
    #                             dist_points_from_cluster_center[8]], 'ro-')
    # plt.show()

    # plt.plot(K, sil_avgs, 'g-')
    # plt.show()

    print('Silhouette', sil_avgs)
    a = dist_points_from_cluster_center[0] - dist_points_from_cluster_center[8]
    b = K[8] - K[0]
    c1 = K[0] * dist_points_from_cluster_center[8]
    c2 = K[8] * dist_points_from_cluster_center[0]
    c = c1 - c2

    distance_of_points_from_line = []
    ratioInertias = []
    for k in range(9):
        distance_of_points_from_line.append(calc_distance(
            K[k], dist_points_from_cluster_center[k], a, b, c))
        if k > 0:
            ratioInertias.append(
                dist_points_from_cluster_center[k] / dist_points_from_cluster_center[k - 1])
        else:
            ratioInertias.append(0)

    # plt.plot(K, distance_of_points_from_line, 'ro-')
    # plt.show()

    print("SecondKmeans :: Inertias ratios:", ratioInertias)
    print("SecondKmeans :: elbow distances:", distance_of_points_from_line)

    indexOfOptimumK = distance_of_points_from_line.index(
        max(distance_of_points_from_line))



    counters = []
    for i in range(0, indexOfOptimumK + 1):
        counters.append(0)
    countTinyClusters = indexOfOptimumK + 1
    print("\nStarting to construct a new matrix without the biggest cluster...")

    for i in range(0, len(labelsK[indexOfOptimumK])):
        for j in range(0, indexOfOptimumK + 1):
            if labelsK[indexOfOptimumK][i] == j:
                counters[j] = counters[j] + 1
                # de base cest 30 pas 10
                if counters[j] == max(10, round(0.02 * len(mat2))):
                    countTinyClusters = countTinyClusters - 1
                break





    j= 0
    clusters_matrix = []
    clusters_pulses= []
    for k in range(1+ indexOfOptimumK ):
        if (counters[k] >= max(10, round(0.02 * len(mat2)))):
            clusters_matrix.append([])
            clusters_pulses.append([])
            j+=1
        for i in range(0,len(mat2)):
            if(labelsK[indexOfOptimumK][i] == k and counters[k] >= max(10, round(0.02 * len(mat2))) ):
                clusters_matrix[j-1].append(mat2[i])
                clusters_pulses[j-1].append(mat2Pulses[i])



    print("\nFinal stage - clusters size:", counters, "; Clusters minimum bound:", max(10, round(0.02 * len(mat2))))
    if countTinyClusters == indexOfOptimumK + 1:
        print("\nNo diseases were found")
        print('rrrrrrrrrrrr')
        minValues, minPulses = kmeansDetectClosestPointToCentroid(X, centers[0], mat2Pulses)
        clusters.append((mat2, mat2Pulses, len(mat2),  minValues[0],minPulses[0]))
        # quit()
    elif (indexOfOptimumK - countTinyClusters + 1) == 1 and ratioInertias[1] > 0.2 and sil_avgs[1] < 0.7:
        print("\nOptimum value of k =", 1)
        minValues, minPulses,ordered_clustermatrix ,ordered_clusterpulses = kmeansDetectClosestPointToCentroid(X, centers[0],mat2, mat2Pulses,[len(mat2)])
        clusters.append((clusters_matrix[0] ,clusters_pulses[0],len(mat2),minValues[0],minPulses[0]))
        print(minPulses[0])
    else:
        print("\nOptimum elbow value; k =", str(indexOfOptimumK - countTinyClusters + 1))
        print("\nOptimum silhouette value; k =", str(
            sil_avgs.index(max(sil_avgs)) - countTinyClusters + 1))
        clusters_length = []
        for i in range(1 + indexOfOptimumK - countTinyClusters):
            clusters_length.append(len(clusters_pulses[i]))
        minValues,minPulses,ordered_clustermatrix ,ordered_clusterpulses= kmeansDetectClosestPointToCentroid(X, centers[indexOfOptimumK - countTinyClusters], mat2 ,mat2Pulses,clusters_length)
        for i in range(1+ indexOfOptimumK - countTinyClusters):
            print('Etape', i)
            clusters.append((ordered_clustermatrix[i],ordered_clusterpulses[i],len(clusters_matrix[i]),minValues[i],minPulses[i]))
        print ("Cluster 1-1", clusters[1][1])
    return clusters


#ordered_clustermatrix ,ordered_clusterpulses

# using KD-Tree => in 'ind' we have the indices and in 'dist' we have the distances
# This functions allows us to determine the delegate of each cluster in order to show it
def kmeansDetectClosestPointToCentroid(clusterSet, setCentroid, matrix , pulses,clusters_sizes):
    print('ClusterSet')
    X = np.array(clusterSet)
    tree = KDTree(X)
    arrQuery = setCentroid
    print("Centroids:", setCentroid)
    lengthX = len(X)
    dist, ind = tree.query(arrQuery, k=lengthX)
    print('ind: ',ind)
    cluster_matrix = {}
    cluster_pulse= {}

    minIndex = []
    minValues = []
    minPulses = []
    print('lenght centroids',len(setCentroid))
    #print(setCentroid)
    for i in range(0, len(setCentroid)):
        cluster_matrix[i] = []
        cluster_pulse[i]=[]
        minIndex.append(ind[i][np.argmin(dist[i])])
        minValues.append(clusterSet[minIndex[i]])
        minPulses.append(pulses[minIndex[i]])
        for j in range(0, clusters_sizes[i]):
            cluster_matrix[i].append(matrix[ind[i][j]])
            cluster_pulse[i].append(pulses[ind[i][j]])


    print("The delegates are:", minValues)
    print("The delegate pulse are:", minPulses)
    return minValues, minPulses,cluster_matrix , cluster_pulse




def findPulse(matX, samples):
    indices = []
    for s in samples:
        for i in range(0, len(matX)):
            if matX[i][0] == s:
                indices.append(i)
                break
    return indices
