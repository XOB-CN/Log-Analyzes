# -*- coding:utf-8 -*-

import os, sys
basepath = os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..'))
sys.path.append(basepath)

from mod.tools.message import Message
msg = Message()

from rules import Fortify_WIE_InputRules as WIE_In_Rules
from rules import Fortify_WIE_AnalysisRules as WIE_Alysis_Rules
from mod.tools.check import Check, ArchiveCheck
from mod.input.general import archive_general
from mod.output.report.general import archive_to_report
from mod.analysis.general import archive_general_report

from multiprocessing import Queue, Process

if __name__ == '__main__':
    # 获取输入的参数
    input_argv= Check.get_input_args()
    if input_argv == 'cmd_help':
        msg.general_help_command()
    # 检查文件是否存在
    filepath = input_argv.get('-f')
    if os.path.exists(filepath) == False:
        msg.general_file_error()

    # 检查输出方法
    if input_argv.get('-out') not in ['report','Report']:
        msg.general_output_error()

    # 执行到此，参数没有问题，继续过滤压缩包中的内容
    file_path_dict = ArchiveCheck.check_archive(filepath, WIE_In_Rules.need_files)
    # 解压压缩包，获取解压路径
    unarchive_path = ArchiveCheck.unarchive(filepath, basepath)
    # 获取需要分析文件列表的绝对路径
    file_abspath_dict = ArchiveCheck.get_abspath_dict(unarchive_path, file_path_dict)

    # 生成多进程需要的数据
    InputRule = {}
    InputRule['match_start'] = WIE_In_Rules.match_start
    InputRule['match_any'] = WIE_In_Rules.match_any
    InputRule['match_end'] = WIE_In_Rules.match_end
    ruleldict = {}
    ruleldict['logs'] = WIE_Alysis_Rules.log_rules_list
    ruleldict['other'] = WIE_Alysis_Rules.other_rule_list

    # 启动子进程并进行日志分析
    Queue_Input = Queue()
    Queue_Output = Queue()
    Queue_Control = Queue()

    if input_argv.get('-out') in ['report','Report']:
        p1 = Process(target=archive_general, args=(file_abspath_dict, Queue_Input, InputRule, input_argv), name='Input Process')
        p2 = Process(target=archive_to_report, args=(Queue_Output, ruleldict, input_argv, unarchive_path), name='Output Process')
        p1.start()
        p2.start()

        for p in range(Check.get_multiprocess_counts()-1):
            p = Process(target=archive_general_report, args=(Queue_Input, ruleldict, Queue_Output, WIE_In_Rules.black_list))
            p.start()