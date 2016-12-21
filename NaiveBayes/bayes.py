'''

Created on Dec 19,2016

'''

from numpy import *


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
            result[vocabList.index(word)] = 1
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
        return False
    else:
        return True
