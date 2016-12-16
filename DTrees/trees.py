from math import log
import operator


def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]

    labels = ['no surfacing', 'flippers']

    return dataSet, labels


# calc entropy （计算熵）
def calcShannonEnt(dataSet):
    numbersOfSet = len(dataSet)
    labelsCount = {}

    for featVec in dataSet:
        curLabel = featVec[-1]
        if curLabel not in labelsCount.keys():
            labelsCount[curLabel] = 0
        labelsCount[curLabel] += 1

    shannonEnt = 0.0
    for key in labelsCount:
        prop = float(labelsCount[key]) / numbersOfSet
        shannonEnt -= prop * log(prop, 2)

    return shannonEnt


def splitDataSet(dataset, axis, value):
    returnDataSet = []

    for featVec in dataset:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis + 1:])
            returnDataSet.append(reducedFeatVec)

    return returnDataSet


# 选择确定性最高的特征
def chooseBestFeatureToSplit(dataset):
    numberOfFeatures = len(dataset[0]) - 1
    baseShannonEnt = calcShannonEnt(dataset)
    bestFeatAxis = 0
    infoGain = 0.0
    for i in range(numberOfFeatures):
        features = [example[i] for example in dataset]
        uniqueFeatures = set(features)

        newShannonEnt = 0.0
        for feature in uniqueFeatures:
            subDataSet = splitDataSet(dataset, i, feature)

            prop = float(len(subDataSet)) / len(dataset)
            newShannonEnt += prop * calcShannonEnt(subDataSet)

        newinfoGain = baseShannonEnt - newShannonEnt
        if newinfoGain > infoGain:
            infoGain = newinfoGain
            bestFeatAxis = i

    return bestFeatAxis


def majorityCnt(classList):
    classCount = {}

    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1

    sortedClassCount = sorted(classCount.items(), operator.itemgetter(1), reversed=True)

    return sortedClassCount[0][0]


def createTree(dataset, labels):
    classList = [example[-1] for example in dataset]

    if classList.count(classList[0]) == len(dataset):
        return classList[0]

    if len(dataset[0]) == 1:
        return majorityCnt(classList)

    bestFeat = chooseBestFeatureToSplit(dataset)
    bestFeatLabel = labels[bestFeat]

    uniqueValues = set([example[bestFeat] for example in dataset])

    myTree = {bestFeatLabel: {}}
    for val in uniqueValues:
        myTree[bestFeatLabel][val] = createTree(splitDataSet(dataset, bestFeat, val), labels[:])

    return myTree