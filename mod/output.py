# -*- coding:utf-8 -*-

import pymysql, os, csv
from mod import tools
from mod.tools import TemplateReport

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
    tools.Output.sql_set_database(hostname, username, password, database, port)
    tools.Output.sql_set_table(hostname, username, password, database, port, tab_name, sql_table_func)

    # 显示数据库信息
    tools.Messages.pop_info("DataBase Name: {}".format(database))

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
                tools.Messages.pop_warn("无法录入本条数据：{}".format(insert_sql))

    # 待数据全部插入后，关闭连接
    db.close()

# 将获得的数据写入到 csv 文件中
def to_csv(arg_dict, queue, headers):
    n = True
    data_list = []
    base_path = os.getcwd() # os.getcwd() --> 返回 shell 提示的当前目录
    file_path = os.path.join(base_path,(arg_dict['filename']+'_output.csv'))
    while n:
        data_dict = queue.get()
        if data_dict == False:
            n = False
        else:
            data_list.append(data_dict)

    # csv 格式需要添加一个 newline='' 参数，否则生成的 csv 文件每行数据都会有一个空行
    # 在 windows 这种使用 \r\n 的系统里，不用 newline='' 的话，会自动在行尾多添加个\r，导致多出一个空行，即行尾为\r\r\n
    with open(file_path, mode='a', encoding='utf-8', newline='') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(data_list)

    tools.Messages.pop_info("分析完成！")

# 将获得的数据写入到 report 中
def to_report(arg_dict, queue):
    n = True
    base_path = os.getcwd()  # os.getcwd() --> 返回 shell 提示的当前目录
    file_path = os.path.join(base_path, (arg_dict['filename'] + '_report.html'))
    event_title = set()
    event_types = [['Information','Information 部分'],
                   ['CPU','CPU 部分'],
                   ['Memory','Memory 部分'],
                   ['Disk','Disk 部分'],
                   ['Network','Network 部分'],
                   ['Permission','Permission 部分'],
                   ['Security','Security 部分'],
                   ['EventID','EventID 部分'],
                   ['Others','Others 部分']]

    # 创建 report 文件
    with open(file_path, mode='w', encoding='utf8', newline='') as f:
        # html 基本信息：开头
        f.writelines(TemplateReport.html_head())
        f.writelines(TemplateReport.html_css())
        f.writelines("<body>\n")

        # 写入日记具体的分析内容
        while n:
            data_dict = queue.get()
            if data_dict == False:
                n = False
            else:
                for dict in data_dict:
                    for type in event_types:
                        # type[0] 为匹配的类型，type[1] 为显示的信息 ---> 对应的变量为：event_types
                        if dict['type'] == type[0] and dict.get('log_line') != None:
                            TemplateReport.event_write(f, type[1], type[0], event_title, arg_dict, dict)

        # html 基本信息：结尾
        f.writelines("</body>\n</html>\n")

    tools.Messages.pop_info("分析完成！")