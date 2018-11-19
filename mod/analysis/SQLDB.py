# -*- coding:utf-8 -*-
import re
from mod.tools import LogAnalyze
from mod.tools import TemplateReport

def MSSQL_Report(queue1, queue2):

    # 初始化数据
    n = True
    log_line = 0

    # 初始化分析数据
    memory_paged_out = {'type':'memory', 'info':'内存不足', 'keyword':"A significant part of sql server process memory has been paged out", 'solution':"添加内存或限制SQL内存使用量"}

    while n:
        line = queue1.get()

        if line == False:
            n = False

        else:
            log_line += 1

            # 内存不足
            if LogAnalyze("A significant part of sql server process memory has been paged out", line).log_regex():
                # 该事件对应的日记行数及内容
                tmp_log_line = memory_paged_out.get('log_line')
                if tmp_log_line == None:
                    memory_paged_out['log_line'] = str(log_line)
                    memory_paged_out['detail'] = "["+ str(log_line) +"]" + " " + line.strip()
                else:
                    memory_paged_out['log_line'] = tmp_log_line + ', ' + str(log_line)
                    memory_paged_out['detail'] = memory_paged_out['detail'] + "<br>" + "["+ str(log_line) +"]" + " " + line.strip()


    for i,v in memory_paged_out.items():
        if i == 'detail':
            print(TemplateReport.html_div(memory_paged_out[i],'log'))
