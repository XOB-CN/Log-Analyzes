# -*- coding:utf-8 -*-

import re
from mod.tools.match import Match

def to_mongodb(Queue_Input, Queue_Output):
    # 初始化参数
    n = True
    data_dict = {}
    log_section = None

    # 从 Queue 中获取数据
    while n:
        queue_data = Queue_Input.get()
        if queue_data == False:
            n = False
        else:
            # 如果获取的数据类型是 logs, 则进行进一步的处理
            if queue_data.get('type') == 'logs':
                filepath = queue_data.get('filepath')

                # 处理日志类型：如果文件路径包含 system.txt, 则 log_section 为 system.txt
                if Match.match_any('system.txt', filepath):
                    log_section = 'system.txt'

                # 处理日志内容
                for line, log_content in queue_data.get('log_content'):
                    print(line)
                    print(log_content.strip())

    # 分析结束, 放入 False
    Queue_Output.put(False)