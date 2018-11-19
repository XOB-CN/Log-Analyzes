# -*- coding:utf-8 -*-

import re
import pymysql

# 输入端部分
class Input(object):
    """
    此类作用为检查用户输入的参数是否正确
    """
    def __init__(self, input_list):
        self.input_list = input_list

    # 判断输出端是否是 csv
    def chk_csv(self):
        have_f = '-f' in self.input_list
        have_out = '-out' in self.input_list
        try:
            have_f_data = self.input_list[self.input_list.index('-f') + 1]
            have_out_data = self.input_list[self.input_list.index('-out') + 1] == 'csv'
        except:
            return False

        # 此处不等于 0 的原因是因为第一个参数永远是文件本身，所以参数个数肯定是奇数
        return have_f and have_f_data and have_out and have_out_data and (len(self.input_list) %2 != 0)

    # 判断输出端是否是 mysql
    def chk_mysql(self):
        have_f = '-f' in self.input_list
        have_t = '-t' in self.input_list
        try:
            have_f_data = self.input_list[self.input_list.index('-f')+1]
            have_t_data = self.input_list[self.input_list.index('-t')+1]
        except:
            return False
        return have_f and have_t and have_f_data and have_t_data and (len(self.input_list) %2 != 0)

    # 判断输出端是否是 report
    def chk_report(self):
        have_f = '-f' in self.input_list
        have_out = '-out' in self.input_list
        try:
            have_f_data = self.input_list[self.input_list.index('-f') + 1]
            have_out_data = self.input_list[self.input_list.index('-out') + 1] == 'report'
        except:
            return False

        return have_f and have_f_data and have_out and have_out_data and (len(self.input_list) %2 != 0)

# 处理端部分
class LogAnalyze(object):
    """
    此类作用是判断日记属于什么规则，结果返回布尔值，匹配则返回 True，不匹配则返回 False
    """
    def __init__(self, rule, logline):
        self.rule = rule
        self.logline = logline

    # 从日记开头开始匹配，如果符合则返回 True
    def log_start(self):
        return self.logline[0:len(self.rule)] == self.rule

    # 从日记结尾开始匹配，如果符合则返回 True
    def log_end(self):
        return self.logline[-len(self.rule)-1:-1] == self.rule

    # 利用正则表达式来进行全局匹配，如果符合则返回 True
    def log_regex(self):
        return re.findall(self.rule, self.logline) != []

# 输出端部分
class Output(object):
    # 创建数据库
    @staticmethod
    def sql_set_database(hostname, username, password, database, port):
        db = pymysql.connect(hostname, username, password, port=port)
        cursor = db.cursor()
        # 判断数据库是否存在
        cursor.execute("show databases;")
        db_tuple = cursor.fetchall()
        db_name = (database,)
        if db_name not in db_tuple:
            cursor.execute(
                "create database if not exists " + "`" + database + "`" + " character set utf8 collate utf8_general_ci;")
        db.close()

    # 创建表，需要下方的模板
    @staticmethod
    def sql_set_table(hostname, username, password, database, port, tab_name, sql_table_func):
        db = pymysql.connect(hostname, username, password, database, port)
        cursor = db.cursor()
        # 判断表是否存在
        cursor.execute("show tables;")
        tb_tuple = cursor.fetchall()
        tb_name = (tab_name,)   # 注意此处是 tb_name 不是 tab_name!,如果出现创建表错误，可能是多进程的参数中添加了括号
        if tb_name not in tb_tuple:
            # sql_table_func 是模板名字
            cursor.execute(sql_table_func(tab_name))
        db.close()

class TemplateCSV(Output):
    # 输出端：csv 的 headers 模板
    @staticmethod
    def idol_query():
        return ['log_line', 'log_time', 'log_thid', 'host', 'action', 'action_id', 'status', 'finsh_time']

    @staticmethod
    def cbk_summary():
        return ['Agent_version', 'Agent_Type', 'Agent_account', 'log_line', 'Agent_action', 'Action_time', 'Action_status', 'Warnings', 'Errors', 'Diagnostics']

class TemplateMySQL(Output):
    # 输出端：MySQL的建表模板
    @staticmethod
    def idol_query(tab_name):
        return "create table if not exists " + "`" + tab_name + "`" + " (" \
               "`id` int not null auto_increment," \
               "`log_line` int," \
               "`log_time` datetime," \
               "`log_thid` varchar(6)," \
               "`host` varchar(128)," \
               "`action` text," \
               "`action_id` varchar(40)," \
               "`status` varchar(40)," \
               "`finsh_time` varchar(10)," \
               "primary key(id));"

    @staticmethod
    def cbk_summary(tab_name):
        return "create table if not exists " + "`" + tab_name + "`" + " (" \
               "`id` int not null auto_increment," \
               "`log_line` int," \
               "`Agent_version` varchar(10)," \
               "`Agent_type` varchar(3)," \
               "`Agent_account` varchar(11)," \
               "`Agent_action` varchar(25)," \
               "`Action_time` varchar(43)," \
               "`Action_status` varchar(25)," \
               "`Warnings` text," \
               "`Errors` text," \
               "`Diagnostics` text," \
               "primary key(id));"

# 提示信息部分
class Messages(object):

    @staticmethod
    def pop_help():
        print("\n"
              "To MySQL:\n"
              "-f   必须：指定要读取的文件名\n"
              "-t   必须：指定要保存的数据表的名字\n"
              "-u   可选：连接数据库的用户名\n"
              "-h   可选：连接数据库的主机\n"
              "-d   可选：需要创建的数据库名，默认为当前时间\n"
              "-p   可选：连接数据库的密码\n"
              "-P   可选：连接数据库的端口，默认为 3306\n"
              "-out 可选：指定要输出的地点，默认为 mysql\n\n"
              "To CSV:\n"
              "-f   必须：指定要读取的文件名\n"
              "-out 必须：指定要输出的地点，默认为 mysql，此处应该设定为 csv\n")
        exit()

    @staticmethod
    def pop_info(content):
        print(content)

    @staticmethod
    def pop_warn(content):
        print(content)

    @staticmethod
    def pop_error(content):
        print(content)
        exit(1)