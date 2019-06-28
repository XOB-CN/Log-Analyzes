# -*- coding:utf-8 -*-

import re
from mod.tools.match import Match

def to_mongodb(Queue_Input, Queue_Output, black_list):
    # 初始化参数
    n = True
    log_section = None
    IsMuline = False
    Tmp_list = []

    # 从 Queue 中获取数据
    while n:
        queue_data = Queue_Input.get()
        if queue_data == False:
            n = False
        else:
            # 如果获取的数据类型是 logs, 则进行进一步的处理
            if queue_data.get('type') == 'logs':
                filepath = queue_data.get('filepath')
                log_file = filepath
                idx_number = 0

                # 判断是什么文件, 如果文件路径包含 system.txt, 则 log_type 为 system.txt
                if Match.match_any('system.txt', filepath):
                    log_type = 'system.txt'

                    # 继续处理日志的每一行内容
                    for line, log_content in queue_data.get('log_content'):
                        black_rule = True
                        print(IsMuline)

                        # 黑名单规则
                        for blk_rule in black_list:
                            if Match.match_any(blk_rule, log_content):
                                black_rule = False

                        if black_rule == True:
                            if IsMuline == True:
                                try:
                                    if len(log_content.split(':')[1].strip()) == 3:
                                        log_level = log_content.split(':')[1].strip()
                                        IsMuline = False
                                except:
                                    print(idx_number)
                                    pass

                            # 该行为事件的起始行, 则执行下列处理步骤
                            if IsMuline == False:
                                # 初始化变量
                                log_line = []
                                log_level = None
                                log_time = None
                                log_component = None
                                log_detail = None
                                log_event_id = []
                                log_unknow = None

                                # log_line 部分
                                log_line.append(line)

                                # log_level 部分
                                try:
                                    if len(log_content.split(':')[1].strip()) == 3:
                                        log_level = log_content.split(':')[1].strip()
                                        IsMuline = False
                                except:
                                    IsMuline = True
                                    pass

                                # log_time 部分
                                if IsMuline == False:
                                    try:
                                        log_time = log_content.split(':',2)[2].split(': ')[0]
                                    except:
                                        pass

                                # log_component / log_unkonw 部分
                                if IsMuline == False:
                                    try:
                                        tmp_log_component = log_content.split(':')[5]
                                        log_component = tmp_log_component.split('(')[0]
                                        log_unknow = tmp_log_component.split('(')[1][:-2]
                                    except:
                                        pass

                                # log_detail 部分
                                if IsMuline == False:
                                    log_detail = log_content.split(':')[-1]
                                    # 如果是以 PID: \d+ 结尾的, 则切分出来的则会是仅数字，为了防止这种情况，则需要调整切分策略
                                    if re.match(' \d+', log_detail) != None:
                                        log_detail = log_content.split(':',6)[-1]
                                else:
                                    log_detail = log_content.strip()

                                # log_event_id 部分
                                if Match.match_any('\(.*?\)', log_detail):
                                    log_event_id = re.findall('\(.*?-\d+\)', log_detail)

                                # 将获取的数据存入到临时的字典中
                                Tmp_list.append({'log_line':log_line,
                                                 'log_level':log_level,
                                                 'log_time':log_time,
                                                 'log_component':log_component,
                                                 'log_detail':log_detail,
                                                 'log_event_id':log_event_id,
                                                 'log_unknow':log_unknow})
                                idx_number += 1

                            # 该行不是事件的起始行，则需要执行下列处理步骤
                            if IsMuline == True:
                                print(idx_number)
                                log_detail = log_content.strip()
                                log_event_id = re.findall('\(.*?-\d+\)', log_detail)

                                # 存入数据
                                print(Tmp_list[idx_number-2])
                                print(Tmp_list[-1])
                                Tmp_list[idx_number-2]['log_level'] = 'INFO'
                                print(Tmp_list[idx_number-2])


                    # for dict in Tmp_list:
                    #     print(dict)

    # 分析结束, 放入 False
    Queue_Output.put(False)