import os
import time

from bs4 import BeautifulSoup
from re_common.baselibrary.utils.basefile import BaseFile
from re_common.baselibrary.utils.baserequest import BaseRequest
from re_common.baselibrary.utils.baseurl import BaseUrl
from re_common.baselibrary.utils.core.requests_core import USER_AGENT
from re_common.baselibrary.utils.myredisclient import getDataFromRedis

import httpx
import  traceback
from re_common.baselibrary.utils.core.mlamada import closeResult
from re_common.baselibrary.utils.basehttpx import BaseHttpx

from basestep import BaseStep

HEADERS = {'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate',
           # 'Connection': 'keep-alive',
           'User-Agent': USER_AGENT,
           # 'Referer': 'http://epub.cnki.net/kns/brief/result.aspx?dbprefix=SMSD',
           'Host': 'kns.cnki.net',
           'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}


class DownPage(BaseStep):
    def __init__(self):
        super().__init__()



        self.ListSqls = []
        self.nPage = 1
        self.nCount = 0

        self.bshttpx = BaseHttpx()

        # self.bshttpx.creat_sn(proxy="192.168.30.176:8012",
        #                       headers="")



    def GetHome(self, NaviCode, Year, nLoop=1):
        self.bshttpx.creat_sn(proxy="192.168.30.176:8012",
                              headers="")
        bRetry = False
        if self.nPage != 1:
            nLoop = self.nPage
            bRetry = True


        url = r'http://kns.cnki.net/KNS/brief/result.aspx?dbprefix=SNAD'
        BoolResult, errString, r = self.bshttpx.base_sn_httpx(url,
                                                              self.bshttpx.sn
                                                              )

        print("111111111111111111111111111111%s" % BoolResult)
        if not BoolResult:
            # self.nPage = nLoop
            return False

        # 请求search
        url = r'http://kns.cnki.net/kns/request/SearchHandler.ashx?action='
        url += '&NaviCode=' + NaviCode
        url += '&catalogName=ZJCLS&ua=1.25&PageName=ASP.brief_result_aspx&DbPrefix=SNAD&DbCatalog=国家科技成果数据库&ConfigFile=SNAD.xml&db_opt=SNAD&db_value=国家科技成果数据库&his=0'
        BoolResult, errString, r = self.bshttpx.base_sn_httpx(url,
                                                              self.bshttpx.sn
                                                              )

        print("2222222222222222222222222222222222222222%s" % BoolResult)
        if not BoolResult:
            # self.nPage = nLoop
            return False
        # 请求年份
        url = 'http://kns.cnki.net/KNS/group/doGroupLeft.aspx?action=1&Param=ASP.brief_result_aspx%23SNAD/%u5E74/%u5E74%2Ccount%28*%29/%u5E74/%28%u5E74%2C%27date%27%29%23%u5E74%24desc/1000000%24/-/40/40000/ButtonView'
        url = 'http://kns.cnki.net/kns/group/doGroupLeft.aspx?' + \
              BaseUrl.urlencode(BaseUrl.urlQuery2Dict(url))

        BoolResult, errString, r = self.bshttpx.base_sn_httpx(url,
                                                              self.bshttpx.sn
                                                              )

        print("33333333333333333333333333333%s" % BoolResult)
        if not BoolResult:
            # self.nPage = nLoop
            return False
        with open('1.html','w',encoding='utf-8')as f:
            f.write(r.text)

        url = "http://kns.cnki.net/KNS/brief/brief.aspx?ctl=5d8f59fd-ac13-462e-aa2e-14b56d0ec4bd&dest=%E5%88%86%E7%BB%84%EF%BC%9A%E5%B9%B4%20%E6%98%AF%20{Year}&action=5&dbPrefix=SNAD&PageName=ASP.brief_result_aspx&Param=%E5%B9%B4+%3d+%27{Year}%27&SortType=%E5%B9%B4&ShowHistory=1&recordsperpage=50".format(
            Year=Year)
        while 1:
            BoolResult, errString, r = self.bshttpx.base_sn_httpx(url,
                                                                  self.bshttpx.sn
                                                                  )

            print("444444444444444444444444444444%s" % BoolResult)
            if not BoolResult:
                self.nPage = nLoop
                bRetry = True
                return False

            soup = BeautifulSoup(r.text, 'lxml')
            nextTag = soup.find('a', id='Page_next')
            checkTag = soup.find('input', id='CheckCode')
            if bRetry and nextTag:
                url = 'http://kns.cnki.net/kns/brief/brief.aspx' + \
                    nextTag.get('href')
                url = url.replace('curpage=2', 'curpage=%d' % nLoop)
                print('retry url:', url)
                bRetry = False
                continue
        

            if not checkTag:
                filePath = os.path.join(r'E:\re_common\re-common\re_common\libtest\bshttpx_session_test\test', NaviCode + '_' + Year + '_' + str(nLoop) + '.html')
                self.logger.info(filePath)
                BaseFile.single_write_wb_file(r.content,filePath)
                self.nCount += 1
                self.logger.info('已经下载了%d页目录' % self.nCount)
                self.logger.info('Time total:' + repr(time.time() - self.StartTime))

            if not nextTag:
                if checkTag:
                    print("验证码")
                    self.nPage = nLoop
                    bRetry = True
                else:
                    self.nPage = 1
                break

            url = 'http://kns.cnki.net/kns/brief/brief.aspx' + nextTag.get('href')
            nLoop += 1
        return not bRetry

    def run(self):
        # 获取命令行参数
        # sql = 'select classes,years from class_year'
        # for row in self.mysqlutils.SelectFromDBFetchOne(sql):
        #     while 1:
        #         self.set_one_proxy()
        #         print("***********%s**********%s"%(row[0], str(row[1])))
        #         bResult = self.GetHome(row[0], str(row[1]))
        #
        #         if bResult:
        #             break
        while True:
            bResult = self.GetHome('B024', '2007')
            if bResult:
                break


if __name__ == '__main__':
    DownPage().run()
