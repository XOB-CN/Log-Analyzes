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

    tools.Messages.pop_info("Log analyzes had finsh!")

# 将获得的数据写入到 report 中
def to_report(arg_dict, queue):
    n = True
    base_path = os.getcwd()  # os.getcwd() --> 返回 shell 提示的当前目录
    file_path = os.path.join(base_path, (arg_dict['filename'] + '_report.html'))

    # 创建 report 文件
    with open(file_path, mode='a', encoding='utf8', newline='') as f:
        # html 头部信息
        f.writelines("<!DOCTYPE html>\n<html>")
        f.writelines(TemplateReport.html_head())
        # css 风格
        f.writelines(TemplateReport.html_css())
        # html 内容信息
        f.writelines("<body>\n")

        while n:
            data_dict = queue.get()
            if data_dict == False:
                n = False
            else:
                for dict in data_dict:
                    # CPU 部分内容
                    if dict['type'] == 'CPU'and dict['log_line'] != None:
                        # 标题部分
                        f.writelines(TemplateReport.html_h('CPU 部分问题', 2))
                        # 问题原因
                        f.writelines(TemplateReport.html_h('问题原因', 3))
                        f.writelines(TemplateReport.html_div(dict['info'], 'log-line'))
                        # 关键信息
                        f.writelines(TemplateReport.html_h('关键信息', 3))
                        f.writelines(TemplateReport.html_div(dict['keyword'], 'keyword'))
                        # 解决思路
                        f.writelines(TemplateReport.html_h('解决思路', 3))
                        f.writelines(TemplateReport.html_div(dict['solution'], 'log-line'))
                        # 对应行数
                        f.writelines(TemplateReport.html_h('对应行数', 3))
                        f.writelines(TemplateReport.html_div(dict['log_line'], 'log-line'))
                        # 详细信息
                        if arg_dict['detail'] in ['True','ture','On','on']:
                            f.writelines(TemplateReport.html_h('详细信息', 3))
                            f.writelines(TemplateReport.html_div(dict['detail'], 'detail'))

                    # Memory 部分内容
                    elif dict['type'] == 'Memory' and dict['log_line'] != None:
                        # 标题部分
                        f.writelines(TemplateReport.html_h('内存部分问题', 2))
                        # 问题原因
                        f.writelines(TemplateReport.html_h('问题原因', 3))
                        f.writelines(TemplateReport.html_div(dict['info'], 'log-line'))
                        # 关键信息
                        f.writelines(TemplateReport.html_h('关键信息', 3))
                        f.writelines(TemplateReport.html_div(dict['keyword'], 'keyword'))
                        # 解决思路
                        f.writelines(TemplateReport.html_h('解决思路', 3))
                        f.writelines(TemplateReport.html_div(dict['solution'], 'log-line'))
                        # 对应行数
                        f.writelines(TemplateReport.html_h('对应行数', 3))
                        f.writelines(TemplateReport.html_div(dict['log_line'], 'log-line'))
                        # 详细信息
                        if arg_dict['detail'] in ['True','ture','On','on']:
                            f.writelines(TemplateReport.html_h('详细信息', 3))
                            f.writelines(TemplateReport.html_div(dict['detail'], 'detail'))

        # html 结尾
        f.writelines("</body></html>\n")