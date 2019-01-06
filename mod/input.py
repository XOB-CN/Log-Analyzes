# -*- coding:utf-8 -*-

import os, copy

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..','config.cfg')), encoding='utf-8')

def single_general(filename, encoding, queue1):
    """
    单一文件，不需要处理任何排序或事件;
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
            if section_line == cfg.getint('base','segment_number'):
                section_id += 1
                log_content_copy = copy.deepcopy(log_content)
                queue1.put({'id':section_id, 'logs':log_content_copy})
                log_content.clear()
                section_line = 0

    # 将最后一部分日记数据放入到队列中
    section_id += 1
    queue1.put({'id': section_id, 'logs': log_content})

    # 放入 False, 作为进程终止的判断条件
    for i in range(cfg.getint('base','multiprocess_counts')-1):
        queue1.put(False)