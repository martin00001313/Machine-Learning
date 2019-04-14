import numpy as np


def loadData(filePath):
    """
    Utility function to load the data from the file provided by file_path
    :param filePath: Path+name of the file for the data to be loaded
    :return: list each element of the list contains fields of the appropriate field
    """
    data = []
    fs = open(filePath, mode='r')
    for line in fs.readline():
        cur = line.strip().split('\t')
        floatV = map(float, cur)
        data.append(floatV)
    return data


def eqDistance(vA, vB):
    """
    Utility function to calculate Euclidean distance
    :param vA: the first data
    :param vB: the second data
    :return: the Euclidean distance of provided data
    """
    return np.sqrt(np.sum(np.power(vA-vB, 2)))


def randCentroids(data, k):
    """
    Utility function to randomly choose k centroids
    :param data:
    :param k:
    :return:
    """
    n = np.shape(data)[1] # get rows count
    centroids = np.mat(np.zeros(k, n)) # Interpret the input as a matrix.
    for j in range(n):
        minEl = np.min(data[:, j]) # get minimum elements of the j'th row
        rangeEl = float(np.max(data[:, j]) - minEl)
        centroids[:, j] = minEl + rangeEl*np.random.rand(k, 1)
    return centroids


def kMeans(data, k, distF = eqDistance, createCent= randCentroids):
    """
    Core K-Means implementation.
    :param data: The data to be used for clustering.
    :param k: The count of clusters.
    :param distF: The distance of the metrice to be used.
    :param createCent: Specifies the initial centroids selection.
    :return: The list of clusters containing the data points and data distribution across clusters.
             sum(clusterAs[1, :]) is SSE, which cen be used as error predictor.
    """
    m = np.shape(data)[0] # the count of columns, i.e. the size of the data
    centroids = createCent(data, k)
    clusterAs = np.mat(np.zeros((m, 2)))
    clusterChanged = False
    while clusterChanged:
        clusterChanged = False
        for i in range(m): # iterate on each data
            minDist = np.inf
            minIdx = -1
            for j in range(k): # iterate on each cluster
                dist = distF(centroids[j, :], data[i, :])
                if dist < minDist:
                    minDist = dist
                    minIdx = j
                clusterChanged = (clusterAs[i, 0] != minIdx)
                clusterAs[i, :] = minIdx, minDist**2
            for c in range(k):
                ptsInCluster = data[np.nonzero(clusterAs[:, 0].A == c)]
                centroids[c, :] = np.mean(ptsInCluster, axis=0)
    return centroids, clusterAs


def example(data_path):
    data = np.mat(loadData(data_path))
    centroids, cAssign = kMeans(data, 3)
    print(centroids, cAssign)


