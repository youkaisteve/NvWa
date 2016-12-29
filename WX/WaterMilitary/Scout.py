"""
侦查员：负责分析数据，确定目标帖子
"""

import urllib.request
import urllib
import random


class Scout:
    userAgent = [
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    ]

    def camouflage(self, opener):
        """
        设置伪装
        :param opener: urllib.request.build_opener()
        """
        headers = {
            'User-Agent': random.choice(self.userAgent),
            'Accept': 'text/html;q=0.9,*/*;q=0.8'
        }
        opener.addheaders = [headers]

    def investigate(self, url):
        opener = urllib.request.build_opener()
        self.camouflage(opener)
        print('要的就是你')
