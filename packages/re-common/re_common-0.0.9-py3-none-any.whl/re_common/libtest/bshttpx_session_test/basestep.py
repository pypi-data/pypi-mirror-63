import time

from re_common.baselibrary.utils.basedir import BaseDir
from re_common.baselibrary.utils.basefile import BaseFile
from re_common.baselibrary.utils.myredisclient import getDataFromRedis
from re_common.facade.mysqlfacade import MysqlUtiles
from re_common.facade.now import get_streamlogger


class BaseStep(object):

    def __init__(self):
        self.cur_path = BaseDir.get_file_dir_absolute(__file__)
        self.top_path = BaseDir.get_upper_dir(self.cur_path, -2)
        self.sPath = BaseFile.get_new_path(self.top_path, "download", "cnki_cg", "download")
        BaseDir.create_dir(self.sPath)
        self.year_html = BaseFile.get_new_path(self.sPath, 'year_html')
        self.subclass_html = BaseFile.get_new_path(self.sPath, 'subclass_html')
        BaseDir.create_dir(self.year_html)
        BaseDir.create_dir(self.subclass_html)

        self.configfile = BaseFile.get_new_path(self.cur_path, "db.ini")
        self.logger = get_streamlogger()

        self.mysqlutils = MysqlUtiles(self.configfile, "db", self.logger)
        self.proxyset = getDataFromRedis(self.configfile)
        self.StartTime = time.time()

        self.raw_path = BaseFile.get_new_path(self.sPath, 'Raw')
        BaseDir.create_dir(self.raw_path)

        self.db3_path = BaseFile.get_new_path(self.sPath, 'db3')
        BaseDir.create_dir(self.db3_path)
