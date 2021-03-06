from kNN import *
import matplotlib
import matplotlib.pyplot as plt
from numpy import *
import random
from os import listdir


def datingClassTest():
    hoRatio = 0.1
    datingMat, labels = file2matrix('datingclassify/datingTestSet2.txt')
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
    datingMat, labels = file2matrix('datingclassify/datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingMat)
    inArr = (testPerson - minVals) / ranges
    result = classify0(inArr, normMat, labels, 10)
    print('You will probably like this person:', resultList[result - 1])


def autoClassifyPerson():
    resultList = ['not at all', 'in small does', 'in large does']
    datingMat, labels = file2matrix('datingclassify/datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingMat)
    for i in range(100):
        testPerson = array([random.uniform(1.0, 10000.0), random.uniform(1.0, 20.0), random.uniform(0.5, 2.0)])
        inArr = (testPerson - minVals) / ranges
        result = classify0(inArr, normMat, labels, 10)
        print('Person in %f-%f-%f You will probably like this person:' % (testPerson[0], testPerson[1], testPerson[2]),
              resultList[result - 1])


def handwritingTest():
    hwLabels = []

    trainingDir = '/Users/youkai/Downloads/trainingDigits'
    testDir = '/Users/youkai/Downloads/testDigits'

    trainingFiles = listdir(trainingDir)
    m = len(trainingFiles)
    trainingMat = zeros((m, 1024))
    for i in range(m):
        trainingFileStr = trainingFiles[i].split('.')[0]
        classname = trainingFileStr.split('_')[0]
        hwLabels.append(classname)

        trainingMat[i, :] = img2Vector('%s/%s' % (trainingDir, trainingFiles[i]))

    testFiles = listdir(testDir)
    mTest = len(testFiles)

    errorCount = 0
    for i in range(mTest):
        testFileStr = testFiles[i].split('.')[0]
        forTestClassName = int(testFileStr.split('_')[0])
        testInX = img2Vector('%s/%s' % (testDir, testFiles[i]))
        classifiedClassName = classify0(testInX, trainingMat, hwLabels, 3)

        classifiedClassName = int(classifiedClassName)
        isAccurate = forTestClassName == classifiedClassName

        if isAccurate == True:
            print('\033[32m classname for test is %d,classified classname is %d,you are right ' % (
                forTestClassName, int(classifiedClassName)))
        else:
            print('\033[31m classname for test is %d,classified classname is %d,you are wrong' % (
                forTestClassName, int(classifiedClassName)))
            errorCount += 1

    print('error rate is : %f' % (int(errorCount) / int(mTest)))


# sli
# group, labels = createDataSet()
#
# result = classify0([0, 0.2], group, labels, 3)
#
# print('result:%s' % result)

# dating
# datingMat, datingLabels = file2matrix('datingTestSet2.txt')
#
# normal, r, minVals = autNorm(datingMat)

# fig = plt.figure()
#
# ax = fig.add_subplot(111)
#
# ax.scatter(datingMat[:, 1], datingMat[:, 2], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
# ax.scatter(datingMat[:, 0], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
# ax.axis([-2, 25, -0.2, 2.0])
# plt.xlabel('Percentage of Time Spent Playing Video Games')
# plt.ylabel('Liters of Ice Cream Consumed Per Week')
#
# plt.show()

# datingClassTest()

# autoClassifyPerson()

handwritingTest()
