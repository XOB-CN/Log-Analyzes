# -*- coding:utf-8 -*-

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..')))

from rules.ITOM_OBM_InputRules import need_files
from mod.tools.check import Check, ArchiveCheck
from mod.tools.message import Message
msg = Message()

from multiprocessing import Queue, Process

if __name__ == '__main__':
    # 获取输入的参数
    input_argv= Check.get_input_args()

    # 检查文件是否存在
    filepath = input_argv.get('-f')
    if os.path.exists(filepath) == False:
        msg.general_file_error()
    # 检查输出方法
    if input_argv.get('-out') not in ['report','Report']:
        msg.general_output_error()

    # 执行到此，参数没有问题，继续过滤压缩包中的内容
    file_path_list = ArchiveCheck.check_archive(filepath, need_files)
    if file_path_list == {'logs':[], 'other':[]}:
        msg.general_no_need_file()