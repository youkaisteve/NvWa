from trees import *

dataSet, labels = createDataSet()

myTree = createTree(dataSet, labels)

print(myTree)

# bestFeat = chooseBestFeatureToSplit(dataSet)
# print(bestFeat)

# shannonEnt = calcShannonEnt(dataSet)
# print(shannonEnt)

# labelsCount = {}
#
# labelsCount['yes'] = 10
# labelsCount['no'] = 20

# print(labelsCount.keys())
