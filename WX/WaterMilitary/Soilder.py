"""
炮灰：负责评论，发帖
"""

import configparser
import json
from urllib import request, parse
from HeadQuarters import *
import json
import time


class Soilder:
    def __init__(self, account):
        """
        初始化
        :param account: 用户账号
        """
        self._account = account
        self._fighting = False

    def comment(self, content, kw, tid, fid):
        """
        发表评论
        :param content: 评论内容
        :param kw: 贴吧名字
        :param tid:帖子id
        :param fid:贴吧id
        :return:
        """
        config = configparser.ConfigParser()
        config.read('tieba.conf')
        cookieStr = str(config[self._account]['cookie'])
        headers = {
            'content-type': str(config['comment']['content-type']),
            'cookie': cookieStr
        }
        data = {'ie': 'utf-8',
                'kw': kw,
                'fid': fid,
                'tid': tid,
                'vcode_md5': '',
                'tbs': '223dd4125c08dd201483064442',
                'content': content,
                '__type__': 'reply'}
        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(str(config['comment']['uri']), data=data, headers=headers, method='POST')
        response = json.loads(request.urlopen(req).read().decode('utf-8'))
        if response['err_code'] == 0:
            print('发表成功 >>> %s' % tid)
        else:
            err_code = response['err_code']
            print('发表失败：err_code:%s,content:%s' % (err_code, globals().get('message_map')['messageMap'][err_code]))

    def fight(self):
        while globals().get('task_queue'):
            id = globals().get('task_queue').popleft()
            self.comment('就是以前做的那些', '小程序', id, 1971972)
            time.sleep(3)

    def done(self):
        self._fighting = False

# so = Soilder('youkaisteve')
# so.comment('现在已经有很多网站开始把公众号的内容转化为小程序了！', '小程序', 4891595201, 1971972)
