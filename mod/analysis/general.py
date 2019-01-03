# -*- coding:utf-8 -*-

import re
from mod.tools import LogAnalze

def general_report(queue1, rulelist, queue2):
    # 初始化参数
    n = True

    # 多行匹配
    rule_index = 0
    end_match = False
    mul_match = False

    # 开始读取数据
    while n:
        queue_data = queue1.get()
        if queue_data == False:
            n = False
        else:
            for line in queue_data:
                print(line)
