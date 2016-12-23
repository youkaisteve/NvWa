from bayes import *
import feedparser
import pickle
import re

fr = open('stopwords')
stopWords = re.split(r'\W*', fr.read())
#
# postLists, classVec = loadDataSet()
# vocabList = createVocabList(postLists)
#
# print(vocabList)
#
# trainMatric = []
#
# for i in range(len(postLists)):
#     trainMatric.append(bagOfWords2VecMN(vocabList, postLists[i]))
#
# p0Vec, p1Vec, pAbusive = trainNB0(trainMatric, classVec)
#
# testEntry = ["I", "love", "worthless", "work"]
# thisDoc = array(bagOfWords2VecMN(vocabList, testEntry))
# result = classifyNB0(thisDoc, pAbusive, p0Vec, p1Vec)
#
# print(result)

# spamTest(stopWords)

# 纽约
# ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
# with open('ny.pickle', 'wb') as f:
#     pickle.dump(ny, f)
#
# 旧金山湾区
# sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
# with open('sf.pickle', 'wb') as f:
#     pickle.dump(sf, f)

# ny = pickle.load(open('ny.pickle', 'rb'))
# sf = pickle.load(open('sf.pickle', 'rb'))
#
# localWords(ny, sf, stopWords)
