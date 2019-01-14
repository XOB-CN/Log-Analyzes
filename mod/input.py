# -*- coding:utf-8 -*-

import os, copy

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..','config.cfg')), encoding='utf-8')

from mod.tools import Check, Message
from mod.rules import InputRules_General, InputRules_Microsoft_SQL_Server
from mod.rules import InputRules_ConnectedBackup_Agent as Input_CBK_Agent

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
                        (rule_start=InputRules_General.match_start,
                         rule_end=InputRules_General.match_end,
                         rule_any=InputRules_General.match_any,
                         line=line):
                section_id += 1
                log_content_copy = copy.deepcopy(log_content)
                queue1.put({'id':section_id, 'logs':log_content_copy})
                log_content.clear()
                section_line = 0

                # 显示提示信息
                Message.info_message('[Info] 输入端：已读取第 {n} 段日记'.format(n=section_id))

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
                        (rule_start=InputRules_Microsoft_SQL_Server.match_start,
                         rule_end=InputRules_Microsoft_SQL_Server.match_end,
                         rule_any=InputRules_Microsoft_SQL_Server.match_any,
                         line=line):
                section_id += 1
                log_content_copy = copy.deepcopy(log_content)
                queue1.put({'id':section_id, 'logs':log_content_copy})
                log_content.clear()
                section_line = 0

                # 显示提示信息
                Message.info_message('[Info] 输入端：已读取第 {n} 段日记'.format(n=section_id))

    # 将最后一部分日记数据放入到队列中
    section_id += 1
    queue1.put({'id': section_id, 'logs': log_content})

    # 放入 False, 作为进程终止的判断条件
    for i in range(cfg.getint('base','multiprocess_counts')-1):
        queue1.put(False)

def zipfile_general(filelist, queue1):
    """
    压缩包文件，不需要处理日记排序
    最终生成的数据格式： {'id':'切割的分段 id', 'log_class':'日记所属分类', 'filename':'文件名', 'log_content':[[ '日记行数', '日记的每行内容' ],]}
    :param filelist:
    :param queue1:
    """
    section_id = 0  # 记录分段的个数序号，用于记录顺序
    section_line = 0  # 记录每段内容的行数
    src_log_line = 0  # 记录原始日记的行数
    log_content = []  # 存放初步整理的数据

    for filepath in filelist:
        # 初始化参数
        encoding = Check.get_encoding(filepath)
        filename = os.path.split(filepath)[1]
        log_class = filename.split('.')[0]

        with open(filepath, mode='r', encoding=encoding) as f:
            for line in f:
                section_line += 1
                src_log_line += 1
                log_content.append(['['+str(src_log_line)+']', line])

                if section_line >= cfg.getint('base','segment_number') and Check.check_input_rule\
                        (rule_start=InputRules_General.match_start,
                         rule_end=InputRules_General.match_end,
                         rule_any=InputRules_General.match_any,
                         line=line):
                    section_id += 1
                    log_content_copy = copy.deepcopy(log_content)
                    queue1.put({'id':section_id, 'log_class':log_class, 'filename':filename, 'log_content':log_content_copy})
                    log_content.clear()
                    section_line = 0

                    # 显示提示信息
                    Message.info_message('[Info] 输入端：已读取第 {n} 段日记'.format(n=section_id))

        # 将最后一部分日记数据放入到队列中
        section_id += 1
        log_content_copy = copy.deepcopy(log_content)
        queue1.put({'id': section_id, 'log_class': log_class, 'filename': filename, 'log_content': log_content_copy})
        log_content.clear()
        src_log_line = 0

    # 放入 False, 作为进程终止的判断条件
    for i in range(cfg.getint('base', 'multiprocess_counts') - 1):
        queue1.put(False)

def zipfile_cbk_agent(filelist, queue1):
    """
    压缩包文件，不需要处理日记排序
    最终生成的数据格式： {'id':'切割的分段 id', 'log_class':'日记所属分类', 'filename':'文件名', 'log_content':[[ '日记行数', '日记的每行内容' ],]}
    :param filelist:
    :param queue1:
    """
    section_id = 0  # 记录分段的个数序号，用于记录顺序
    section_line = 0  # 记录每段内容的行数
    src_log_line = 0  # 记录原始日记的行数
    log_content = []  # 存放初步整理的数据

    for filepath in filelist:
        # 初始化参数
        encoding = Check.get_encoding(filepath)
        filename = os.path.split(filepath)[1]
        log_class = filename.split('.')[0]

        # 注意，通用模块中可以没有这部分：
        if log_class[0:len('Agent_')] == 'Agent_':
            log_class = 'Information'


        with open(filepath, mode='r', encoding=encoding) as f:
            for line in f:
                section_line += 1
                src_log_line += 1
                log_content.append(['['+str(src_log_line)+']', line])

                if section_line >= cfg.getint('base','segment_number') and Check.check_input_rule\
                        (rule_start=Input_CBK_Agent.match_start,
                         rule_end=Input_CBK_Agent.match_end,
                         rule_any=Input_CBK_Agent.match_any,
                         line=line):
                    section_id += 1
                    log_content_copy = copy.deepcopy(log_content)
                    queue1.put({'id':section_id, 'log_class':log_class, 'filename':filename, 'log_content':log_content_copy})
                    log_content.clear()
                    section_line = 0

                    # 显示提示信息
                    Message.info_message('[Info] 输入端：已读取第 {n} 段日记'.format(n=section_id))

        # 将最后一部分日记数据放入到队列中
        section_id += 1
        log_content_copy = copy.deepcopy(log_content)
        queue1.put({'id': section_id, 'log_class': log_class, 'filename': filename, 'log_content': log_content_copy})
        log_content.clear()
        src_log_line = 0

    # 放入 False, 作为进程终止的判断条件
    for i in range(cfg.getint('base', 'multiprocess_counts') - 1):
        queue1.put(False)