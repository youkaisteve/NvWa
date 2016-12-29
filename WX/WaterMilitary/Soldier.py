"""
炮灰：负责评论，发帖
"""

import configparser
import json
from urllib import request, parse


class Soldier:
    def __init__(self, account):
        """
        初始化
        :param account: 用户账号
        """
        self._account = account

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
                'tbs': 'b2bfdd62d0124df21482969715',
                'content': content,
                '__type__': 'reply'}
        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(str(config['comment']['uri']), data=data, headers=headers, method='POST')
        response = request.urlopen(req)
        resData = response.read().decode('utf-8')
        resJson = json.loads(resData)
        if resJson['err_code'] == 0:
            print('发表成功')
        else:
            print('发表失败：err_code:%s,content:%s' % (resJson['err_code'], resJson['data']['content']))


# so = Soldier('youkaisteve')
# so.comment('现在已经有很多网站开始把公众号的内容转化为小程序了！', '小程序', 4891595201, 1971972)
