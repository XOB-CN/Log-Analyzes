# -*- coding:utf-8 -*-

import os, copy

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..','config.cfg')), encoding='utf-8')

from mod.tools import Check, Message
from mod.rules import InputRules_General, InputRules_Microsoft_SQL_Server

def single_general(filename, encoding, queue1):
    """
    单一文件，不需要处理任何排序;
    输出内容：{'id':section_id, 'logs':'log_content'}
    """
    log_content = []    # 存放初步整理的数据
    section_id = 0      # 记录分段的个数序号，用于记录顺序
    section_line = 0    # 记录每段内容的行数
    src_log_line = 0    # 记录原始日记的行数

    with open(filename, encoding=encoding) as f:
        for line in f:
            src_log_line += 1
            section_line += 1
            # log_content：['[数字，对应日记的原始行数]', '日记的每行内容']
            log_content.append(['['+str(src_log_line)+']', line])

            # 由于传递的是列表，所以此处需要使用深拷贝功能才行
            # 如果 check_input_rule 匹配到改行，则不能进行分割日记，因为此时是多行匹配的开始（即第一行）
            if section_line >= cfg.getint('base', 'segment_number') and Check.check_input_rule \
                        (rule_start=InputRules_General.rule_start,
                         rule_end=InputRules_General.rule_end,
                         rule_any=InputRules_General.rule_any,
                         line=line):
                section_id += 1
                log_content_copy = copy.deepcopy(log_content)
                queue1.put({'id':section_id, 'logs':log_content_copy})
                log_content.clear()
                section_line = 0

                # 显示提示信息
                Message.info_message('输入端：已读取第{n}段日记'.format(n=section_id))

    # 将最后一部分日记数据放入到队列中
    section_id += 1
    queue1.put({'id': section_id, 'logs': log_content})

    # 放入 False, 作为进程终止的判断条件
    for i in range(cfg.getint('base','multiprocess_counts')-1):
        queue1.put(False)

def single_sql_server(filename, encoding, queue1):
    """
    单一文件，专门针对 Microsoft_SQL_Server 的日记做处理，不需要做排序，但是需要在分割时注意是否包含有多行日记;
    输出内容：{'id':section_id, 'logs':'log_content'}
    """
    log_content = []    # 存放初步整理的数据
    section_id = 0      # 记录分段的个数序号，用于记录顺序
    section_line = 0    # 记录每段内容的行数
    src_log_line = 0    # 记录原始日记的行数

    with open(filename, encoding=encoding) as f:
        for line in f:
            src_log_line += 1
            section_line += 1
            # log_content：['[数字，对应日记的原始行数]', '日记的每行内容']
            log_content.append(['['+str(src_log_line)+']', line])

            # 如果 check_input_rule 匹配到改行，则不能进行分割日记，因为此时是多行匹配的开始（即第一行）
            if section_line >= cfg.getint('base','segment_number') and Check.check_input_rule\
                        (rule_start=InputRules_Microsoft_SQL_Server.rule_start,
                         rule_end=InputRules_Microsoft_SQL_Server.rule_end,
                         rule_any=InputRules_Microsoft_SQL_Server.rule_any,
                         line=line):
                section_id += 1
                log_content_copy = copy.deepcopy(log_content)
                queue1.put({'id':section_id, 'logs':log_content_copy})
                log_content.clear()
                section_line = 0

                # 显示提示信息
                Message.info_message('输入端：已读取第{n}段日记'.format(n=section_id))

    # 将最后一部分日记数据放入到队列中
    section_id += 1
    queue1.put({'id': section_id, 'logs': log_content})

    # 放入 False, 作为进程终止的判断条件
    for i in range(cfg.getint('base','multiprocess_counts')-1):
        queue1.put(False)