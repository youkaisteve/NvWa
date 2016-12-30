"""
参谋：负责构思文案
"""

from HeadQuarters import *


class StaffOfficer:
    isWorking = False

    def work(self):
        self.isWorking = True
        while globals().get('msg_queue'):
            msg = globals().get('msg_queue').popleft()
            if self.conceive(msg[1]):
                print('StaffOfficer >>> I make it out in "%s"' % msg[1])
                globals().get('task_queue').append(msg[0])

    def take_a_rest(self):
        self.isWorking = False

    def conceive(self, msg):
        try:
            index = msg.index('张小龙')
            return index >= 0
        except:
            return False
