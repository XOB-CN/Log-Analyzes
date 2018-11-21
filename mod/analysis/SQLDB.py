# -*- coding:utf-8 -*-
import re
from mod.tools import LogAnalyze

def MSSQL_Report(queue1, queue2):

    # 初始化数据
    n = True
    log_line = 0
    EventID_No = {}
    EventID_Detail = False

    # 初始化分析数据
    memory_pageout = {'type':'Memory',
                      'info':'内存不足',
                      'keyword':"A significant part of sql server process memory has been paged out",
                      'solution':"添加内存或限制SQL内存使用量"}

    security_login = {'type':'Security',
                      'info':'登陆失败',
                      'keyword':"Login failed for user",
                      'solution':"请检查账户登陆相关的设置"}

    EventID_18056 = {
        'type':'EventID',
        'info':'The client was unable to reuse a session with SPID ***',
        'keyword':'Error: 18056',
        'solution':'''
            考虑增加 IIS 连接池大小<br>
            <a href="https://blog.csdn.net/yangzhawen/article/details/8209167">https://blog.csdn.net/yangzhawen/article/details/8209167</a>'''}

    EventID_26073 = {
        'type':'EventID',
        'info':'TCP connection closed',
        'keyword':'Error: 26073',
        'solution':'''
            <a href="https://support.microsoft.com/zh-cn/help/2491214/non-yielding-scheduler-error-and-sql-server-2008-or-sql-server-2008-r2">
            https://support.microsoft.com/zh-cn/help/2491214/non-yielding-scheduler-error-and-sql-server-2008-or-sql-server-2008-r2</a>'''}

    # 事件列表
    event_lists = [memory_pageout, security_login, EventID_18056, EventID_26073]

    while n:
        line = queue1.get()
        if line == False:
            n = False
        else:
            log_line += 1

            ################-内存部分-###################################################################################

            # 内存不足：memory_pageout
            if LogAnalyze(memory_pageout['keyword'], line).log_regex():
                # 该事件对应的日记行数及内容
                tmp_log_line = memory_pageout.get('log_line')
                if tmp_log_line == None:
                    memory_pageout['log_line'] = str(log_line)
                    memory_pageout['detail'] = "["+ str(log_line) +"]" + " " + line.strip()
                else:
                    memory_pageout['log_line'] = tmp_log_line + ', ' + str(log_line)
                    memory_pageout['detail'] = memory_pageout['detail'] + "<br>" + "["+ str(log_line) +"]" + " " + line.strip()

            ################-安全部分-###################################################################################

            # 登陆问题：security_login
            elif LogAnalyze(security_login['keyword'], line).log_regex():
                # 该事件对应的日记行数及内容
                tmp_log_line = security_login.get('log_line')
                if tmp_log_line == None:
                    security_login['log_line'] = str(log_line)
                    security_login['detail'] = "[" + str(log_line) + "]" + " " + line.strip()
                else:
                    security_login['log_line'] = tmp_log_line + ', ' + str(log_line)
                    security_login['detail'] = security_login['detail'] + "<br>" + "[" + str(log_line) + "]" + " " + line.strip()

            ################-EventID-###################################################################################

            # 会话被重置：EventID_18056
            elif LogAnalyze(EventID_18056['keyword'], line).log_regex():
                # 该事件对应的日记行数及内容
                tmp_log_line = EventID_18056.get('log_line')
                if tmp_log_line == None:
                    EventID_18056['log_line'] = str(log_line)
                    EventID_18056['detail'] = "[" + str(log_line) + "]" + " " + line.strip()
                else:
                    EventID_18056['log_line'] = tmp_log_line + ', ' + str(log_line)
                    EventID_18056['detail'] = EventID_18056['detail'] + "<br>" + "[" + str(log_line) + "]" + " " + line.strip()

                EventID_No = EventID_18056
                EventID_Detail = True

            # TCP连接关闭：EventID_26073
            elif LogAnalyze(EventID_26073['keyword'], line).log_regex():
                # 该事件对应的日记行数及内容
                tmp_log_line = EventID_26073.get('log_line')
                if tmp_log_line == None:
                    EventID_26073['log_line'] = str(log_line)
                    EventID_26073['detail'] = "[" + str(log_line) + "]" + " " + line.strip()
                else:
                    EventID_26073['log_line'] = tmp_log_line + ', ' + str(log_line)
                    EventID_26073['detail'] = EventID_26073['detail'] + "<br>" + "[" + str(log_line) + "]" + " " + line.strip()

                EventID_No = EventID_26073
                EventID_Detail = True

            ################-EventID Detail-############################################################################

            elif EventID_Detail:
                EventID_No['log_line'] = EventID_No['log_line'] + ', ' + str(log_line)
                EventID_No['detail'] = EventID_No['detail']+"<br>"+"[" + str(log_line) + "]" + " " + line.strip()
                EventID_Detail = False

            ############################################################################################################

    queue2.put(event_lists)
    queue2.put(False)