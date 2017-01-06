import urllib.parse
import gzip
import json
import re
from http.client import HTTPConnection
from baidu.httputils import getCookiesFromHeaders, getCookieStr
import configparser
import requests

# 请求头
headers = dict()
headers["Connection"] = "keep-alive"
headers["Cache-Control"] = "max-age=0"
headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
headers[
    "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.107 Safari/537.36"
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Accept-Encoding"] = "gzip,deflate,sdch"
headers["Accept-Language"] = "zh-CN,zh;q=0.8"
headers["Cookie"] = ""

config = configparser.ConfigParser()
config.read('baidu/tieba.conf')


def login(account, password, tieba):
    '''登录'''
    headers["Host"] = "wappass.baidu.com"
    body = "username={0}&password={1}&submit=%E7%99%BB%E5%BD%95&quick_user=0&isphone=0&sp_login=waprate&uname_login=&loginmerge=1&vcodestr=&u=http%253A%252F%252Fwap.baidu.com%253Fuid%253D1392873796936_247&skin=default_v2&tpl=&ssid=&from=&uid=1392873796936_247&pu=&tn=&bdcm=3f7d51b436d12f2e83389b504fc2d56285356820&type=&bd_page_type="
    body = body.format(account, password)
    conn = HTTPConnection("wappass.baidu.com", 80)
    conn.request("POST", "/passport/login", body, headers)
    resp = conn.getresponse()
    # cookies = getCookiesFromHeaders(resp.getheaders())
    # config.set(account, 'cookie', urllib.parse.unquote(getCookieStr(cookies)))

    tbs, forum_id = getTbsAndforumId(tieba)
    config.set(tieba, 'tbs', tbs)
    config.set(tieba, 'kw', tieba)
    config.set(tieba, 'fid', forum_id)
    with open(r'baidu/tieba.conf', 'w') as configfile:
        config.write(configfile)
    # 登录成功会返回302
    return True if resp.code == 302 else False


tbsPattern = re.compile('"tbs":"\W*"')
forumPattern = re.compile('"forum_id":\d*')


def getTbsAndforumId(tieBaName):
    '''签到'''
    # 获取页面中的参数tbs
    queryStr1 = urllib.parse.urlencode({"kw": tieBaName})
    resp = requests.get("http://tieba.baidu.com/f", params=queryStr1, allow_redirects=False)
    html = resp.content.decode()
    return re.findall(r'\'tbs\': "\w*"', html)[0].split(':')[1].replace('"', ''), \
           re.findall(r'"forum_id":\d*', html)[0].split(':')[1]
