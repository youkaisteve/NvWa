from trees import *

dataSet, labels = createDataSet()

myTree = createTree(dataSet, labels)
print(myTree)
result = classify([1, 1], myTree, labels)
print(result)

# bestFeat = chooseBestFeatureToSplit(dataSet)
# print(bestFeat)

# shannonEnt = calcShannonEnt(dataSet)
# print(shannonEnt)

# labelsCount = {}
#
# labelsCount['yes'] = 10
# labelsCount['no'] = 20

# print(labelsCount.keys())
