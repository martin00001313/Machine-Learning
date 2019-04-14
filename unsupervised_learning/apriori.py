import numpy as np

def loadData():
    pass


def createFSet1(data):
    """
    The function to create a frozenset for each relation/item.
    :param data: Data to be scanned
    :return: frozenset of all data items. (i.e. const set, which can be used as a key in a map)
    """
    res = []
    for col in data:
        for i in col:
            if not [i] in res:
                res.append([i])
    res.sort()
    return map(frozenset, res)


def scanData(data, Ck, minSupport):
    """
    Function to filter the data by keeping items, having at last the provided minimum support
    :param data: Data to be scanned
    :param Ck: List of candidate states
    :param minSupport: Minimum support
    :return: Scaned dataset having >=minSupport support and support values
    """
    ssCnt = {}
    for i in data:
        for c in Ck:
            if c.issubset(i):
                if ssCnt.has_key(c):
                    ssCnt[c] += 1
                else:
                    ssCnt[c] = 1
    dataSize = len(data)
    supportData = {}
    res = []
    for k in ssCnt:
        curSupport = ssCnt[k] / dataSize
        if curSupport >= minSupport:
            res.insert(0, k)
        supportData[k] = curSupport
    return res, supportData


def aprioriGen(Lk, k):
    """
    Function to create candidate itemsets
    :param Lk: list of frequent itemsets
    :param k: the size of the itemsets
    :return:
    """
    res = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:, k-2]
            L2 = list(Lk[j])[:, k-2]
            if L1 == L2:
                res.append(L1 | L2)
    return res


def apriori(data, minSupport = 0.13):
    c1 = createFSet1(data)
    d = map(set, data)
    L1, supportData = scanData(d, c1, minSupport)
    L = L1
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanData(d, Ck, minSupport)
        L.append(Lk)
        k += 1
    return L, supportData


