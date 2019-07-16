# -*- coding:utf-8 -*-

import os
from datetime import datetime
from mod.tools.check import Check
from mod.tools.io_mongo import MongoDB
from mod.tools.io_tools import delete_directory
from mod.tools.message import Message
msg = Message()

def add_to_mongodb(Queue_Output, input_argv, unarchive_path):
    # 初始化变量
    n = True
    false_number = Check.get_multiprocess_counts() - 1
    false_number_count = 0
    insert_number = 0

    if input_argv.get('-db_name') == None:
        db_name = datetime.now().strftime('%Y%m%d%H%M%S')
    else:
        db_name = input_argv.get('-db_name')

    if input_argv.get('-col_name') == None:
        cl_name = 'default'
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
            # 显示进度信息
            insert_number += 1
            msg.output_mongo_insert_info(insert_number)

    # 清除临时目录
    temp_path = os.path.join(os.path.abspath(os.path.join(os.path.realpath(__file__), '..\..\..\..')), Check.get_temp_path())
    # 代表分析的是压缩包，需要清空临时目录
    if temp_path == unarchive_path:
        delete_directory(unarchive_path)
    # 代表分析的是单独的文件，不需要执行此步骤
    else:
        pass

    # 待数据完全录入到 MongoDB 后, 返回 "数据库" 和 "集合" 的名字
    print('DB Name: ', db_name)
    print('CL Name: ', cl_name)