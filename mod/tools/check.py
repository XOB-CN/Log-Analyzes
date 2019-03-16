# -*- coding:utf-8 -*-

import os, sys

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..\..','config.cfg')), encoding='utf-8')

class Check(object):
    """检查类，主要判断各个参数是否正确以及获取各种配置参数"""

    @staticmethod
    def get_input_args():
        """
        获取并判断输入的参数是否正确，并给出相应的返回值;
        如果参数输入正确，则返回 Ture 以及对应的参数;
        如果参数输入错误，则返回 False 以及错误的信息;
        :return:
        """
        input_args = sys.argv
        return input_args

    @staticmethod
    def get_display_language():
        return cfg.get('system','display_language')

