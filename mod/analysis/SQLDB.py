# -*- coding:utf-8 -*-
import re
from mod.tools import LogAnalyze
from mod.rules.Rules_MSSQL import RulesList

def MSSQL_Report(queue1, queue2):
    # 初始化数据
    n = True
    log_line = 0
    EventID_Detail = False
    rules_index = 0

    # 加载匹配规则
    rules_list = RulesList

    # 读取日记信息
    while n:
        line = queue1.get()
        if line == False:
            n = False
        else:
            log_line += 1

        # 进行日记匹配
        for rule in rules_list:
            # 如果发现日记内容是False,直接退出for循环
            if line == False:
                break

            # 如果 EventID_Detail = Ture, 直接录入数据
            elif EventID_Detail == True:
                rules_list[rules_index]['log_line'] = rules_list[rules_index]['log_line'] + ', ' + str(log_line)
                rules_list[rules_index]['detail'] = rules_list[rules_index]['detail'] + "<br>" + "[" + str(log_line) + "]" + " " + line.strip()
                EventID_Detail = False
                break

            # 常规匹配：匹配关键字
            elif LogAnalyze(rule.get('match'),line).log_regex():
                # 特殊规则：EventID 的事件
                if rule.get('type') == 'EventID':
                    # 开启 EventID_Detail 的标记，准备记录下一行内容
                    EventID_Detail = True
                    # 记下此时生效的规则位置
                    rules_index = rules_list.index(rule)

                # 特殊规则：仅搜集信息
                elif rule.get('type') == 'Information' or rule.get('type') == 'Others':
                    cmd = rule.get('rule')
                    rule['content'] = eval(cmd).strip()

                # 常规匹配：记录内容
                tmp_log_line = rule.get('log_line')
                if tmp_log_line == None:
                    rule['log_line'] = str(log_line)
                    rule['detail'] = "[" + str(log_line) + "]" + " " + line.strip()
                else:
                    rule['log_line'] = tmp_log_line + ', ' + str(log_line)
                    rule['detail'] = rule['detail'] + "<br>" + "[" + str(log_line) + "]" + " " + line.strip()
                break

    queue2.put(rules_list)
    queue2.put(False)