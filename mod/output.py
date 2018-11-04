# -*- coding:utf-8 -*-

import pymysql
from mod import tools

# 将获得的数据写入到指定的内容中
def to_mysql(arg_dict, queue, sql_table_func):
    n = True
    tab_name = arg_dict['tab_name']
    username = arg_dict['username']
    password = arg_dict['password']
    hostname = arg_dict['hostname']
    database = arg_dict['database']
    port = int(arg_dict['port'])

    # 准备需要使用的 database / table
    tools.sql_set_database(hostname, username, password, database, port)
    tools.sql_set_table(hostname, username, password, database, port, tab_name, sql_table_func)

    # 显示数据库信息
    tools.pop_info("DataBase Name: {}".format(database))

    # 连接数据库,准备录入数据
    db = pymysql.connect(hostname, username, password, database, port)
    cursor = db.cursor()

    while n:
        data_dict = queue.get()
        if data_dict == False:
            n = False
        else:
            # 生成 insert into 语句
            key_list = []
            val_list = []
            key_str = ''
            for k,v in data_dict.items():
                key_list.append(k)
                val_list.append(v)

            for i in key_list:
                key_str += i + ", "
            key_str = key_str[:-2]

            insert_key = " (" + key_str + ") "
            insert_val = " (" + str(val_list)[1:-1] + "); "
            insert_sql = "insert into " + tab_name + insert_key + "values" + insert_val

            # 插入数据
            try:
                cursor.execute(insert_sql)
                db.commit()
            except:
                tools.pop_warn("无法录入本条数据：{}".format(insert_sql))

    # 待数据全部插入后，关闭连接
    db.close()

# 将获得的数据写入到 csv 文件中
def to_csv(arg_dict, queue, headers):
    n = True
    while n:
        data_dict = queue.get()
        if data_dict == False:
            n = False
        else:
            print(data_dict)