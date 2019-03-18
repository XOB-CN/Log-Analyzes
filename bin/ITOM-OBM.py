# -*- coding:utf-8 -*-

import os, sys
basepath = os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..'))
sys.path.append(basepath)

from mod.tools.message import Message
msg = Message()

from rules.ITOM_OBM_InputRules import need_files
from mod.tools.check import Check, ArchiveCheck
from mod.input.general import archive_general

from multiprocessing import Queue, Process

if __name__ == '__main__':
    # 获取输入的参数
    input_argv= Check.get_input_args()
    if input_argv == 'cmd_help':
        msg.general_help()
    # 检查文件是否存在
    filepath = input_argv.get('-f')
    if os.path.exists(filepath) == False:
        msg.general_file_error()
    # 检查输出方法
    if input_argv.get('-out') not in ['report','Report']:
        msg.general_output_error()

    # 执行到此，参数没有问题，继续过滤压缩包中的内容
    file_path_dict = ArchiveCheck.check_archive(filepath, need_files)
    # 解压压缩包，获取解压路径
    unarchive_path = ArchiveCheck.unarchive(filepath, basepath)
    # 获取需要分析文件列表的绝对路径
    file_abspath_dict = ArchiveCheck.get_abspath_dict(unarchive_path, file_path_dict)

    # 启动子进程并进行日志分析
    Queue_Input = Queue()
    Queue_Output = Queue()
    Queue_Control = Queue()

    if input_argv.get('-out') in ['report','Report']:
        p1 = Process(target=archive_general, args=(file_abspath_dict, Queue_Input), name='InputProcess')
        #p2 = Process()
        p1.start()
        #p2.start()