# -*- coding:utf-8 -*-

import os, sys
basepath = os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..'))
sys.path.append(basepath)

from mod.tools.message import Message
msg = Message()

from rules import Fortify_SSC_InputRules as SSC_In_Rules
from rules import Fortify_SSC_AnalysisRules as SSC_Alysis_Rules
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

    # 检查输出方法
    if input_argv.get('-out') not in ['report', 'Report']:
        msg.general_output_error()

    # 检查文件是否存在
    filepath = input_argv.get('-f')
    if os.path.exists(filepath) == False:
        msg.general_file_error()

    # 过滤待分析的文件或压缩包
    file_abspath_dict, unarchive_path = Check.check_files(filepath, SSC_In_Rules.need_files, basepath)

    # 生成多进程需要的数据
    InputRule = {}
    InputRule['match_start'] = SSC_In_Rules.match_start
    InputRule['match_any'] = SSC_In_Rules.match_any
    InputRule['match_end'] = SSC_In_Rules.match_end
    ruleldict = {}
    ruleldict['logs'] = SSC_Alysis_Rules.log_rules_list
    ruleldict['other'] = SSC_Alysis_Rules.other_rule_list

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
            p = Process(target=archive_general_report, args=(Queue_Input, ruleldict, Queue_Output, SSC_In_Rules.black_list))
            p.start()