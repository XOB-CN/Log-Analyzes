# -*- coding:utf-8 -*-

import sys, time
from mod import tools
from mod.tools import Input

# 读取输入的参数, 并以字典形式返回输入的参数值
def read_args():
    sys_list = sys.argv
    for_list = ['-f','-u','-p','-h','-P','-d','-t','-out']
    idx_dict = {}
    arg_dict = {}
    type = ''

    # 检查输出的类型
    out_type = Input(sys_list)

    # 判断输入的参数是否有错误
    if out_type.chk_csv():
        type = 'csv'
    elif out_type.chk_mysql():
        type = 'mysql'
    elif out_type.chk_report():
        type = 'report'
    else:
        tools.Messages.pop_help()

    # 将输入的参数以字典的形式分别对应
    for i in for_list:
        if i in sys_list:
            index = sys_list.index(i)
            idx_dict[i] = sys_list[index+1]

    # 处理输入的参数
    arg_dict['filename'] = idx_dict['-f']
    if type == 'mysql':
        arg_dict['tab_name'] = idx_dict['-t']
    arg_dict['username'] = set_args(idx_dict,'-u','root')
    arg_dict['password'] = set_args(idx_dict,'-p','')
    arg_dict['hostname'] = set_args(idx_dict,'-h','localhost')
    arg_dict['database'] = set_args(idx_dict,'-d',time.strftime("%Y%m%d%H%M%S"))
    arg_dict['port'] = set_args(idx_dict,'-P','3306')
    arg_dict['output'] = set_args(idx_dict, '-out', 'mysql')

    # 额外处理一下 -out 参数的值，在这里检查会比较方便
    if arg_dict['output'] == 'mysql' or arg_dict['output'] == 'csv' or arg_dict['output'] == 'report':
        return arg_dict
    else:
        tools.Messages.pop_help()


# 读取参数的值，如果没有则采用默认值
def set_args(dict,argv,default):
    try:
        return dict[argv]
    except:
        return default


# 日记发送模块，将读取到的日记内容发送到另一个进程
def log_send(filename, queue):
    try:
        with open(filename,'r',encoding='utf8') as file:
            for line in file:
                queue.put(line)
        queue.put(False)

    except:
        with open(filename,'r',encoding='utf16') as file:
            for line in file:
                queue.put(line)
        queue.put(False)