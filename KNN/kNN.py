from numpy import *
import operator
import random


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


def datingClassTest():
    hoRatio = 0.1
    datingMat, labels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingMat)
    m = normMat.shape[0]
    testNumbers = int(m * hoRatio)
    errorCount = 0.0
    for i in range(testNumbers):
        classifierResult = classify0(normMat[i, :], normMat[testNumbers:m, :], labels[testNumbers:m], 3)
        print('the classify0 call result is %d, and the real result is %s' % (classifierResult, labels[i]))
        if classifierResult != labels[i]:
            errorCount += 1

    print(errorCount / float(testNumbers))


def classifyPerson():
    resultList = ['not at all', 'in small does', 'in large does']
    flyMiles = float(input('filer mile earned per year:'))
    percentageOfGame = float(input('Percentage of time spent playing video games:'))
    litersOfIceCream = float(input('Liters of ice cream consumed per week:'))

    testPerson = array([flyMiles, percentageOfGame, litersOfIceCream])
    datingMat, labels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingMat)
    inArr = (testPerson - minVals) / ranges
    result = classify0(inArr, normMat, labels, 10)
    print('You will probably like this person:', resultList[result - 1])


def autoClassifyPerson():
    resultList = ['not at all', 'in small does', 'in large does']
    datingMat, labels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingMat)
    for i in range(100):
        testPerson = array([random.uniform(1.0, 10000.0), random.uniform(1.0, 20.0), random.uniform(0.5, 2.0)])
        inArr = (testPerson - minVals) / ranges
        result = classify0(inArr, normMat, labels, 10)
        print('Person in %f-%f-%f You will probably like this person:' % (testPerson[0], testPerson[1], testPerson[2]),
              resultList[result - 1])
