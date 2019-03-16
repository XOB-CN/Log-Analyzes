# -*- coding:utf-8 -*-

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..')))

from mod.tools.check import Check
from mod.tools.message import Message

from multiprocessing import Queue, Process

if __name__ == '__main__':
    # 获取输入的参数
    input_args= Check.get_input_args()
    msg = Message()
    msg.info_general_help()
