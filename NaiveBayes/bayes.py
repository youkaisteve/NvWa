'''

Created on Dec 19,2016

'''

from numpy import *
import re

def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]  # 1 is abusive, 0 not
    return postingList, classVec


def createVocabList(dataLists):
    vocabListSet = set([])
    for document in dataLists:
        vocabListSet = vocabListSet | set(document)
    return list(vocabListSet)


def setOfWords2Vec(vocabList, inputSet):
    result = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            result[vocabList.index(word)] += 1
    return result


def trainNB0(trainMatrix, categorys):
    numberOfDocs = len(trainMatrix)
    numberOfWords = len(trainMatrix[0])
    pAbusive = sum(categorys) / numberOfDocs

    p0nums = ones(numberOfWords)
    p1nums = ones(numberOfWords)
    p0TotalWords = 2.0
    p1TotalWords = 2.0

    for i in range(numberOfDocs):
        if categorys[i] == 1:
            p1nums += trainMatrix[i]
            p1TotalWords += sum(trainMatrix[i])
        else:
            p0nums += trainMatrix[i]
            p0TotalWords += sum(trainMatrix[i])

    return log(p0nums / p0TotalWords), log(p1nums / p1TotalWords), pAbusive


def classifyNB0(vec2Classify, pAbusive, p0Vec, p1Vec):
    p0 = sum(p0Vec * vec2Classify) + log(1 - pAbusive)
    p1 = sum(p1Vec * vec2Classify) + log(pAbusive)

    if p0 > p1:
        return 0
    else:
        return 1


def textParser(bigString):
    splitWords = re.split(r'\W*', bigString)
    return [word.lower() for word in splitWords if len(word) > 2]


def spamTest():
    docList = []
    classList = []

    for i in range(1, 26):
        wordList = textParser(open('ham/%d.txt' % i).read())
        docList.append(wordList)
        classList.append(0)

        wordList = textParser(open('spam/%d.txt' % i).read())
        docList.append(wordList)
        classList.append(1)

    vocabList = createVocabList(docList)

    trainingSet = list(range(50))
    testSet = []
    for i in range(10):
        randomIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randomIndex])
        del (trainingSet[randomIndex])

    trainMat = []
    trainClassVec = []

    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
        trainClassVec.append(classList[docIndex])

    p0, p1, pAb = trainNB0(trainMat, trainClassVec)

    errorCount = 0
    for docIndex in testSet:
        classified = classifyNB0(array(setOfWords2Vec(vocabList, docList[docIndex])), pAb, p0, p1)
        if classified != classList[docIndex]:
            errorCount += 1

    print('error rate is : %f' % (float(errorCount) / len(classList)))

    # hamTemp = zeros(len(vocabList))
    # spamTemp = zeros(len(vocabList))
    # for docIndex in range(len(trainMat)):
    #     for wordIndex in range(len(vocabList)):
    #         if classList[docIndex] == 1:
    #             spamTemp[wordIndex] += trainMat[docIndex][wordIndex]
    #         else:
    #             hamTemp[wordIndex] += trainMat[docIndex][wordIndex]
    #
    # for wordIndex in range(len(vocabList)):
    #     print('word:"%s" occurs %d times in ham,occurs %d times in spam' % (
    #         vocabList[wordIndex], hamTemp[wordIndex], spamTemp[wordIndex]))
