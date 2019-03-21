# -*- coding:utf-8 -*-

from mod.tools.check import Check
from mod.tools.io_tools import write_to_html, delete_directory

def archive_to_report(Queue_Output, ruleldict, input_argv, unarchive_path):
    """
    report 功能
    :param Queue_Output:
    :param ruleldict:
    :param input_argv:
    :param unarchive_path:
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
            # false_number_count +=1
            # if false_number_count == false_number:
            #     n = False
            n = False
        else:
            temp_data[log_data.get('id')] = log_data.get('logs')

    for i in range(1,len(temp_data)+1):
        for data_dict in temp_data.get(i):
            # 如果 detail 不等于 None, 则代表已经获取了数据
            if data_dict.get('detail') != None:
                # 整理 type 为 Information 或 Others 中的特殊记录
                if data_dict.get('type') == 'Information' or data_dict.get('type') == 'Others':
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

    write_to_html(finish_data, input_argv)
    delete_directory(unarchive_path)