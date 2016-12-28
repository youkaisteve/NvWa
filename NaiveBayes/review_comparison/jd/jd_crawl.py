import urllib.request
import urllib
import fnmatch
import os
import shutil
import random
import time
import re

from requests import HTTPError
from collections import deque
from lxml import etree


# urlpattern - https://club.jd.com/comment/skuProductPageComments.action?productId=11452840&score=0&sortType=3&page=%d&pageSize=10&isShadowSku=0&callback=fetchJSON_comment98vv61564
class JDCrawl():
    bookname = ""
    urlpattern = "unnamed.txt"
    totalpages = 1
    savefilename = "saved.txt"
    queue = deque()

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
            self.queue.append(urlpattern % i)

        print('初始化完成')
        print('---------------------')

    def dispose(self):
        # if os.path.exists(self.bookname):
        #     os.rmdir(self.bookname)

        print('---------------------')
        print('执行结束')

    def extract_and_save(self, ajaxContent, index):
        formatStr = '%s\t%s\t%s\t%s\t%s\t%s\t%s\n'

        reviewlist = ajaxContent.comments

        book = open(os.path.join(self.bookname, str(index) + '.txt'), 'w')

        for review in reviewlist:
            title = review.title
            rating = review.score
            content = review.content
            author = review.nickname
            time = review.creationTime
            province = review.userProvince
            userlevel = review.userLevelName
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

    def run(self):
        visited = set()
        cnt = 0

        userAgent = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        ]

        headers = {
            'User-Agent': random.choice(userAgent),
            'Accept': 'text/html;charset=GBK'
        }

        opener = urllib.request.build_opener()
        opener.addheaders = [headers]

        while self.queue:
            url = self.queue.popleft()
            visited |= {url}
            cnt += 1
            print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)

            # 避免程序异常中止, 用try..catch处理异常
            try:
                urlop = opener.open(url)
                data = urlop.read().decode('GBK')
                # print(data)
                print(re.findall(r'(?<=\()\S*(?=\))', str(data)))
                self.extract_and_save(data, cnt)
            except HTTPError as e:
                if e.code == 408:
                    print('timeout occurs,sleep 60s')
                    time.sleep(60)
                continue
            except Exception as e:
                print(e)

        self.combineFiles('*.txt')
        self.dispose()


jdcrawl = JDCrawl(
    '解忧杂货铺',
    'https://club.jd.com/comment/skuProductPageComments.action?productId=11452840&score=0&sortType=3&page=%d&pageSize=10&isShadowSku=0&callback=fetchJSON_comment98vv61564',
    1)

jdcrawl.run()
