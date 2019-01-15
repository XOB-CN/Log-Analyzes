# -*- coding:utf-8 -*-

import shutil   # 用于删除非空文件夹
from mod.tools import Output, Message, Debug, Check

@Debug.get_time_cost('[Debug] 输出端：')
def to_report(queue, rulelist, input_args):
    # 初始化参数
    n = True
    false_number = Check.get_multiprocess_counts() - 1
    false_number_count = 0
    temp_data = []

    # 循环从 queue 中获取数据
    while n:
        log_data = queue.get()
        if log_data == False:
            false_number_count += 1
            if false_number_count == false_number:
                n = False
        else:
            temp_data.append(log_data)

    # 对临时数据进行"排序"和"整合"，最终获得处理后的数据：finish_data
    m = 0
    temp_data_len = len(temp_data)
    temp_data_idx = []
    temp_data_all = []

    Message.info_message('[Info] 输出端：正在汇总数据，请稍后')
    for dict in temp_data:
        for k,v in dict.items():
            m += 1
            if m % 2 != 0:
                temp_data_idx.append(v)
            else:
                temp_data_all.append(v)

    # 加载最终数据的模板
    finish_data = rulelist

    # 开始整合数据
    for i in range(temp_data_len):
        idx = 0
        for content in temp_data_all[temp_data_idx.index(i + 1)]:
            # 如果 detail 不等于 None, 则代表已经获取了数据
            if content.get('detail') != None:
                # 整理 type 为 Information 或 Others 中的特殊记录
                if content.get('type') == 'Information' or content.get('type') == 'Others':
                    if rulelist[idx].get('content') == None:
                        rulelist[idx]['content'] = content.get('content')
                    else:
                        rulelist[idx]['content'] = rulelist[idx]['content'] + '<br>' + content.get('content')
                # 整理 log_line 中的记录
                if rulelist[idx].get('log_line') == None:
                    rulelist[idx]['log_line'] = content.get('log_line')
                else:
                    rulelist[idx]['log_line'] = rulelist[idx]['log_line'] + ', ' + content.get('log_line')
                # 整理 detail 中的记录
                if rulelist[idx].get('detail') == None:
                    rulelist[idx]['detail'] = content.get('detail')
                else:
                    rulelist[idx]['detail'] = rulelist[idx]['detail'] + '<br>' + content.get('detail')
            idx += 1

    # 将数据写入到文件中
    Message.info_message('[Info] 输出端：正在生成显示结果，请稍后')
    Output.write_to_html(finish_data, input_args)

def mult_to_report(queue, rulelist, input_args, unzip_path):
    """
    多文件的 report 功能
    :param queue: 消息队列
    :param rulelist: 匹配的规则列表
    :param input_args: 输入的参数，主要判断输出模式是否是 report
    :param unzip_path: 压缩包解压路径
    """
    # 初始化参数
    n = True
    false_number = Check.get_multiprocess_counts() - 1
    false_number_count = 0
    temp_data = []

    # 循环从 queue 中获取数据
    while n:
        log_data = queue.get()
        if log_data == False:
            false_number_count += 1
            if false_number_count == false_number:
                n = False
        else:
            temp_data.append(log_data)

    # 对临时数据进行"排序"和"整合"，最终获得处理后的数据：finish_data
    m = 0
    temp_data_len = len(temp_data)
    temp_data_idx = []
    temp_data_all = []

    Message.info_message('[Info] 输出端：正在汇总数据，请稍后')
    for dict in temp_data:
        for k, v in dict.items():
            m += 1
            if m % 2 != 0:
                temp_data_idx.append(v)
            else:
                temp_data_all.append(v)

    # 加载最终数据的模板
    finish_data = rulelist

    # 开始整合数据
    for i in range(temp_data_len):
        idx = 0
        for content in temp_data_all[temp_data_idx.index(i + 1)]:
            # 如果 detail 不等于 None, 则代表已经获取了数据
            if content.get('detail') != None:
                # 整理 type 为 Information 或 Others 中的特殊记录
                if content.get('type') == 'Information' or content.get('type') == 'Others':
                    if finish_data[idx].get('content') == None:
                        finish_data[idx]['content'] = content.get('content')
                    else:
                        finish_data[idx]['content'] = finish_data[idx]['content'] + '<br>' + content.get('content')
                # 整理 log_line 中的记录
                if finish_data[idx].get('log_line') == None:
                    finish_data[idx]['log_line'] = content.get('log_line')
                else:
                    finish_data[idx]['log_line'] = finish_data[idx]['log_line'] + '<br>' + content.get('log_line')
                # 整理 detail 中的记录
                if finish_data[idx].get('detail') == None:
                    finish_data[idx]['detail'] = content.get('detail')
                else:
                    finish_data[idx]['detail'] = finish_data[idx]['detail'] + '<br>' + content.get('detail')

                # 整理 log_class 中的记录
                if finish_data[idx].get('log_class') == None:
                    finish_data[idx]['log_class'] = content.get('log_class')
            idx += 1

    # 将数据写入到文件中
    Message.info_message('[Info] 输出端：正在生成显示结果，请稍后')
    Output.write_to_html(finish_data, input_args)

    # 清空临时目录中的文件
    shutil.rmtree(unzip_path)
    Message.info_message('[Info] 输出端：临时目录已删除，分析完成')