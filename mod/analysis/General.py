# -*- coding:utf-8 -*-

import re
from mod.tools import LogAnalyze
from mod.tools import Messages

def General_Report_LogAnalyze(queue1, queue2, RuleList):
    # 初始化数据
    n = True
    log_line = 0

    # 多行匹配参数
    rule_index = 0
    end_match = False
    mul_match = False

    # 加载匹配规则
    rules_list = RuleList

    # 读取日记信息
    while n:
        line = queue1.get()
        if line == False:
            n = False
        else:
            log_line += 1

        # 显示目前已经分析的行数
        if log_line % 10000 == 0:
            Messages.pop_info('正在分析：第 {} 行'.format(log_line))

    # 循环匹配
        for rule in rules_list:
            # 如果发现日记内容是False,直接退出for循环
            if line == False:
                break

            # 进行多行匹配
            elif mul_match:
                # 代表第一次匹配到 endmatch 中的内容
                if LogAnalyze(rules_list[rule_index].get('endmatch'),line).log_regex() and end_match == False:
                    end_match = True
                    tmp_log_line = rules_list[rule_index].get('log_line')
                    rules_list[rule_index]['log_line'] = tmp_log_line + ', ' + str(log_line)
                    rules_list[rule_index]['detail'] = rules_list[rule_index]['detail'] + "<br>" + "[" + str(log_line) + "]" + " " + line.strip()
                    break

                # 代表数次匹配到 endmatch 中的内容
                elif LogAnalyze(rules_list[rule_index].get('endmatch'),line).log_regex() and end_match == True:
                    tmp_log_line = rules_list[rule_index].get('log_line')
                    rules_list[rule_index]['log_line'] = tmp_log_line + ', ' + str(log_line)
                    rules_list[rule_index]['detail'] = rules_list[rule_index]['detail'] + "<br>" + "[" + str(log_line) + "]" + " " + line.strip()
                    break

                # 代表还没有匹配到 endmatch, 但是多行匹配已经开启
                elif LogAnalyze(rules_list[rule_index].get('endmatch'), line).log_regex() == False and end_match == False:
                    tmp_log_line = rules_list[rule_index].get('log_line')
                    rules_list[rule_index]['log_line'] = tmp_log_line + ', ' + str(log_line)
                    rules_list[rule_index]['detail'] = rules_list[rule_index]['detail'] + "<br>" + "[" + str(log_line) + "]" + " " + line.strip() + 'cc'
                    break

                # 代表上一行已经是该事件的最后一行，本行进入单行匹配模式
                elif LogAnalyze(rules_list[rule_index].get('endmatch'),line).log_regex() == False and end_match == True:
                    mul_match = False
                    end_match = False

            # 开启多行匹配
            elif LogAnalyze(rule.get('match'),line).log_regex() and rule.get('endmatch') != None:
                mul_match = True
                rule_index = rules_list.index(rule)

                tmp_log_line = rule.get('log_line')
                if tmp_log_line == None:
                    rule['log_line'] = str(log_line)
                    rule['detail'] = "[" + str(log_line) + "]" + " " + line.strip()
                    break
                else:
                    rule['log_line'] = tmp_log_line + ', ' + str(log_line)
                    rule['detail'] = rule['detail'] + "<br>" + "[" + str(log_line) + "]" + " " + line.strip()
                    break

            # 单行匹配流程
            elif LogAnalyze(rule.get('match'),line).log_regex():

                # 特殊规则：仅搜集信息
                if rule.get('type') == 'Information' or rule.get('type') == 'Others':
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