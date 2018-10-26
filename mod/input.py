# -*- coding:utf-8 -*-

import sys, time
from mod import tools

# 读取输入的参数, 并以字典形式返回输入的参数值
def read_args():
    sys_list = sys.argv
    for_list = ['-f','-u','-p','-h','-P','-d','-t']
    idx_dict = {}
    arg_dict = {}

    # 检查输入的数据
    if len(sys_list)%2 == 0 or len(sys_list) == 1 :
        tools.pop_error("输入的参数个数不正确，请检查后重新输入")

    # 将输入的参数以字典的形式分别对应
    for i in for_list:
        if i in sys_list:
            index = sys_list.index(i)
            idx_dict[i] = sys_list[index+1]

    # 处理输入的参数
    try:
        arg_dict['filename'] = idx_dict['-f']
        arg_dict['tab_name'] = idx_dict['-t']
        arg_dict['username'] = set_args(idx_dict,'-u','root')
        arg_dict['password'] = set_args(idx_dict,'-p','')
        arg_dict['hostname'] = set_args(idx_dict,'-h','localhost')
        arg_dict['database'] = set_args(idx_dict,'-d',time.strftime("%Y%m%d%H%M%S"))
        arg_dict['port'] = set_args(idx_dict,'-P','3306')
    except:
        tools.pop_error("输入的参数不正确，请检查后重新输入")

    return arg_dict


# 读取参数的值，如果没有则采用默认值
def set_args(dict,argv,default):
    try:
        return dict[argv]
    except:
        return default


# 日记发送模块，将读取到的日记内容发送到另一个进程
def log_send(filename, queue):
    with open(filename,'r',encoding='utf8') as file:
        for line in file:
            queue.put(line)
    queue.put(False)