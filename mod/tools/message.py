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

    def general_help(self):
        print(self.dsplay_language.general_help)
        exit(1)

    def general_input_error(self):
        print(self.dsplay_language.general_input_error)
        exit(1)

    def general_file_error(self):
        print(self.dsplay_language.general_file_error)
        exit(1)

    def general_output_error(self):
        print(self.dsplay_language.general_output_error)
        exit(1)

    def general_no_need_file(self):
        print(self.dsplay_language.general_no_need_file)
        exit(1)

    def archive_type_error(self):
        print(self.dsplay_language.archive_type_error)
        exit(1)