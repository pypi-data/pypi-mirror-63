from re_common.baselibrary.utils.basehttpx import BaseHttpx
import  httpx
from re_common.baselibrary.utils.core.requests_core import USER_AGENT

def test_down():
    bshttpx = BaseHttpx()

    url = "http://www.baidu.com"

    HEADERS = {'Accept': '*/*',
               'Accept-Encoding': 'gzip, deflate',
               # 'Connection': 'keep-alive',
               'User-Agent': USER_AGENT,
               # 'Referer': 'http://epub.cnki.net/kns/brief/result.aspx?dbprefix=SMSD',
               # 'Host': 'kns.cnki.net',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}

    BoolResult, errString, r = bshttpx.base_sn_httpx(url=url,
                                                     proxies='',
                                                     headers=HEADERS,
                                                     )
    print(r)

def test_httpx():
    url = "http://www.baidu.com"
    proxies = {'http': 'http://192.168.30.176:8012', 'https': 'http://192.168.30.186:8012'}
    print(proxies)
    sn = httpx.Client(proxies=proxies)

    r = sn.get(url=url)
    with open("2.html",'w',encoding='utf-8')as f:
        f.write(r.text)

if __name__ == '__main__':
    test_down()
    # test_httpx()