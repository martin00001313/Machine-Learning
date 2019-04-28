class treeNode:
    """
    A class to hold each node of the tree.
    It has variables to hold the name of the node, a count.
    The nodeLink variable will be used to link similar items.
    Next, the parent variable is used to refer to the parent of this node in the tree.
    """
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        """
        Inorder travers of the tree, by providing hierarchic structure of the tree
        :param ind: shift of current data
        :return: None
        """
        print(' '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)


def createTree(dataSet, minSup=1):
    """
    A basic function to create FP tree.
    It takes the dataset and the minimum support as arguments and builds the FP -tree. This makes
    two passes through the dataset. The first pass goes through everything in the dataset
    and counts the frequency of each term. These are stored in the header table. Next,
    the header table is scanned and items occurring less than minSup are deleted.
    :param dataSet:
    :param minSup:
    :return:
    """
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
        for k in headerTable.keys():
            if headerTable[k] < minSup:
                del (headerTable[k])
        freqItemSet = set(headerTable.keys())
        if len(freqItemSet) == 0:
            return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null Set', 1, None)
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    """
    The function first tests if the first item in the transaction exists as a child node.
    If so, it updates the count of that item. If the item doesn’t exist, it creates a new treeNode and adds it as a chied.
    :param items:
    :param inTree:
    :param headerTable:
    :param count:
    :return:
    """
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):
    while (nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode