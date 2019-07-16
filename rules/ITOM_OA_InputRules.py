# -*- coding:utf-8 -*-

"""
如果匹配到下列列表中的规则，则本行不能被分段
match_start: 从行首开始匹配
match_end: 从行尾开始匹配
match_any: 利用正则表达式，全行任意位置匹配
"""
match_start=[]
match_end=[]
match_any=[]

# 需要分析的文件字典
need_files = {
    # 日志类型
    'logs':[
        # 12.x 版本 OA 的日志
        'system\.txt',

        # Unix 系统 / 11.x 版本
        'status\.scope',
        'status\.mi',
        'status\.perfalarm',
        'status\.perfd',

        # 未知日志
        'rc\.log',
        'syslog\.log',

        # 匹配所有
        # '.*\.log',
        # '.*\.txt',

    ],
    # 其余类型
    'other':[
        # 信息搜集
        'agent\.log',
    ],
}

# 内容黑名单，匹配到的内容直接忽略，不匹配
black_list = [
    # eg:如果该行包括 content 则直接忽略
    # 'content',
    'rolled=0',
]