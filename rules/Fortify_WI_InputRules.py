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
        # 以 .log 结尾的日志信息
        'ScanLog\.log',
        'Scanner\.log$',
        'WebInspectWCFService\.log'
    ],
    # 其余类型
    'other':[
        # 信息搜集
        '.*\.log',
    ],
}

# 内容黑名单，匹配到的内容直接忽略，不匹配
black_list = [
    # eg:如果该行包括 content 则直接忽略
    # 'content',
]