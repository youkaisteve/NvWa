"""
侦查员：负责分析数据，确定目标帖子
"""

from urllib import request, parse
import urllib
import random
import logging
from lxml import etree
import re
from HeadQuarters import *


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
        opener = request.build_opener()
        self.camouflage(opener)
        response_html = opener.open(url).read().decode('utf-8')
        self.interpret(response_html)

    def interpret(self, html):
        selector = etree.HTML(html)
        article_list = selector.xpath('//ul[@id="thread_list"]//a[@class = "j_th_tit "]')
        for article_a in article_list:
            globals().get('msg_queue').append((re.findall(r'\d*', article_a.xpath('@href')[0])[3], article_a.xpath('text()')[0]))
            print("Scout >>> I find something and send to HeadQuarters")

#
# scout = Scout()
# scout.investigate('http://tieba.baidu.com/f?kw=%E5%B0%8F%E7%A8%8B%E5%BA%8F&ie=utf-8&pn=0')
