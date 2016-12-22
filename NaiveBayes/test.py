from bayes import *

#
# postLists, classVec = loadDataSet()
# vocabList = createVocabList(postLists)
#
# print(vocabList)
#
# trainMatric = []
#
# for i in range(len(postLists)):
#     trainMatric.append(setOfWords2Vec(vocabList, postLists[i]))
#
# p0Vec, p1Vec, pAbusive = trainNB0(trainMatric, classVec)
#
# testEntry = ["I", "love", "worthless", "work"]
# thisDoc = array(setOfWords2Vec(vocabList, testEntry))
# result = classifyNB0(thisDoc, pAbusive, p0Vec, p1Vec)
#
# print(result)

spamTest()