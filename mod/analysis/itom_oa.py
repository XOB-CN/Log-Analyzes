# -*- coding:utf-8 -*-

import re
from datetime import datetime
from mod.tools.match import Match

def analysis_to_mongodb(Queue_Input, Queue_Output, black_list):
    # 初始化参数
    n = True
    IsMuline = False
    tmp_list = []
    fin_list = []
    fin_data = []

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

                # 判断是什么文件, 如果文件路径包含 system.txt, 则 log_type 为 system.txt
                if Match.match_any('system.txt', filepath):
                    log_type = 'system.txt'

                    # 对日志的事件进行整合和预处理, 生成预处理数据
                    for line, log_content in queue_data.get('log_content'):
                        black_rule = True

                        # 黑名单规则
                        for blk_rule in black_list:
                            if Match.match_any(blk_rule, log_content):
                                black_rule = False

                        if black_rule == True:
                            # 先将每行数据放入临时列表中
                            tmp_list.append({'log_line':line, 'log_content':log_content.strip()})
                            # 判断本行是否是事件的开头, 如果是, 则将本行内容从临时列表中弹出, 并放入到最终的列表中, 否则开启多行匹配
                            if re.findall('INF|WRN|ERR', log_content):
                                fin_list.append(tmp_list.pop())
                                # 如果本行已经是事件的开始, 那么意味着上一个事件已经结束, 需要将数据进行合并
                                while IsMuline:
                                    if len(tmp_list) > 0:
                                        dict = {'log_line':'','log_content':''}
                                        for tmp_dict in tmp_list:
                                            dict['log_line'] = dict.get('log_line') + tmp_dict.get('log_line')
                                            dict['log_content'] = dict.get('log_content') + '\n' + tmp_dict.get('log_content')
                                        fin_list[-2]['log_line'] = fin_list[-2].get('log_line') + dict.get('log_line')
                                        fin_list[-2]['log_content'] = fin_list[-2].get('log_content') + dict.get('log_content')
                                        tmp_list.clear()
                                    else:
                                        IsMuline = False
                            else:
                                IsMuline = True

                    # 对预处理的数据进行进一步的分析, 并生成符合 mongodb 的数据
                    for dict in fin_list:
                        # 获取需要的各项的值
                        log_type = log_type
                        log_file = log_file
                        log_line = dict.get('log_line')
                        log_time = dict.get('log_content').split(':',2)[-1].split('(')[0].split(': o')[0].strip()
                        log_time = Match.convert_time(log_time)
                        try:
                            log_level = dict.get('log_content').split(':')[1].strip()
                        except:
                            log_level = None
                        try:
                            log_component = dict.get('log_content').split(':')[5].split('(')[0].strip()
                        except:
                            log_component = None
                        try:
                            log_unknow1 = dict.get('log_content').split(':')[5].split('(')[1].strip()[:-2]
                        except:
                            log_unknow1 = None
                        if Match.match_any('PID: \d+', dict.get('log_content')):
                            log_detail = dict.get('log_content').split(':')[-2] + dict.get('log_content').split(':')[-1]
                        else:
                            log_detail = dict.get('log_content').split(':')[-1]
                        log_event_id = re.findall('\(.*?-\d+\)', log_detail)

                        # 生成单个 event 数据
                        tmp_data = {}
                        tmp_data['log_type'] = log_type
                        tmp_data['log_file'] = log_file
                        tmp_data['log_line'] = log_line
                        tmp_data['log_time'] = log_time
                        if log_level != None:
                            tmp_data['log_level'] = log_level
                        if log_component != None:
                            tmp_data['log_component'] = log_component
                        tmp_data['log_detail'] = log_detail
                        if log_unknow1 != None:
                            tmp_data['log_unknow1'] = log_unknow1
                        if log_event_id != []:
                            tmp_data['log_event_id'] = log_event_id

                        # 将数据放入最终的数据列表中
                        tmp_data_copy = tmp_data.copy()
                        fin_data.append(tmp_data_copy)
                        tmp_data.clear()

                    # 将数据放入到消息队列中
                    fin_data_copy = fin_data.copy()
                    Queue_Output.put(fin_data_copy)
                    fin_data.clear()

    # 分析结束, 放入 False
    Queue_Output.put(False)