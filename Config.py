# -*- coding: UTF-8 -*_
import configparser
import os


class ReadConfig:
    fileName = "config.ini"
    """定义一个读取配置文件的类"""

    def __init__(self, filepath=None):
        if filepath:
            configpath = filepath
        else:
            #root_dir = os.path.dirname(os.path.abspath('.'))
            root_dir = os.getcwd()
            configpath = os.path.join(root_dir, self.fileName)
        self.cf = configparser.ConfigParser()
        self.cf.read(configpath)

    def get_val(self, section, param, val):
        try:
            value = self.cf.get(section, param)
            return value
        except Exception as e:
            if 'No section' in str(e):
                #root_dir = os.path.dirname(os.path.abspath('.'))
                root_dir = os.getcwd()
                configpath = os.path.join(root_dir, self.fileName)
                self.cf.add_section(section)
                self.cf.write(open(configpath, "w"))

        try:
            value = self.cf.get(section, param)
            return value
        except Exception as e:
            if 'No option' in str(e):
                #root_dir = os.path.dirname(os.path.abspath('.'))
                root_dir = os.getcwd()
                configpath = os.path.join(root_dir, self.fileName)
                self.cf.set(section, param, val)
                self.cf.write(open(configpath, "w"))

        try:
            value = self.cf.get(section, param)
            return value
        except Exception as e:
            return ""
