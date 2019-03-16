# -*- coding:utf-8 -*-

import locale

from mod.tools.check import Check
from mod.lang import Chinese, English

class Message(object):
    """信息类，显示各种提示信息"""
    system_language = locale.getdefaultlocale()[0]
    dsplay_language = English

    def __init__(self):
        """判断系统语言，根据系统语言来决定信息提示的语言"""
        if Check.get_display_language() == 'auto':
            if self.system_language == 'zh_CN':
                self.dsplay_language = Chinese

        else:
            ds_lang = Check.get_display_language()
            if ds_lang == 'zh_CN':
                self.dsplay_language = Chinese
            else:
                self.dsplay_language = English

    def info_general_help(self):
        """显示通用的帮助信息"""
        print(self.dsplay_language.general_help)
        exit(1)