# -*- coding:utf-8 -*-

import os
from mod.tools.check import Check
from mod.tools.debug import Debug
from mod.tools.io_tools import write_to_html, delete_directory
from mod.tools.message import Message
msg=Message()

@Debug.get_time_cost('[debug] 输出端 - 运行的总耗时：')
def archive_to_report(Queue_Output, ruleldict, input_argv, unarchive_path):
    """
    report 功能
    :param Queue_Output:从 Queue_Output 队列中获取分析后的数据
    :param ruleldict:加载分析规则列表
    :param input_argv:输入的参数字典
    :param unarchive_path:解压所在的临时路径
    :return:
    """
    # 初始化参数
    n = True
    false_number = Check.get_multiprocess_counts() - 1
    false_number_count = 0
    temp_data = {}
    finish_data_name = []
    finish_data = ruleldict.get('other') + ruleldict.get('logs')

    for dict in finish_data:
         finish_data_name.append(dict.get('name'))

    # 循环从 Queue_Output 中获取数据
    while n:
        log_data = Queue_Output.get()
        if log_data == False:
            false_number_count +=1
            if false_number_count == false_number:
                n = False
        else:
            temp_data[log_data.get('id')] = log_data.get('logs')

    # 开始 整理/合并 数据
    msg.output_integrate_info()
    for i in range(1,len(temp_data)+1):
        for data_dict in temp_data.get(i):
            # 如果 detail 不等于 None, 则代表已经获取了数据
            if data_dict.get('detail') != None:
                # 整理 type 为 Information 中的特殊记录
                if data_dict.get('type') == 'Information':
                    if finish_data[finish_data_name.index(data_dict.get('name'))].get('content') == None:
                        finish_data[finish_data_name.index(data_dict.get('name'))]['content'] = data_dict.get('content')
                    else:
                        finish_data[finish_data_name.index(data_dict.get('name'))]['content'] = finish_data[finish_data_name.index(data_dict.get('name'))]['content'] + '<br>' + data_dict.get('content')

                # 整理 log_line 中的记录
                if finish_data[finish_data_name.index(data_dict.get('name'))].get('log_line') == None:
                    finish_data[finish_data_name.index(data_dict.get('name'))]['log_line'] = data_dict.get('log_line')
                else:
                    finish_data[finish_data_name.index(data_dict.get('name'))]['log_line'] = finish_data[finish_data_name.index(data_dict.get('name'))]['log_line'] + '<br>' + data_dict.get('log_line')

                # 整理 detail 中的记录
                if finish_data[finish_data_name.index(data_dict.get('name'))].get('detail') == None:
                    finish_data[finish_data_name.index(data_dict.get('name'))]['detail'] = data_dict.get('detail')
                else:
                    finish_data[finish_data_name.index(data_dict.get('name'))]['detail'] = finish_data[finish_data_name.index(data_dict.get('name'))]['detail'] + '<br>' + data_dict.get('detail')
    # 数据合并结束
    msg.output_integrate_finish_info()

    # 将结果写入到 html 文件中
    write_to_html(finish_data, input_argv)

    # 清除临时目录
    temp_path = os.path.join(os.path.abspath(os.path.join(os.path.realpath(__file__), '..\..\..\..')), Check.get_temp_path())
    # 代表分析的是压缩包，需要清空临时目录
    if temp_path == unarchive_path:
        delete_directory(unarchive_path)
    # 代表分析的是单独的文件，不需要执行此步骤
    else:
        pass