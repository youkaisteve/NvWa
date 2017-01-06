"""
负责指挥调度，流程：
1.Commander开启战役，调用侦查兵侦查网站，判断帖子是否需要发表评论
2.侦察兵若发现目标，则取回目标参数，存入queue
3.参谋从queue中取出目标，分析并给出计划，将作战计划交给commander
4.commander收到计划后，交给soldier执行（进行评论）
"""

from collections import deque
from Scout import Scout
from StaffOfficer import StaffOfficer
from Soilder import Soilder
from HeadQuarters import *
from baidu.baiduclient import login


class Commander:
    def __init__(self, target, StaffOfficer, Scout, Soldier):
        self._target = target
        self._StaffOfficer = StaffOfficer
        self._Scout = Scout
        self._Soldier = Soldier

    def go(self):
        globals().get('config').read('baidu/tieba.conf')
        # ok = login('youkaisteve', 'mssj123!@#', '小程序')
        # if ok:
        #     print('登录成功')
        # else:
        #     print('登录失败')

        self._Scout.investigate(self._target)
        self._StaffOfficer.work()
        self._Soldier.fight('小程序')


scout = Scout()
staff = StaffOfficer()
soilder = Soilder('youkaisteve')
commander = Commander('http://tieba.baidu.com/f?kw=%E5%B0%8F%E7%A8%8B%E5%BA%8F&ie=utf-8&pn=0',
                      staff, scout, soilder)
commander.go()
