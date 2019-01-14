# -*- coding:utf-8 -*-

RulesList = [
    {
        'name': 'Agent 版本',
        'type': 'Information',
        'match': "Agent Version:",
        'rule': "line"
    },
    {
        'name': 'AgentService 版本',
        'type': 'Information',
        'match': "AgentService Version",
        'rule': "line"
    },
    {
        'name': '没有本地数据库',
        'type': 'DataBase',
        'match': "Database path does not exist :",
        'solution': '没有本地数据库，一般在软件首次安装的时候会遇到这个错误，一般不用理会'
    },
    {
        'name': '其余 Warn 信息',
        'type': 'Others',
        'match': "Warn",
        'rule': "line"
    },
    {
        'name': '其余 Error 信息',
        'type': 'Others',
        'match': "Error",
        'rule': "line"
    },
]