

import warnings
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rcParams
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
from .help_functions import calc_distance


# walkthrough:
# 1. mat1 = new matrix [no noises]
# 2. try to find the optimal K of KMEANS, from 1 to 9 (included)
# 3. save the inertias, centers and labels for each Kmeans from K = 1 till K = 9
# 4. make a line from 2 points: inertia of K=1 AND k=9
# 5. the farest inertia from the line is "the elbow" therefore is the right K to detect the correct biggest cluster
# 6. return: K centers of KMEANS with the K we found and the labels of each pulse
def detectCluster6d(mat1):
    X = mat1
    dist_points_from_cluster_center = []
    centers = []
    labelsKmeans = []

    # Elbow method for finding the right K
    kLength = range(1, 10)
    for no_of_clusters in kLength:
        k_model = KMeans(n_clusters=no_of_clusters)
        k_model.fit(X)
        dist_points_from_cluster_center.append(k_model.inertia_)
        centers.append(k_model.cluster_centers_)
        labelsKmeans.append(k_model.labels_)

    print("Inertias (from k=1 to k=9):", dist_points_from_cluster_center)

    #
    # plt.plot(kLength, dist_points_from_cluster_center)
    # plt.plot([kLength[0], kLength[8]], [dist_points_from_cluster_center[0],
    #                      dist_points_from_cluster_center[8]], 'ro-')
    

    a = dist_points_from_cluster_center[0] - dist_points_from_cluster_center[8]
    b = kLength[8] - kLength[0]
    c1 = kLength[0] * dist_points_from_cluster_center[8]
    c2 = kLength[8] * dist_points_from_cluster_center[0]
    c = c1 - c2

    distance_of_points_from_line = []
    ratioInertias = []
    for k in range(9):
        distance_of_points_from_line.append(calc_distance(
            kLength[k], dist_points_from_cluster_center[k], a, b, c))
        if k > 0:
            ratioInertias.append(
                dist_points_from_cluster_center[k] / dist_points_from_cluster_center[k - 1])
        else:
            ratioInertias.append(0)

    # plt.plot(kLength, distance_of_points_from_line, 'ro-')
    # plt.show()

    print("Inertias ratios:", ratioInertias)

    #The point with max distance is the elbow and our K
    indexOfOptimumK = distance_of_points_from_line.index(
        max(distance_of_points_from_line))

    print("Number of clusters  =", str(indexOfOptimumK + 1))
    print("center final ",centers[indexOfOptimumK])
    print("labels final",labelsKmeans[indexOfOptimumK])
    return centers[indexOfOptimumK], labelsKmeans[indexOfOptimumK]
