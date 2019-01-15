# -*- coding:utf-8 -*-

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..')))

from mod import input, output
from mod.tools import ZipCheck, Message
from mod.rules import InputRules_ConnectedBackup_Agent as Input_CBK_Agent
from mod.rules import AnalysisRules_ConnectedBackup_Agent as Analysis_CBK_Agent
from mod.analysis import connected_backup

from multiprocessing import Queue, Process

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
    file_path_list = ZipCheck.check_zipfile(filename, Input_CBK_Agent.ZipAgent_list)
    # 解压压缩包, 获取解压路径
    unzip_path = ZipCheck.unzip(filename)
    # 获取需要分析文件列表的绝对路径
    file_abspath_list= ZipCheck.get_abspath_list(unzip_path, file_path_list)

    # 启动多进程，开始分析日记
    Q1 = Queue()    # Q1 存放预处理的数据
    Q2 = Queue()    # Q2 存放已经处理完毕的数据

    if input_args[1].get('-out') in ['report','Report']:
        p1 = Process(target=input.zipfile_cbk_agent, args=(file_abspath_list, Q1), name='Input-Process')
        p2 = Process(target=output.mult_to_report, args=(Q2, Analysis_CBK_Agent.match_rules_list, input_args[1], unzip_path), name='Out-Process')    # input_args 数据格式： [True，字典数据]
        p1.start()
        p2.start()

        # 启动日记分析的多进程模块
        for number in range(ZipCheck.get_multiprocess_counts()-1):
            number = Process(target=connected_backup.cbk_agent_report, args=(Q1, Analysis_CBK_Agent.match_rules_list, Q2, Input_CBK_Agent.black_rule_list))
            number.start()

    else:
        Message.error_message('没有这个输出方法')
