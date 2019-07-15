# -*- coding:utf-8 -*-

import copy
import pandas as pd
import matplotlib.pyplot as plt
from mod.tools.io_mongo import MongoDB
from mod.tools.message import Message
msg = Message()

# 需要明确注册 matplotlib 转换器
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def summary_by_date(input_argv):
    """
    从 MongoDB 中获取数据, 并生成统计图表
    基于时间统计事件的比重
    """
    # 初始化参数
    db_name = input_argv.get('-db_name', None)
    col_name = input_argv.get('-col_name','default')
    # pandas 重采样的频率值, 默认为每小时
    _freq = input_argv.get('-freq', 'H')

    # 判断是否没有输入 db_name, 如果没有输入, 则终止程序继续执行
    if db_name == None:
        msg.output_graph_dbname_error()
    else:
        db_name = str(db_name)

    # 如果参数符合, 则从 MongoDB 中获取数据
    mongo = MongoDB()
    mongo_sess = mongo.get_mongo_sess(db_name, col_name)
    mongo_data = mongo_sess.find({'$or':[{'log_level':'WRN'},{'log_level':'ERR'}]})

    # 将获取的 mongodb 数据转换成 pandas 的数据
    pd_data = pd.DataFrame(list(mongo_data))
    del pd_data['_id']

    # 开始处理 pandas 数据
    full_data = pd_data.set_index('log_time')

    # 可选：基于时间进一步过滤数据
    if input_argv.get('-ge', False):
        full_data = full_data[full_data.index > input_argv.get('-ge')]
    if input_argv.get('-le', False):
        full_data = full_data[full_data.index < input_argv.get('-le')]

    full_data = full_data.log_weight.resample(_freq).sum()
    full_data = full_data[full_data.values > 0]

    # 生成图表：基于时间的事件权重（柱状图）
    plt.figure(figsize=(8,4))
    plt.title('Time Based Event Weight')
    plt.bar(full_data.index, full_data)
    plt.show()

def summary_by_count(input_argv):
    """
    从 MongoDB 中获取数据, 并生成统计图表
    基于组件统计事件的个数
    """
    # 初始化参数
    db_name = input_argv.get('-db_name', None)
    col_name = input_argv.get('-col_name','default')

    # 判断是否没有输入 db_name, 如果没有输入, 则终止程序继续执行
    if db_name == None:
        msg.output_graph_dbname_error()
    else:
        db_name = str(db_name)

    # 如果参数符合, 则从 MongoDB 中获取数据
    mongo = MongoDB()
    mongo_sess = mongo.get_mongo_sess(db_name, col_name)
    mongo_data = mongo_sess.find({'$or':[{'log_level':'WRN'},{'log_level':'ERR'}]})

    # 将获取的 mongodb 数据转换成 pandas 的数据
    pd_data = pd.DataFrame(list(mongo_data))
    del pd_data['_id']

    # 开始处理 pandas 数据
    tmp1_data = pd_data.set_index('log_time')

    # 可选：基于时间进一步过滤数据
    if input_argv.get('-ge', False):
        tmp1_data = tmp1_data[tmp1_data.index > input_argv.get('-ge')]
    if input_argv.get('-le', False):
        tmp1_data = tmp1_data[tmp1_data.index < input_argv.get('-le')]

    # 继续整理数据
    tmp2_data = tmp1_data['log_component']
    tmp3_data = copy.deepcopy(tmp2_data)
    full_data = tmp3_data.value_counts('log_component')

    # 生成时间字符串
    max_date = max(tmp2_data.index)
    min_date = min(tmp2_data.index)
    date_limit = ('{min_date} to {max_date}'.format(min_date=min_date, max_date=max_date))

    # 生成图表：基于时间的组件比重（柱状图）
    plt.figure(figsize=(8,4))
    plt.title('Time Base Component Event Percentage')
    plt.bar(full_data.index, full_data)
    plt.xlabel(date_limit)
    plt.show()