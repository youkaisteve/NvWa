# 为了说明条件概率对于我们判断的影响
# 计算对于A病的检查，正确地概率是多大 （以下全是假设值）

# 条件1：患A病者做检查，呈阳性和阴性的概率
positiveIfPositive = 0.99
positiveIfNegative = 0.01

# 条件2：不患A病者做检查，呈阳性和阴性的概率
negativeIfPositive = 0.01
negativeIfNegative = 0.99

# 条件3：一般人群患A病的概率
averageRate = 0.4

# 那么假设有10万人来做检查，误查（没患A病被查出是阳性）的概率是多少？

# 根据一般概率，10万人中，检查出阳性的为100000 * 0.001 = 100
totalPerson = 100000
averagePerson = totalPerson * averageRate

# 这100患病的人中，其实只有%99的人检查出阳性(根据条件1)
resultPositiveInPositive = averagePerson * positiveIfPositive

# 剩下的99900不患病的人中，检查出阳性的概率为0.01(根据条件2)
resultPositiveInNegative = (totalPerson - averagePerson) * negativeIfPositive

# 最后阳性的结果是二者的和，但是在这个呈现阳性的检查结果里面，实际患病的只有99人（因为有一人检查结果呈现阴性）
resultPositive = resultPositiveInPositive + resultPositiveInNegative
realPositiveInResult = resultPositiveInPositive / resultPositive

print(realPositiveInResult)

# 不断改变条件3 - averageRate的值，你会发现，当普遍患病概率越高，检查的正确率就越高。
# 所以医院会做多想检查，最后根据条件概率来判断。
# 打个比方（也许不是很恰当），检查艾滋病时，吸毒者检查出来呈现阳性的概率就要比一般人高出很多；
# 如果没有吸毒这个条件，误差的概率会变得较高，就像以上假定实验一样。
