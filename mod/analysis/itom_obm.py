# -*- coding:utf-8 -*-

import re, os
from datetime import datetime
from mod.tools.match import Match

def analysis_to_mongodb(Queue_Input, Queue_Output, black_list):
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