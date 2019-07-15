# -*- coding:utf-8 -*-

import os, sys
basepath = os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..'))
sys.path.append(basepath)

from mod.tools.message import Message
msg = Message()

from rules import ITOM_OA_InputRules as OA_In_Rules
from rules import ITOM_OA_AnalysisRules as OA_Alysis_Rules
from mod.tools.check import Check, ArchiveCheck
from mod.input.general import archive_general
from mod.output.report.general import archive_to_report
from mod.output.mongo.general import add_to_mongodb
from mod.output.graph import graph_itom_oa
from mod.analysis.general import archive_general_report
from mod.analysis.itom_oa import analysis_to_mongodb

from multiprocessing import Queue, Process

if __name__ == '__main__':
    # 获取输入的参数
    input_argv= Check.get_input_args()
    if input_argv == 'cmd_help':
        msg.general_help_command()

    # 检查文件是否存在
    # 例外情况, 此情况下可以没有 -f 参数
    if input_argv.get('-out') in ['summary_by_time','summary_by_date','summary_by_count']:
        pass
    else:
        filepath = input_argv.get('-f')
        if os.path.exists(filepath) == False:
            msg.general_file_error()

    # 检查输出方法
    if input_argv.get('-out') not in ['report','Report','mongodb','MongoDB','mongoDB','summary_by_time','summary_by_date','summary_by_count']:
        msg.general_output_error()

    # 过滤待分析的文件或压缩包
    # 例外情况, 此情况下可以没有 -f 参数
    if input_argv.get('-out') in ['summary_by_time','summary_by_date','summary_by_count']:
        pass
    else:
        file_abspath_dict, unarchive_path = Check.check_files(filepath, OA_In_Rules.need_files, basepath)

    # 生成多进程需要的数据
    InputRule = {}
    InputRule['match_start'] = OA_In_Rules.match_start
    InputRule['match_any'] = OA_In_Rules.match_any
    InputRule['match_end'] = OA_In_Rules.match_end
    ruleldict = {}
    ruleldict['logs'] = OA_Alysis_Rules.log_rules_list
    ruleldict['other'] = OA_Alysis_Rules.other_rule_list

    # 启动子进程并进行日志分析
    Queue_Input = Queue()
    Queue_Output = Queue()
    Queue_Control = Queue()

    # 最终生成 Report 信息
    if input_argv.get('-out') in ['report','Report']:
        p1 = Process(target=archive_general, args=(file_abspath_dict, Queue_Input, InputRule, input_argv), name='Input Process')
        p2 = Process(target=archive_to_report, args=(Queue_Output, ruleldict, input_argv, unarchive_path), name='Output Process')
        p1.start()
        p2.start()

        for p in range(Check.get_multiprocess_counts()-1):
            p = Process(target=archive_general_report, args=(Queue_Input, ruleldict, Queue_Output, OA_In_Rules.black_list))
            p.start()

    # 将获取的数据最终写入到 MongoDB 中
    if input_argv.get('-out') in ['mongodb','MongoDB','mongoDB']:
        p1 = Process(target=archive_general, args=(file_abspath_dict, Queue_Input, InputRule, input_argv), name='Input Process')
        p2 = Process(target=add_to_mongodb, args=(Queue_Output,input_argv,), name='Output Process')
        p1.start()
        p2.start()

        for p in range(Check.get_multiprocess_counts()-1):
            p = Process(target=analysis_to_mongodb, args=(Queue_Input, Queue_Output, OA_In_Rules.black_list))
            p.start()

    # 生成统计图: summary_by_date / time
    if input_argv.get('-out') in ['summary_by_time','summary_by_date']:
        p = Process(target=graph_itom_oa.summary_by_date, args=(input_argv,))
        p.start()

    # 生产统计图：summary_by_count
    if input_argv.get('-out') in ['summary_by_count',]:
        p = Process(target=graph_itom_oa.summary_by_count, args=(input_argv,))
        p.start()