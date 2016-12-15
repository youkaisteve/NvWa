from numpy import *
import operator


def createDataSet():
    group = array([[0.1, 0.0], [0, 0.1], [0, 0], [1.0, 1.0], [1.0, 1.1]])
    labels = ['B', 'B', 'B', 'A', 'A']
    return group, labels


def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()

    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1

    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)

    return sortedClassCount[0][0]


def file2matrix(filename):
    fr = open(filename)
    lines = fr.readlines()
    numberOfLines = len(lines)
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []

    index = 0
    for line in lines:
        line = line.strip()
        splitlines = line.split('\t')
        returnMat[index, :] = splitlines[0:3]
        classLabelVector.append(int(splitlines[-1]))
        index += 1
    return returnMat, classLabelVector


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    m = dataSet.shape[0]
    normalDataSet = dataSet - tile(minVals, (m, 1))
    normalDataSet = normalDataSet / tile(ranges, (m, 1))

    return normalDataSet, ranges, minVals


# 32*32 image pixel
def img2Vector(file):
    resultVector = zeros((1, 1024))
    i = 0
    fr = open(file)
    for line in fr.readlines():
        for j in range(32):
            resultVector[0, 32 * i + j] = int(line[j])
        i += 1
    return resultVector

