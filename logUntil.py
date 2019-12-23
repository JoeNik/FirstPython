# coding:utf-8

import logging

import logging.handlers
import re

import time

import os

class logs(object):

    def __init__(self):

        self.logger = logging.getLogger("")

        # 设置输出的等级

        LEVELS = {'NOSET': logging.NOTSET,

                  'DEBUG': logging.DEBUG,

                  'INFO': logging.INFO,

                  'WARNING': logging.WARNING,

                  'ERROR': logging.ERROR,

                  'CRITICAL': logging.CRITICAL}

        # 创建文件目录

        #logs_dir = sys.path[0] + "\\logs\\"
        logs_dir = os.getcwd() + "\\logs\\"

        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):

            pass

        else:

            os.mkdir(logs_dir)

        # 修改log保存位置

        timestamp = time.strftime("%Y-%m-%d", time.localtime())

        logfilename = '%s.txt' % timestamp

        logfilepath = os.path.join(logs_dir, logfilename)
        #参考 https://blog.csdn.net/ashi198866/article/details/46725813
        # RotatingFileHandler
        # log_file_handler = TimedRotatingFileHandler(filename="ds_update", when="M", interval=2, backupCount=2)
        # “S”: Seconds
        # “M”: Minutes
        # “H”: Hours
        # “D”: Days
        # “W”: Week day(0 = Monday) “midnight”: Roll over at midnight
        rotatingFileHandler = logging.handlers.TimedRotatingFileHandler(filename=logs_dir+"Run.log", when="D",
                                                                        interval=1,
                                                                        backupCount=2)
        rotatingFileHandler.suffix = "%Y-%m-%d.log"
        rotatingFileHandler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}.log$")
        # rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=logfilepath,
        #
        #                                                            maxBytes=1024 * 1024 * 50,
        #
        #                                                            backupCount=5)

        # 设置输出格式

        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')

        rotatingFileHandler.setFormatter(formatter)

        # 控制台句柄

        console = logging.StreamHandler()

        # 设置级别
        console.setLevel(logging.INFO)

        console.setFormatter(formatter)

        # 添加内容到日志句柄中

        self.logger.addHandler(rotatingFileHandler)

        self.logger.addHandler(console)

        self.logger.setLevel(logging.INFO)

    def info(self, message):

        self.logger.info(message)

    def debug(self, message):

        self.logger.debug(message)

    def warning(self, message):

        self.logger.warning(message)

    def error(self, message):

        self.logger.error(message)

# if __name__ == '__main__':
#     logger = logs()
#
#     logger.info("this is info")
#
#     logger.debug("this is debug")
#
#     logger.error("this is error")
#
#     logger.warning("this is warning")
