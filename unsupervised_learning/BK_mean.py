import numpy as np
from K_mean import kMeans, eqDistance


def BK_means(data, k, dist=eqDistance):
    """
    Bisecting K-means overcums local-minimum problem of K-means by starting with one cluster
       an then split the cluster in two. Then it chooses a cluster to split vim SSE minimization.
    :param data: The data needs to be clusterized
    :param k: The count of clusters
    :param dist: The norm
    :return:  The list of clusters containing the data points and data distribution across clusters.
    """
    m = np.shape(data)[0] # the count of data-elements
    clusterAs = np.mat(np.zeros((m, 2)))
    initCentroid = np.mean(data, axis = 0).tolist()[0]
    cList = [initCentroid]
    for i in range(m):
        clusterAs[j, 1] = dist(np.mat(initCentroid), data[j, :])**2
    while (len(cList) < k):
        minSSE =np.inf
        for i in range(len(cList)):
            curPtsCluster = data[np.nonzero(clusterAs[:, 0].A == i)[0], :]
            cMat, splitClusterAss = kMeans(curPtsCluster, 2, dist)
            sseSplit = np.sum(splitClusterAss[:, 1])
            sseNoSplit = np.sum(clusterAs[np.nonzero(clusterAs[:, 0].A != i)[0], 1])
            if (sseNoSplit + sseSplit) < minSSE:
                bestCenToSplit = i
                bestNewCents = cMat
                bestClusterAss = splitClusterAss.copy()
                minSSe = sseSplit + sseNoSplit
        bestClusterAss[np.nonzero(bestClusterAss[:, 0].A == 1)[0], 0] = len(cList)
        bestClusterAss[np.nonzero(bestClusterAss[:, 0].A == 0)[0], 0] = bestCenToSplit
        cList[bestCenToSplit] = bestNewCents[0, :]
        cList.append(bestNewCents[1, :])
        clusterAs[np.nonzero(clusterAs[:, 0].A == bestCenToSplit)[0], :] = bestClusterAss
    return np.mat(cList), clusterAs

