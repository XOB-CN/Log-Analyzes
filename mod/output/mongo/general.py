# -*- coding:utf-8 -*-

import pymongo
from mod.tools.check import Check

def add_to_mongodb(Queue_Output):

    # 设置初始变量
    n = True
    false_number = Check.get_multiprocess_counts() - 1
    false_number_count = 0

    # 循环从 Queue_Output 中获取数据
    while n:
        mongo_data = Queue_Output.get()
        if mongo_data == False:
            false_number_count += 1
            if false_number_count == false_number:
                n = False
        else:
            print(mongo_data)