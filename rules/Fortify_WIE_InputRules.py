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
        'Console_trace\.log',
        'ManagerWS_trace\.log',
        'Scheduler_trace\.log',
        'TaskService_trace\.log',
        'UploaderService_trace\.log',
        # 所有以 .log 结尾的日志信息
        '.*\.log',
    ],
    # 其余类型
    'other':[
        # 信息搜集
        'ManagerWS_trace\.log',
    ],
}

# 内容黑名单，匹配到的内容直接忽略，不匹配
black_list = [
    # eg:如果该行包括 content 则直接忽略
    # 'content',

    # 目前看这些信息对排查错误帮助不大，都是警告信息
    'SMTP.Server setting not configured',
    'SMTP.Sender setting not configured',
    'SMTP.UserName property not configured',
    'SMTP.Password property not configured',
    'SNMP.HostIp setting not configured',
    'SNMP.Community setting not configured',
    'SNMP.MibSubject setting not configured',
    'SNMP.MibBody setting not configured',
]