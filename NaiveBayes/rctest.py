from bayes import *
import re
import jieba
import jieba.analyse
import random
import pickle
import os

# 准备dataset和class vector
classVec = []
reviewList = []

wordListPath = 'review_comparison/解忧杂货铺_wordslist.pickle'
if os.path.exists(wordListPath) == False:
    jieba.analyse.set_stop_words('./stopwords_cn')
    f_jieyou = open('review_comparison/解忧杂货铺.txt', 'r')
    lines = f_jieyou.readlines()

    for review in lines:
        featureList = review.split('\t')

        content = featureList[4]

        rating = float(featureList[0].split(' ')[0])

        if rating == 3.0:
            continue  # 不分析中间评价

        if rating >= 4.0:
            classVec.append(0)

        if rating <= 2.0:
            classVec.append(1)

        seg_list = jieba.analyse.extract_tags(content)
        reviewList.append(seg_list)

    with open(wordListPath, 'wb') as f:
        pickle.dump([reviewList, classVec], f)
else:
    print('skip reviewlist creating')
    data = pickle.load(open(wordListPath, 'rb'))
    reviewList = data[0]
    classVec = data[1]

vocablist = list([])
vocabulary = 'review_comparison/解忧杂货铺_vocabulary.txt'
if os.path.exists(vocabulary) == False:
    vocablist = createVocabList(reviewList)
    with open(vocabulary, 'w') as f:
        f.write(','.join(vocablist))
else:
    print('skip vocabulary creating')
    with open(vocabulary, 'r') as fr:
        vocablist = list(fr.read().split(','))

reviewCountList = list(range(len(reviewList)))
trainMatrix = []
trainVec = []

trainresult = 'review_comparison/解忧杂货铺_train.pickle'
if os.path.exists(trainresult) == False:
    for review in range(int(len(reviewList) * 0.9)):
        randIndex = int(random.uniform(0, len(reviewCountList)))
        trainMatrix.append(bagOfWords2VecMN(vocablist, reviewList[randIndex]))
        trainVec.append(classVec[randIndex])
        del (reviewCountList[randIndex])

    p0, p1, pf1 = trainNB0(trainMatrix, trainVec)
    with open(trainresult, 'wb') as f:
        pickle.dump([p0, p1, pf1], f)
else:
    print('skip training')
    with open(trainresult, 'rb') as fr:
        results = pickle.load(fr)
        p0 = results[0]
        p1 = results[1]
        pf1 = results[2]

errorCount = 0
for index in reviewCountList:
    testVec = bagOfWords2VecMN(vocablist, reviewList[index])
    classified = classifyNB0(testVec, pf1, p0, p1)
    if classified != classVec[index]:
        errorCount += 1

print('error rate is : %f' % (float(errorCount) / len(reviewCountList)))
