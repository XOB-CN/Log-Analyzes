# -*- coding:utf-8 -*-

import re
import pymysql

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

# 定义错误消息
def pop_error(content):
    print(content)
    exit(1)

# 定义警告消息
def pop_warn(content):
    print(content)

# 定义要输出的消息
def pop_info(content):
    print(content)

# 创建数据库
def sql_set_database(hostname, username, password, database, port):
    db = pymysql.connect(hostname, username, password, port=port)
    cursor = db.cursor()
    # 判断数据库是否存在
    cursor.execute("show databases;")
    db_tuple = cursor.fetchall()
    db_name = (database,)
    if db_name not in db_tuple:
        cursor.execute("create database if not exists " + "`" + database + "`" + " character set utf8 collate utf8_general_ci;")
    db.close()

# 创建表，需要下方的模板
def sql_set_table(hostname, username, password, database, port, tab_name, sql_table_func):
    db = pymysql.connect(hostname, username, password, database, port)
    cursor = db.cursor()
    # 判断表是否存在
    cursor.execute("show tables;")
    tb_tuple = cursor.fetchall()
    tb_name = (tab_name,)
    if tb_name not in tb_tuple:
        # sql_table_func 是模板名字，下方的 sql_table_idol_query 就是其中的一个实际的模板
        cursor.execute(sql_table_func(tab_name))
    db.close()

# 模板，创建符合 IDOL-Query 的数据表
def sql_table_idol_query(tab_name):
    return "create table if not exists " + "`" + tab_name + "`" + " (" \
    "`id` int not null auto_increment," \
    "`log_line` int," \
    "`log_time` datetime," \
    "`log_thid` varchar(4)," \
    "`host` varchar(128)," \
    "`action` varchar(1024)," \
    "`action_id` varchar(40)," \
    "`status` varchar(40)," \
    "`finsh_time` varchar(10)," \
    "primary key(id));"