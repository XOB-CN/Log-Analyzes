# -*- coding:utf-8 -*-
import re
from mod.tools import LogAnalyze

def MSSQL_Report(queue1, queue2):

    # 初始化数据
    n = True
    log_line = 0

    # 初始化分析数据
    memory_paged_out = {'type':'memory', 'title':'内存不足', 'content':"A significant part of sql server process memory has been paged out"}

    while n:
        line = queue1.get()

        if line == False:
            n = False

        else:
            log_line += 1

            # 内存不足
            if LogAnalyze("A significant part of sql server process memory has been paged out", line).log_regex():
                # 该事件对应的日记行数
                tmp_log_line = memory_paged_out.get('log_line')
                if tmp_log_line == None:
                    memory_paged_out['log_line'] = str(log_line)
                else:
                    memory_paged_out['log_line'] = tmp_log_line + ', ' + str(log_line)



    print(memory_paged_out)
