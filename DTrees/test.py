from trees import *
import os

dataSet, labels = createDataSet()

# myTree = createTree(dataSet, labels)
# print(myTree)
# result = classify([1, 1], myTree, labels)
# print(result)

# bestFeat = chooseBestFeatureToSplit(dataSet)
# print(bestFeat)

# shannonEnt = calcShannonEnt(dataSet)
# print(shannonEnt)

# labelsCount = {}
#
# labelsCount['yes'] = 10
# labelsCount['no'] = 20

# print(labelsCount.keys())


# predict contact lens type

fr = open('lenses.txt')
lenses = [ins.strip().split('\t') for ins in fr.readlines()]
lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']

lensesTree = createTree(lenses, lensesLabels)
# exist = os.path.exists('lensesTree.pickle')
#
# if exist is False:
#     saveTree(lensesTree, 'lensesTree')
#     print(lensesTree)

myTree = getTree('lensesTree')

result = classify(['young', 'myope', 'yes', 'reduced'], myTree, lensesLabels)
print(result)