# -*- coding:utf-8 -*-

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..')))

from mod.tools import Check, Input, Message
from multiprocessing import Queue, Process, Pool

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
    p1 = Process(target=Input.input_single_general, args=(filename, encoding, Q1), name='Input-Process')

    for p in range(Check.get_multiprocess_counts()-1):
        print(p)