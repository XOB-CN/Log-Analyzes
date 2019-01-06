# -*- coding:utf-8 -*-

import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..')))

from mod import input, output
from mod.tools import Check, Message
from mod.analysis import general
from mod.rules import Rule_Microsoft_SQL_Server
from multiprocessing import Queue, Process, Pool

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..','config.cfg')), encoding='utf-8')

if __name__ == '__main__':
    # 获取输入的参数
    input_args = Check.get_input_args()

    # 如果参数正确，则继续执行
    if input_args[0]:
        filename = input_args[1].get('-f')
        if os.path.exists(filename):
            encoding = Check.get_encoding(filename)
        else:
            Message.error_message('没有这个文件，请检查后重新输入')
    else:
        Message.error_message(input_args[1])

    # 启动多进程来处理日记
    Q1 = Queue()    # Q1 存放预处理的数据
    Q2 = Queue()    # Q2 存放已经处理完毕的数据
    p1 = Process(target=input.single_general, args=(filename, encoding, Q1), name='Input-Process')
    p2 = Process(target=output.to_report, args=(Q2,), name='Out-Process')
    p1.start()
    p2.start()

    # 启动日记分析的多进程模块
    for number in range(cfg.getint('base','multiprocess_counts')-1):
        number = Process(target=general.general_report, args=(Q1, Rule_Microsoft_SQL_Server.RulesList, Q2)).start()