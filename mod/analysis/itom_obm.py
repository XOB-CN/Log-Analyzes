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
            for i in queue_data:
                print(i)