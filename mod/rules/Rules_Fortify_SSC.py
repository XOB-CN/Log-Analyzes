# -*- coding:utf-8 -*-

RulesList = [
    {
        'name':'OS Name',
        'type':'Information',
        'info':'操作系统分类',
        'keyword':"os.name",
        'rule':"line.split('=')[-1]"
    },
    {
        'name': 'OS Version',
        'type': 'Information',
        'info': '操作系统版本',
        'keyword': "os.version",
        'rule': "line.split('=')[-1]"
    },
]