import numpy as np
import operator
import sys


def file_to_matrix(file_name):
    """
    The function to convert the contents of the file to matrix.
    :param file_name: Name of the file containing the data
    :return: matrix of the futures and labels of appropriate futures
    """
    fd = open(file=file_name, mode='r')
    lines = fd.readlines()
    samples_count = len(lines)

    assert samples_count != 0
    futures_count = len(lines[0].strip().split(' ')) - 1
    assert futures_count != 0
    mtx = np.zeros((samples_count, futures_count))
    labels = []
    cur_idx = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        futures = line.split(' ')
        assert len(futures) == futures_count + 1
        mtx[cur_idx, : ] = futures[0: futures_count]
        labels.append(int(futures[futures_count]))
        cur_idx += 1
    return mtx, labels


def image2Vector(file_name):
    """
    Coverts 32x32-{0, 1} image to 1x1024 vector.
    The function can be used for handwriting digit recognation.
    :param file_name:
    :return: 1x1024 NumPy array
    """
    res = np.zeros(1, 1024)
    fd = open(file_name)
    for i in range(32):
        line = fd.readline()
        for j in range(32):
            res[0, 32*i+j] = int(line[j])
    return res


def normalize_data(data):
    """
    Normailizes the data by mapping the values of futures to [0, 1]
    :param data: the futures need to normalize
    :return: normaized data
    """
    minVal = data.min(0)
    maxVal = data.max(0)
    range = maxVal - minVal
    normalizedData = np.zeros(data.shape())
    m = data.shape[0]
    normalizedData = data - np.tile((minVal, (m, 1)))
    normalizedData = normalizedData/np.tile(maxVal, (m, 1))
    return normalizedData


def predict_via_KNN(input, data, labels, k):
    """
    The goal of this function is to use the KNN algorithm to classify one piece of data.
    To calculate the distance is used Euclidian norm.
    :param input: the data need to be classified
    :param data: the features of predicted data
    :param labels: the labels of appropriate data
    :param k: the count of lowest distances for prediction of data
    :return: class of the input unlabeled data
    """
    dataSize = data.shape[0]
    distance = np.tile(input, (dataSize, 1)) - data
    sqDistance = distance ** 2
    distSum = sqDistance.sum(axis=1)
    distByNorm = distSum ** 0.5
    sortedDistIndices = distByNorm.argsort()
    classFrequanqe = {}
    for i in range(k):
        curLabel = labels[sortedDistIndices[i]]
        classFrequanqe[curLabel] = classFrequanqe.get(curLabel, 0) + 1
    sortedLabels = sorted(classFrequanqe.items(),
                          key=operator.itemgetter(1), reverse=True)
    print(sortedLabels)
    return sortedLabels[0][0]


def label_handwriten_digit(fn1, fn2):
    groups, labels = file_to_matrix(fn1)
    inX = image2Vector(fn2)
    return predict_via_KNN(inX, groups, labels, 3)


if __name__ == "__main__":
    groups, labels = file_to_matrix(sys.argv[1])
    unlabeled_data = open(sys.argv[2]).readlines()
    for i in unlabeled_data:
        inX = int(i)
        label = predict_via_KNN(inX, groups, labels, 3)
        print ("The label of {input_data} is {label}".format(input_data=inX, label = label))
    
