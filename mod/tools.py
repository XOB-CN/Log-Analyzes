# -*- coding:utf-8 -*-

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
            print(have_f and have_f_data and have_out and have_out_data)
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

class Input(object):
    """输入端，读取日记内容，并进行预处理"""

    @staticmethod
    def input_single_general(filename, encoding, queue):
        """单一文件，不需要处理排序"""
        with open(filename, encoding=encoding) as f:
            for i in f:
                queue.put(i)

class Message(object):
    """信息类，显示各种提示信息"""

    @staticmethod
    def error_message(message):
        print(message)
        exit()