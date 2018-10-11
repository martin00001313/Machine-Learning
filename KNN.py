# KNN:  k-Nearest Neighbors
# Pros: Insensitive to outliers, no assumption about data, high accuracy
# Cons: Computationally expensive, requires a lot of memory

"""

"""

import numpy as np
import operator

def loadDataSet() -> [np.array, list]:
    """
    The function creates/loads the dataset and labels
    :return numpy array of dataset and list of labels:
    """
    pass

def classifyByKNN(X, dataSet, labels, k)
    """"
    For every point in our dataset:
        calculate the distance between X and the current point
            by using Euclidean distance: sqrt(SUM(Xi^2)) 
        sort the distances in increasing order
        take k items with lowest distances to X
        find and return the majority class among this items
    :param X:  the input data need to classify 
    :param dataSet: the trained dataset 
    :param labels: labels of appropriate trained data
    :param k: the number of neighbors to predict the data
    :return: the label of input data
    """
    # Distance calculation
    dataSize = dataSet.shape[0]
    diff = np.tile(X, (dataSize, 1)) - dataSet
    sqDiff = diff ** 2
    sqDistace = sqDiff.sum(axis=1)
    distances = sqDistace ** 0.5
    sortDistances = distances.argsort()
    # Voting with lowest k distances
    classCount = {}
    for i in range(k) :
        curLabel = labels[sortDistances[i]]
        classCount[curLabel] = classCount.get(curLabel, 0) + 1
    sortedClassByCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortDistances[0][0]
