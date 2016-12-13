from kNN import createDataSet, classify0, file2matrix
import matplotlib
import matplotlib.pyplot as plt
from numpy import *

# sli
# group, labels = createDataSet()
#
# result = classify0([1, 1.2], group, labels, 3)
#
# print('result:%s' % result)

# dating
datingMat, datingLabels = file2matrix('datingTestSet2.txt')

fig = plt.figure()

ax = fig.add_subplot(111)

ax.scatter(datingMat[:, 1], datingMat[:, 2], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
ax.axis([-2, 25, -0.2, 2.0])
plt.xlabel('Percentage of Time Spent Playing Video Games')
plt.ylabel('Liters of Ice Cream Consumed Per Week')

plt.show()
