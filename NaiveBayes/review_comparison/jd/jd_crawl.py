import urllib.request
import urllib
import fnmatch
import os
import shutil
import random
import time
import re
import json
import asyncio
import aiohttp
import html

from requests import HTTPError
from collections import deque
from lxml import etree


# urlpattern - https://club.jd.com/comment/skuProductPageComments.action?productId=11452840&score=0&sortType=3&page=%d&pageSize=10&isShadowSku=0&callback=fetchJSON_comment98vv61564
class JDCrawl():
    bookname = ""
    urlpattern = "unnamed.txt"
    totalpages = 1
    savefilename = "saved.txt"
    tasks = []
    sem = asyncio.Semaphore(5)

    def __init__(self, bookname, urlpattern, totalpages):
        self.bookname = bookname
        self.urlpattern = urlpattern
        self.totalpages = totalpages

        if os.path.exists(bookname) == False:
            os.mkdir(bookname)

        self.savefilename = self.bookname + '.txt'
        if os.path.exists(self.savefilename):
            os.remove(self.savefilename)

        for i in range(0, totalpages):
            self.tasks.append(urlpattern % i)

        print('初始化完成')
        print('---------------------')

    def dispose(self):
        # if os.path.exists(self.bookname):
        #     os.rmdir(self.bookname)

        print('---------------------')
        print('执行结束')

    def extract_and_save(self, ajaxContent, index):
        formatStr = '%s\t%s\t%s\t%s\t%s\t%s\t%s\n'

        reviewlist = ajaxContent['comments']

        book = open(os.path.join(self.bookname, str(index) + '.txt'), 'w')

        for review in reviewlist:
            title = review['title']
            rating = review['score']
            content = str(review['content']).replace('\n', ' ')
            author = review['nickname']
            time = review['creationTime']
            province = review['userProvince']
            userlevel = review['userLevelName']
            book.write(formatStr % (rating, author, time, title, content, userlevel, province))

        book.close()

    def combineFiles(self, sourcepattern):
        tempfilename = "temp.tmp"
        with open(os.path.join(self.bookname, tempfilename), "a") as dest:
            for _, _, filenames in os.walk(self.bookname):
                for filename in fnmatch.filter(filenames, sourcepattern):
                    with open(os.path.join(self.bookname, filename)) as src:
                        shutil.copyfileobj(src, dest)
                        src.close()
                        os.remove(os.path.join(self.bookname, filename))
        os.rename(os.path.join(self.bookname, tempfilename), self.bookname + ".txt")

    @asyncio.coroutine
    def fetch(self, url, cnt):
        client = aiohttp.ClientSession()
        with (yield from self.sem):
            try:
                response = yield from client.get(url)
                body = yield from response.text()
                client.close()
                objecrStr = re.findall(r'\{.*\}', str(body))[0]
                object = json.loads(objecrStr)
                self.extract_and_save(object, cnt)
            except Exception as e:
                print(e)

    def run(self):
        f = asyncio.wait([self.fetch(task, self.tasks.index(task) + 1) for task in self.tasks])
        loop = asyncio.get_event_loop()
        loop.run_until_complete(f)
        loop.close()
        self.combineFiles('*.txt')
        self.dispose()


jdcrawl = JDCrawl(
    '解忧杂货铺',
    'https://club.jd.com/comment/skuProductPageComments.action?productId=11452840&score=0&sortType=3&page=%d&pageSize=10&isShadowSku=0&callback=fetchJSON_comment98vv61564',
    10)

jdcrawl.run()
