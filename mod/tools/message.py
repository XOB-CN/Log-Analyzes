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
        exit(0)

    def general_help_command(self):
        print(self.dsplay_language.general_help_command)
        exit(0)

    def general_no_function(self):
        print(self.dsplay_language.general_no_function)
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

    def archive_decompressing_info(self):
        print(self.dsplay_language.archive_decompressing_info)

    def archive_decompressing_error(self, err_content):
        print(self.dsplay_language.archive_decompressing_error)
        exit(1)

    def archive_decompression_finish_info(self):
        print(self.dsplay_language.archive_decompression_finish_info)

    def input_info(self, section_id):
        """根据 section_id 的数值来显示提示信息"""
        if section_id % Check.get_display_segments() == 0:
            print(self.dsplay_language.input_info.format(num=section_id))

    def input_warn(self, wrn_content):
        if Check.get_debug_level() in ['warn','debug']:
            print(self.dsplay_language.input_warn + wrn_content)

    def analysis_info(self, section_id):
        """根据 section_id 的数值来显示提示信息"""
        if section_id % Check.get_display_segments() == 0:
            print(self.dsplay_language.analysis_info.format(num=section_id))

    def analysis_content_warn(self, content):
        if Check.get_debug_level() in ['warn', 'debug']:
            print(self.dsplay_language.analysis_content_warn + content)

    def output_get_finish_info(self):
        print(self.dsplay_language.output_get_finish_info)

    def output_integrate_info(self):
        print(self.dsplay_language.output_integrate_info)

    def output_integrate_finish_info(self):
        print(self.dsplay_language.output_integrate_finish_info)

    def output_write_html_info(self):
        print(self.dsplay_language.output_write_html_info)

    def output_write_html_finish_info(self):
        print(self.dsplay_language.output_write_html_finish_info)

    def output_delete_info(self):
        print(self.dsplay_language.output_delete_info)

    def output_delete_finish_info(self):
        print(self.dsplay_language.output_delete_finish_info)

    def output_delete_warn(self, e):
        print(self.dsplay_language.output_delete_warn)
        print(str(e))
        exit(1)

    def output_graph_dbname_error(self):
        print(self.dsplay_language.output_graph_dbname_error)
        exit(1)