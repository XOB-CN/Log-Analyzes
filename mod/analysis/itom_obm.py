# -*- coding:utf-8 -*-

import re, os
from datetime import datetime
from mod.tools.match import Match

# test mode
from mod.tools.io_tools import delete_directory

def analysis_to_mongodb(Queue_Input, Queue_Output, black_list, dir_path):
    # 初始化参数
    n = True
    IsMuline = False
    tmp_list = []
    fin_list = []
    fin_data = []

    # 初始化数据变量
    file_type = None

    # 从 Queue 中获取数据
    while n:
        queue_data = Queue_Input.get()
        if queue_data == False:
            n = False
        else:
            # 如果获取的数据类型是 logs, 则进行进一步的处理
            # queue_data: {'section_id': id, 'type': 'log', 'filepath': filepath, 'log_content': [行数, 日志内容]}
            if queue_data.get('type') == 'logs':
                file_type = os.path.basename(queue_data.get('filepath')).split('.')[0]
                file_path = queue_data.get('filepath')

                # 对日志的事件进行整合和预处理, 生成预处理数据
                for line, log_content in queue_data.get('log_content'):
                    black_rule = True

                    # 黑名单规则
                    for blk_rule in black_list:
                        if Match.match_any(blk_rule, log_content):
                            black_rule = False

                    if black_rule == True and file_type not in []:
                        # 先将每行数据放入临时列表中
                        tmp_list.append({'log_line': line, 'log_content': log_content.strip()})
                        # 判断本行是否是事件的开头, 如果是, 则将本行内容从临时列表中弹出, 并放入到最终的列表中, 否则开启多行匹配
                        if re.findall('INF:|INFO|WRN:|WARN|ERR|DEBUG| - ', log_content):
                            fin_list.append(tmp_list.pop())
                            # 如果本行已经是事件的开始, 那么意味着上一个事件已经结束, 需要将数据进行合并
                            while IsMuline:
                                if len(tmp_list) > 0:
                                    try:
                                        dict = {'log_line': '', 'log_content': ''}
                                        for tmp_dict in tmp_list:
                                            dict['log_line'] = dict.get('log_line') + tmp_dict.get('log_line')
                                            dict['log_content'] = dict.get('log_content') + '\n' + tmp_dict.get('log_content')
                                        fin_list[-2]['log_line'] = fin_list[-2].get('log_line') + dict.get('log_line')
                                        fin_list[-2]['log_content'] = fin_list[-2].get('log_content') + dict.get('log_content')
                                        tmp_list.clear()
                                    except:
                                        IsMuline = False
                                else:
                                    IsMuline = False
                        else:
                            IsMuline = True

                # 对每行数据进行进一步的处理：fin_list
                # print(fin_list)
                for i in fin_list:
                    log_line = i.get('log_line')
                    log_content = i.get('log_content')
                    if len(log_line) > 10:
                        print(log_line)
                        print(file_type)
                        print(file_path)
                        print(log_content)



    # test mode
    delete_directory(dir_path)