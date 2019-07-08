# -*- coding:utf-8 -*-

import pymongo
from datetime import datetime
from mod.tools.check import Check
from mod.tools.io_mongo import MongoDB

def add_to_mongodb(Queue_Output, input_argv):
    # 初始化变量
    n = True
    false_number = Check.get_multiprocess_counts() - 1
    false_number_count = 0

    if input_argv.get('-db_name') == None:
        db_name = datetime.now().strftime('%Y%m%d%H%M%S')
    else:
        db_name = input_argv.get('-db_name')

    if input_argv.get('-col_name') == None:
        cl_name = 'system_txt'
    else:
        cl_name = input_argv.get('-col_name')

    # 实例化一个 MongoDB 的 session 类
    mongo = MongoDB()

    # 创建一个 MongoDB 的数据库会话链接, 准备插入数据
    mg_sess = mongo.get_mongo_sess(db_name, cl_name)

    # 循环从 Queue_Output 中获取数据
    while n:
        mongo_data = Queue_Output.get()
        if mongo_data == False:
            false_number_count += 1
            if false_number_count == false_number:
                n = False
        else:
            # 将数据写入到 MongoDB 中
            mg_sess.insert_many(mongo_data)