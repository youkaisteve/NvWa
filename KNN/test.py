from kNN import createDataSet, classify0

group, labels = createDataSet()

result = classify0([1, 1.2], group, labels, 3)

print('result:%s' % result)
