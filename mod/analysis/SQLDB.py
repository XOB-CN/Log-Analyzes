# -*- coding:utf-8 -*-
import re
from mod.tools import LogAnalyze
from mod.tools import TemplateReport

def MSSQL_Report(queue1, queue2):

    # 初始化数据
    n = True
    log_line = 0

    # 初始化分析数据
    memory_pageout = {'type':'memory', 'info':'内存不足', 'keyword':"A significant part of sql server process memory has been paged out", 'solution':"添加内存或限制SQL内存使用量"}
    event_lists = [memory_pageout,]

    while n:
        line = queue1.get()

        if line == False:
            n = False

        else:
            log_line += 1

            # 内存不足
            if LogAnalyze("A significant part of sql server process memory has been paged out", line).log_regex():
                # 该事件对应的日记行数及内容
                tmp_log_line = memory_pageout.get('log_line')
                if tmp_log_line == None:
                    memory_pageout['log_line'] = str(log_line)
                    memory_pageout['detail'] = "["+ str(log_line) +"]" + " " + line.strip()
                else:
                    memory_pageout['log_line'] = tmp_log_line + ', ' + str(log_line)
                    memory_pageout['detail'] = memory_pageout['detail'] + "<br>" + "["+ str(log_line) +"]" + " " + line.strip()


    for i in event_lists:
        print(i['type'])
        print(i['info'])
        print(i['keyword'])
        print(i['solution'])
        print(i['log_line'])
        print(i['detail'])
