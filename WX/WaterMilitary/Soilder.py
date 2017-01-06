"""
炮灰：负责评论，发帖
"""

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
        self.config = globals().get('config')

    def comment(self, kw, tid, fid):
        """
        发表评论
        :param content: 评论内容
        :param kw: 贴吧名字
        :param tid:帖子id
        :param fid:贴吧id
        :return:
        """
        cookie_str = str(self.config[self._account]['cookie'])
        content = str(self.config[self._account]['water'])
        headers = {
            'content-type': str(self.config['comment']['content-type']),
            'cookie': cookie_str
        }
        data = {'ie': 'utf-8',
                'kw': kw,
                'fid': fid,
                'tid': tid,
                'vcode_md5': '',
                'tbs': '3ccb879e4ac38b261483668754',
                'content': content,
                '__type__': 'reply'}
        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(str(self.config['comment']['uri']), data=data, headers=headers, method='POST')
        response = json.loads(request.urlopen(req).read().decode('utf-8'))
        if response['err_code'] == 0:
            print('发表成功 >>> %s' % tid)
        else:
            err_code = response['err_code']
            print(
                '发表失败：err_code: %s,content: %s' % (
                str(err_code), globals().get('message_map')['messageMap'][str(err_code)]))

    def fight(self, where):
        fid = str(self.config[where]['fid'])
        kw = str(self.config[where]['kw'])
        self._fighting = True
        while globals().get('task_queue') and self._fighting:
            id = globals().get('task_queue').popleft()
            self.comment(kw, id, fid)
            time.sleep(3)

    def done(self):
        self._fighting = False

# so = Soilder('youkaisteve')
# so.comment('现在已经有很多网站开始把公众号的内容转化为小程序了！', '小程序', 4891595201, 1971972)
