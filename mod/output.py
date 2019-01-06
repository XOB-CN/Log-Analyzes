# -*- coding:utf-8 -*-

import os

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..','config.cfg')), encoding='utf-8')

def to_report(queue):
    # 初始化参数
    n = True
    false_number = cfg.getint('base','multiprocess_counts') - 1
    false_number_count = 0

    # 循环从 queue 中获取数据
    while n:
        log_data = queue.get()
        if log_data == False:
            false_number_count += 1
            if false_number_count == false_number:
                n = False
        else:
            id = log_data.get('id')
            print(id)