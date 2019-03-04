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

# 需要分析的文件列表
need_file_list = [
    # log 部分
    'Backup\.log',
    'ConnectedAgentUI\.log',
    'Database\.log',
    'Service\.log',
    'Protocol\.log',
    'EMOLog\.log',
    'Heal\.log',
    'Soap\.log',
    'Notifier\.log',
    'CFA\.log',

    # xml 部分
    'ConnectionInfo\.xml',

    # txt 部分
    'SystemInfo\.txt',
    'Agent_\d{5}-\d{5}_\d+-\d+-\d{4}_\d+-\d+.txt',
    #'AgentLog.*\.txt'
]

# 如果匹配到，直接跳过后续匹配内容
black_rule_list = [
    # Backup.log
    '\[WARN \]\[Agent.Backup.Processors.MbLimitsBackupFileProcessor\]\[.*\] -',

    # Database.log
    'Attempt .* failed; retrying in \d.\d+ second',

    # Service.log
    'EMO not licensed. Skipping',
]