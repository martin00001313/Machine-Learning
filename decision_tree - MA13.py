import numpy as np
import math
import operator


def entropy(dataSet):
    """
    To calculate Shannon entropy for the given dataset, i.e H(E)=-sum(p*logp)
    The detailes of such calculation are based on Khinchin's theorem.
    The higher the entropy, the more mixed up the data is.
    Alternative way is to use Gini imurity, i.e. Gini(E) = 1-sum(p**2)
    :param dataSet: The dataset, for which there is need to calculate entropy
    :return: returns Shannon entropy for the given dataset.
    """
    labelsFrequ = {}
    for i in dataSet:
        labelsFrequ[i[-1]] = labelsFrequ.get(i[-1], 0) + 1
    entropy = 0.
    dataSize = len(dataSet)
    for label, count in labelsFrequ.items():
        prob = float(count) / dataSize
        entropy -= prob * math.log(prob, 2)
    return entropy


def split_data(dataset, axis, value):
    """
    To split dataset by given axis and value.
    Returnes new dataset, which constaines futures containing the value.
    :param dataset: The given data need to split.
    :param axis: The axis to split
    :param value: The value to split
    :return: New generated dataset
    """
    retDataSet = []
    for ft in dataSet:
        if ft[axis] == value:
            newFutureVector = ft[:axis]
            newFutureVector.extend(ft[axis+1:])
            retDataSet.append(newFutureVector)


def best_future_to_split(dataSet):
    """
    To choose the besst future to split the dataset.
    :param dataSet: The given dataset should be passed as list of lists
                    and all lists are equal size
    :return: The best future to split the dataset.
    """
    futuresCount = len(dataSet)-1
    baseEntropy = entropy(dataSet)
    bestFeature = -1
    bestInfoGain = 0.
    for i in range(futuresCount):
        featList = [example[i] for example in dataSet]
        uniquieVals = set(featList)
        newEntropy = 0.
        for val in uniquieVals:
            subData = split_data(dataset=dataSet, axis=i, value=val)
            p_val = len(subData) / float(futuresCount)
            newEntropy += p_val * entropy(subData)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestFeature = i
            bestInfoGain = infoGain
    return bestFeature


def majority_count(labels):
    """
    The function to handle cases when the dataset has run out of attributes
    but the class labels are not all the same.
    :param labels: list of labels
    :return: the label. which has majority vote
    """
    labelFreq = {}
    for l in labels:
        labelFreq[l] = labelFreq.get(l, 0) + 1
    sortedByVote = sorted(labelFreq.items(), key=operator.itemgetter(1), reverse=True)
    return sortedByVote[0][0]


def create_tree(dataSet, labels):
    """
    The function to create a dicission tree from the given trailing dataset.
    :param dataSet: Trailing features' list as trailing data
    :param labels: The labels of appropriate futures
    :return: Generated dicission tree
    """
    classList = [data[-1] for data in dataSet]
    # Stop when all classes are the same
    if classList.count(classList[0]) == len(classList):
        return classlist[0]
    # Stop when no more future, return most frequence label
    if len(dataSet[0]) == 1:
        return majority_count(classList)
    futToSplit = best_future_to_split(dataSet)
    labelofSplit =  labels[futToSplit]
    genTree = {labelofSplit:{}}
    del (labels[futToSplit])
    featValues = [example[futToSplit] for example in dataSet]
    uniqueVals = set(featValues)
    for val in uniqueVals:
        subLabels = labels[:]
        genTree[labelofSplit][val] = create_tree(split_data(dataSet, futToSplit, val), subLabels)
    return genTree


def classify_via_dicission_tree(tree, labels, vec):
    firstStr = inputTree.keys()[0]
    secondDict = tree[firstStr]
    featIndex = labels.index(firstStr)
    for key in secondDict.keys():
        if vec[featIndex] == key:
            if type(secondDict[key]).__name__ == "dict":
                classLabel = classify_via_dicission_tree(secondDict[key], labels, vec)
            else:
                classLabel = secondDict[key]
    return classLabel
