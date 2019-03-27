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
        'Backup\.log',
        'ConnectedAgentUI\.log',
        'Database\.log',
        'Service\.log',
        'Protocol\.log',
        'Agent_\d{5}-\d{5}_\d+-\d+-\d{4}_\d+-\d+.txt',
    ],
    # 其余类型
    'other':[
        # 信息搜集
        'SystemInfo\.txt',
        'ConnectionInfo\.xml',
    ],
}

# 内容黑名单，匹配到的内容直接忽略，不匹配
black_list = [
    # Backup.log
    '\[WARN \]\[Agent.Backup.Processors.MbLimitsBackupFileProcessor\]\[.*\] -',
    # Database.log
    'Attempt .* failed; retrying in \d.\d+ second',
    # Service.log
    'EMO not licensed. Skipping',
]