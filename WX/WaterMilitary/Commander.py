"""
负责指挥调度，流程：
1.Commander开启战役，调用侦查兵侦查网站，判断帖子是否需要发表评论
2.侦察兵若发现目标，则取回目标参数，存入queue
3.参谋从queue中取出目标，分析并给出计划，将作战计划交给commander
4.commander收到计划后，交给soldier执行（进行评论）
"""

from collections import deque


class Commander:
    # 目标，比如百度贴吧
    target = None
    # 参谋
    StaffOfficers = None
    # 侦查员
    Scouts = None
    # 轰炸机
    Soldiers = None

    task_queue = deque()

    def go(self):
        print('给我上！')
