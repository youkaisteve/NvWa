
def getCookiesFromHeaders(headers):
    '''从http响应中获取所有cookie'''
    cookies = list()
    for header in headers:
        if "Set-Cookie" in header:
            cookie = header[1].split(";")[0]
            cookies.append(cookie)
    return cookies


def getCookieStr(cookies):
    '''保存cookies'''
    cookieStr = ''
    for cookie in cookies:
        cookieStr += cookie + ";"
    return cookieStr


def getCookieValue(cookies, cookieName):
    '''从cookies中获取指定cookie的值'''
    for cookie in cookies:
        if cookieName in cookie:
            index = cookie.index("=") + 1
            value = cookie[index:]
            return value


def parseQueryString(queryString):
    '''解析查询串'''
    result = dict()
    strs = queryString.split("&")
    for s in strs:
        name = s.split("=")[0]
        value = s.split("=")[1]
        result[name] = value
    return result