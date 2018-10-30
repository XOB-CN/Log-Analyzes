# -*- coding:utf-8 -*-
import re
from mod.tools import LogAnalyze

# ConnectedBackup 日记的处理模块
def CBK_ZipAgent_Summary(queue1, queue2):
    # 初始化
    n = True
    index_id = 1
    log_line = 0
    Is_Start = False
    Agent_events = {}
    Agent_list = [False, 'Warnings', 'Errors', 'Diagnostics']
    event_info = Agent_list[0]  # 与 Agent_list 配合使用，判断该行内容处于哪个事件内容

    # 从 queue1 获取日记，并开始分析
    while n:
        line = queue1.get()
        if line == False:
            n = False
        else:
            line = line.strip()+'\n'
            log_line += 1

            ################-账户信息-###################################################################################

            # 判断日记的开头是否是 'Account Number:'
            if LogAnalyze('Account Number:', line).log_start():
                Agent_account = line[16:-1]
                Agent_events[index_id] = {'Agent_account': Agent_account}

            # Agent Type 为 Mac
            elif LogAnalyze('Connected® Backup for Mac Agent Version:', line).log_start():
                Agent_type = 'Mac'
                Agent_version = (line.split(':')[-1]).strip()
                Agent_events[index_id] = {'Agent_version': Agent_version, 'Agent_Type': Agent_type}

            # Agent Type 为 PC
            elif LogAnalyze('Connected Backup/PC Agent Version:', line).log_start():
                Agent_type = 'PC'
                Agent_version = line.split(':')[-1][:(line.split(':')[-1]).index('(')].strip()
                Agent_events[index_id] = {'Agent_version': Agent_version, 'Agent_Type': Agent_type}

            ################-开头结束-###################################################################################

            # 判断日记的开头是否是 '----------' 并且 Is_start = False，是则代表事件的开始
            elif LogAnalyze('----------', line).log_start() and Is_Start == False:
                Is_Start = True
                Agent_events[index_id] = {'Agent_version': Agent_version, 'Agent_Type': Agent_type,
                                          'Agent_account': Agent_account, 'log_line': log_line}

            # 判断日记的开头是否是 '----------' 并且 Is_start = False，是则代表上一个事件的结束，以及下一个事件的开始
            elif LogAnalyze('----------', line).log_start() and Is_Start == True:
                event_info = Agent_list[0]  # 0 为 False
                queue2.put(Agent_events.pop(index_id))
                index_id += 1
                Agent_events[index_id] = {'Agent_version': Agent_version, 'Agent_Type': Agent_type,
                                          'Agent_account': Agent_account, 'log_line': log_line}

            ################-注册事件-###################################################################################

            # 判断日记的结尾是否是 'Account registration', 是则代表注册事件
            elif LogAnalyze('Account registration', line).log_end():
                Agent_events[index_id]['Agent_action'] = 'Account registration'
                Agent_events[index_id]['Action_time'] = str(
                    re.findall('\d+/\d+/\d+, \d+[.:]\d+ [AP]?M?.*- \d+/\d+/\d+, \d+[.:]\d+ [AP]?M?', line))[2:-2]

            # 判断日记的开头是否是 'Account registration outcome:'，是则代表注册事件结果
            elif LogAnalyze('Account registration outcome:', line).log_start():
                Agent_events[index_id]['Action_status'] = line[len('Account registration outcome: '):-1]

            ################-内部诊断-###################################################################################

            # 判断日记的结尾是否是 'Internal diagnostic', 是则代表内部诊断 -- Agent Type 为 Mac
            elif LogAnalyze('Internal diagnostic', line).log_end():
                Agent_events[index_id]['Agent_action'] = 'Internal diagnostic'
                Agent_events[index_id]['Action_time'] = line[:line.index('Internal')].strip()

            # 判断日记的开头是否是 '日期 - 日期', 是则代表内部诊断 -- Agent Type 为 PC，且不带 AM/PM
            elif LogAnalyze('\d+/\d+/\d+ \d+:\d+ - \d+/\d+/\d+ \d+:\d+$', line).log_regex():
                Agent_events[index_id]['Agent_action'] = 'Internal diagnostic'
                Agent_events[index_id]['Action_time'] = str(re.findall('\d+/\d+/\d+ \d+:\d+ - \d+/\d+/\d+ \d+:\d+$',line))[2:-2]

            # 判断日记的开头是否是 '日期 - 日期', 是则代表内部诊断 -- Agent Type 为 PC，且带 AM/PM
            elif LogAnalyze('\d+/\d+/\d+ \d+:\d+ [AP]M - \d+/\d+/\d+ \d+:\d+ [AP]M$', line).log_regex():
                Agent_events[index_id]['Agent_action'] = 'Internal diagnostic'
                Agent_events[index_id]['Action_time'] = str(re.findall('\d+/\d+/\d+ \d+:\d+ [AP]M - \d+/\d+/\d+ \d+:\d+ [AP]M$',line))[2:-2]

            # 判断日记的开头是否是 'Internal diagnostic',是则代表是内部诊断的结果
            elif LogAnalyze('Internal diagnostic outcome:', line).log_start():
                Agent_events[index_id]['Action_status'] = line[len('Internal diagnostic outcome: '):-1]

            ################-备份事件-###################################################################################

            # 判断日记的开头是否是 '日期 - 日期 Backup'，是则代表是 Backup 事件 -- Agent Type 为 Mac
            elif LogAnalyze('\d+/\d+/\d+, \d+[.:]\d+ [AP]?M?.*- \d+/\d+/\d+, \d+[.:]\d+ [AP]?M?.* Backup',
                            line).log_regex():
                Agent_events[index_id]['Agent_action'] = 'Backup'
                Agent_events[index_id]['Action_time'] = str(re.findall('\d+/\d+/\d+, \d+[.:]\d+ [AP]?M?.*- \d+/\d+/\d+, \d+[.:]\d+ [AP]?M?',line))[2:-2]

            # 判断日记的开头是否是 '日期 - 日期 Backup'，是则代表是 Backup 事件 -- Agent Type 为 PC
            elif LogAnalyze('\d+/\d+/\d+ \d+[.:]\d+ [AP]?M?.*- \d+/\d+/\d+ \d+[.:]\d+ [AP]?M?.* Backup',
                            line).log_regex():
                Agent_events[index_id]['Agent_action'] = 'Backup'
                Agent_events[index_id]['Action_time'] = str(re.findall('\d+/\d+/\d+ \d+[.:]\d+ [AP]?M?.*- \d+/\d+/\d+ \d+[.:]\d+ [AP]?M?',line))[2:-2].strip()

            # 判断日记的开头是否是 'Backup outcome:',是则代表是备份事件的结果
            elif LogAnalyze('Backup outcome:', line).log_start():
                Agent_events[index_id]['Action_status'] = line[len('Backup outcome: '):-1]

            ################-事件详情-###################################################################################

            # 进入 Warnings level，并读取其中的内容
            elif LogAnalyze('Warnings', line).log_start():
                event_info = Agent_list[1]

            # 进入 Errors level, 并读取其中的内容
            elif LogAnalyze('Errors', line).log_start():
                event_info = Agent_list[2]

            # 进入 Diagnostics level, 并读取其中的内容
            elif LogAnalyze('Diagnostics', line).log_start():
                event_info = Agent_list[3]

            # 确定为 Warnings 下的内容
            elif LogAnalyze('\d+/\d+/\d+,? \d+:\d+ [AP]?M? \D', line).log_regex() and event_info == Agent_list[1]:
                Agent_events[index_id]['Warnings'] = line

            # 确定为 Errors 下的内容
            elif LogAnalyze('\d+/\d+/\d+,? \d+:\d+ [AP]?M? \D', line).log_regex() and event_info == Agent_list[2]:
                Agent_events[index_id]['Errors'] = line

            # 确定为 Diagnostics 下的内容
            elif LogAnalyze('\d+/\d+/\d+,? \d+:\d+ [AP]?M? \D', line).log_regex() and event_info == Agent_list[3]:
                oldline = Agent_events[index_id].get('Diagnostics')
                if oldline == None:
                    newline = line
                else:
                    newline = str(oldline) + line
                Agent_events[index_id]['Diagnostics'] = newline

    # 将最后一个事件数据放入 queue2 中，最后在放入 False
    queue2.put(Agent_events.pop(index_id))
    queue2.put(False)