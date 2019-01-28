# -*- coding:utf-8 -*-

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..')))

from mod import input, output
from mod.tools import ArchiveCheck, Message
from mod.rules import InputRules_ITOM_OA as Input_ITOM_OA
from mod.rules import AnalysisRules_ITOM_OA as Analysis_ITOM_OA
from mod.analysis import itom_oa

from multiprocessing import Queue, Process

if __name__ == '__main__':
    # 获取输入的参数
    input_args = ArchiveCheck.get_input_args()

    # 如果参数正确，则继续执行
    if input_args[0]:
        filename = input_args[1].get('-f')
        if os.path.exists(filename):
            encoding = ArchiveCheck.get_encoding(filename)
        else:
            Message.error_message('没有这个文件，请检查后重新输入')
    else:
        Message.error_message(input_args[1])

    # 获取需要分析的文件列表
    file_path_list = ArchiveCheck.check_archive(filename, Input_ITOM_OA.Zip_File_list)
    if file_path_list == []:
        Message.error_message('没有需要分析的文件，请注意只接受标准的 ZipAgent 压缩包')
    # 解压压缩包, 获取解压路径
    unarchive_path = ArchiveCheck.unarchive(filename)
    # 获取需要分析文件列表的绝对路径
    file_abspath_list= ArchiveCheck.get_abspath_list(unarchive_path, file_path_list)

    # 启动多进程，开始分析日记
    Q1 = Queue()    # Q1 存放预处理的数据
    Q2 = Queue()    # Q2 存放已经处理完毕的数据

    if input_args[1].get('-out') in ['report','Report']:
        p1 = Process(target=input.archive_general, args=(file_abspath_list, Q1), name='Input-Process')
        p2 = Process(target=output.archive_to_report, args=(Q2, Analysis_ITOM_OA.match_rules_list, input_args[1], unarchive_path), name='Out-Process')    # input_args 数据格式： [True，字典数据]
        p1.start()
        p2.start()

        # 启动日记分析的多进程模块
        for number in range(ArchiveCheck.get_multiprocess_counts() - 1):
            number = Process(target=itom_oa.itom_oa_report, args=(Q1, Analysis_ITOM_OA.match_rules_list, Q2, Input_ITOM_OA.black_rule_list))
            number.start()

    else:
        Message.error_message('没有这个输出方法')
