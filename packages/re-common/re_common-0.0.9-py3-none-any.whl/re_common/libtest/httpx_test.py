import os
import time

from bs4 import BeautifulSoup
from re_common.baselibrary.utils.basefile import BaseFile
from re_common.baselibrary.utils.basehttpx import BaseHttpx
from re_common.baselibrary.utils.baseurl import BaseUrl
from re_common.baselibrary.utils.core.requests_core import USER_AGENT
from re_common.baselibrary.utils.myredisclient import getDataFromRedis


from re_common.baselibrary.utils.core.mlamada import closeResult

def get_session():
    bshttpx = BaseHttpx()
    print(bshttpx.sn)
    print("******************")
    bshttpx.creat_sn(proxy="",
                     headers="")
    print(bshttpx.sn)
    print("*************")
    url = "https://www.ip.cn/"
    BoolResult, errString, r = bshttpx.base_sn_httpx(url,
                                                     bshttpx.sn)
    print(r.text)
if __name__ == '__main__':
    get_session()

