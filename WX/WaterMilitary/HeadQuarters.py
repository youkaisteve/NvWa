"""
指挥部，接收信息
"""

from collections import deque
import json
import configparser

global task_queue
# 任务队列，存的是帖子的id
task_queue = deque()

global msg_queue
# 消息队列，存的是帖子的id和标题
msg_queue = deque()

global message_map
message_map = json.loads(open('baidu_tieba_messagemap.json').read())

global config
config = configparser.ConfigParser()
config.read('tieba.conf')