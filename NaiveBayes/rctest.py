from bayes import *
import re
import jieba
import jieba.analyse
import random
import pickle
import os
import operator


def naiveClassify():
    # 准备dataset和class vector
    classVec = []
    reviewList = []

    wordListPath = 'review_comparison/解忧杂货铺_wordslist.pickle'
    if os.path.exists(wordListPath) == False:
        jieba.analyse.set_stop_words('review_comparison/stopwords_jieyou')
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


def wordStatistics():
    reviewClassifyCache = 'review_comparison/解忧杂货铺_classify.pickle'
    reviewClassify = {}
    # 将评论按星级分类
    if os.path.exists(reviewClassifyCache) == False:
        jieba.analyse.set_stop_words('review_comparison/stopwords_jieyou')
        f_jieyou = open('review_comparison/解忧杂货铺.txt', 'r')
        lines = f_jieyou.readlines()

        for review in lines:
            featureList = review.split('\t')
            content = featureList[4]
            rating = float(featureList[0].split(' ')[0])
            seg_list = jieba.analyse.extract_tags(content)

            if rating in reviewClassify:
                oldDictFeq = reviewClassify[rating]
                for token in seg_list:
                    if token in oldDictFeq:
                        oldDictFeq[token] += seg_list.count(token)
                    else:
                        oldDictFeq[token] = seg_list.count(token)
            else:
                dictFeq = {}
                for token in seg_list:
                    dictFeq[token] = seg_list.count(token)
                reviewClassify[rating] = dictFeq

        with open(reviewClassifyCache, 'wb') as f:
            pickle.dump(reviewClassify, f)
    else:
        print('skip reviewlist creating')
        reviewClassify = pickle.load(open(reviewClassifyCache, 'rb'))

    # 统计不同星级里面出现频率最高的前10个词汇
    for reviewInRating in reviewClassify:
        dictFeq = reviewClassify[reviewInRating]

        sortedFreq = sorted(dictFeq.items(), key=operator.itemgetter(1), reverse=True)
        print(reviewInRating)
        print(sortedFreq[:20])


wordStatistics()
