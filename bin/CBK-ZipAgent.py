# -*- coding:utf-8 -*-

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..')))

from mod.tools import ZipCheck, Message
from mod.rules import ZipRules_ConnectedBackup_Agent as CBK_Agent
from mod.input import zipfile_general

if __name__ == '__main__':
    # 获取输入的参数
    input_args = ZipCheck.get_input_args()

    # 如果参数正确，则继续执行
    if input_args[0]:
        filename = input_args[1].get('-f')
        if os.path.exists(filename):
            encoding = ZipCheck.get_encoding(filename)
        else:
            Message.error_message('没有这个文件，请检查后重新输入')
    else:
        Message.error_message(input_args[1])

    # 获取需要分析的文件列表
    file_path_list = ZipCheck.check_zipfile(filename, CBK_Agent.ZipAgentList)
    # 解压压缩包, 获取解压路径
    unzip_path = ZipCheck.unzip(filename)
    # 获取需要分析文件列表的绝对路径
    file_abspath_list= ZipCheck.get_abspath_list(unzip_path, file_path_list)

    # 启动多进程，开始分析日记
    zipfile_general(file_abspath_list, 'queue')