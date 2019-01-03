# -*- coding:utf-8 -*-
import os, copy

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..','config.cfg')), encoding='utf-8')

def single_general(filename, encoding, queue):
    """单一文件，不需要处理任何排序或事件"""
    n = 0
    m = 0
    log_evet = []
    with open(filename, encoding=encoding) as f:
        for line in f:
            n += 1
            m += 1
            log_evet.append([n, line])

            # 由于传递的是列表，所以此处需要使用深拷贝功能才行
            if m == 10:
                log_evet_copy = copy.deepcopy(log_evet)
                queue.put(log_evet_copy)
                log_evet.clear()
                m = 0

    # 将最后一部分日记数据放入到队列中
    queue.put(log_evet)

    # 放入 False, 作为进程终止的判断条件
    for i in range(cfg.getint('base','multiprocess_counts')-1):
        queue.put(False)