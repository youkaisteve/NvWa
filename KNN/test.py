from kNN import *

group, labels = createDataSet()

result = classify0([1, 1.2], group, labels, 3)

print('result:%s'%result)