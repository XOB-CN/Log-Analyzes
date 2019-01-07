# -*- coding:utf-8 -*-

import re
import os, sys
import chardet

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..','config.cfg')), encoding='utf-8')

class Check(object):
    """检查类，主要判断各个参数是否正确以及获取各种配置参数"""

    @staticmethod
    def get_input_args():
        """
        获取并判断输入的参数是否正确，并给出相应的返回值;
        如果参数输入正确，则返回 Ture 以及对应的参数;
        如果参数输入错误，则返回 False 以及错误的信息;
        """
        check_list = ['-f','-t','-out','-detail']
        argv_dict = {}

        if len(sys.argv) %2 == 0:
            return [False, '参数个数不正确，请检查后重新输入']

        for i in check_list:
            if i in sys.argv:
                index = sys.argv.index(i)
                argv_dict[i] = sys.argv[index+1]

        try:
            have_f = '-f' in sys.argv
            have_f_data = sys.argv[sys.argv.index('-f') + 1]
            have_out = '-out' in sys.argv
            have_out_data = sys.argv[sys.argv.index('-out') + 1]
        except:
            return [False, '缺少必须参数，请检查后重新输入']

        if have_f and have_f_data and have_out and have_out_data:
            return [True, argv_dict]
        else:
            print('缺少必须参数，请检查后重新输入')
            return [False, '缺少必须参数，请检查后重新输入']

    @staticmethod
    def get_encoding(filename):
        """获取文件编码"""
        if cfg.getboolean('base','auto_detect_encoding'):
            _varchar = b''
            with open(filename, 'rb') as f:
                for i in range(cfg.getint('base','detect_encoding_line')):
                    _varchar = _varchar + f.readline()
            return chardet.detect(_varchar)['encoding']
        else:
            return 'utf-8'

    @staticmethod
    def get_multiprocess_counts():
        """获取可以同时进行的进程数"""
        return cfg.getint('base','multiprocess_counts')

class LogAnalze(object):
    """分析类，判断日记属于什么规则，结果返回布尔值，匹配则返回 True，不匹配则返回 False"""

    @staticmethod
    def match_any(rule, logline):
        """利用正则表达式来进行全局匹配，如果符合则返回 True, 其中 re.I 代表大小写不敏感"""
        return re.findall(rule, logline, re.I) != []

    @staticmethod
    def match_start(rule, logline):
        """从日记开头开始匹配，如果符合则返回 True"""
        return logline[0:len(rule)] == rule

    @staticmethod
    def match_end(rule, logline, isInclsEnter=True):
        """从日记结尾开始匹配，如果符合则返回 True，默认匹配带换行符的"""
        if isInclsEnter:
            print(logline[-len(rule) - 1:-1])
            return logline[-len(rule) - 1:-1] == rule
        else:
            print(logline[-len(rule):])
            return logline[-len(rule):] == rule

class Output(object):
    """输出类，将数据输出到指定位置"""

    @staticmethod
    def write_to_html(data):
        """将数据写入到 html 文件中"""
        base_path = os.getcwd()
        print(Template_Report.html_template('日记分析结果','日记内容'))

class Template_Report(Output):
    """Report输出模板"""

    @staticmethod
    def html_template(title, content):
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                h2{font-weight:bold; text-align:center;}
                h3{font-size:18px; font-weight:bold;}
                .title{color:blue;}
                .log-line{font-size:12px;}
                .keyword{font-size:12px; color:red;}
                .detail{font-size:12px;}
            </style>
        </head>
        <body>
        {content}
        </body>
        </html>"""
        return html_content.format(title=title, content=content)

class Message(object):
    """信息类，显示各种提示信息"""

    @staticmethod
    def error_message(message):
        print(message)
        exit()