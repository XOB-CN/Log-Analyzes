# -*- coding:utf-8 -*-

from mod.tools import LogAnalyze
from mod.rules import Rules_Fortify_SCA

def SCA_Report(queue1, queue2):
    # 初始化数据
    n = True
    log_line = 0

    # 加载匹配规则
    rules_list = Rules_Fortify_SCA.RulesList

    # 读取日记信息
    while n:
        line = queue1.get()
        if line == False:
            n = False
        else:
            log_line += 1

    # 循环匹配
        for rule in rules_list:
            # 如果发现日记内容是False,直接退出for循环
            if line == False:
                break

            # 常规匹配：匹配关键字
            elif LogAnalyze(rule.get('keyword'),line).log_regex():
                # 特殊规则：搜集信息
                if rule.get('type') == 'Information':
                    pass

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