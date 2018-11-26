# -*- coding:utf-8 -*-

RulesList = [
    {
        'name':'WI Version',
        'type':'Information',
        'info':'WebInspect 版本',
        'keyword':"WebInspect Sensor for EXE version",
        'rule':"line.split(' ', 10)[-1]"
    },
    {
        'name':'NET Framework Version',
        'type':'Information',
        'info':'NET Framework 版本',
        'keyword':"Running on .NET Framework version",
        'rule':"line.split(' ', 9)[-1]"
    },
    {
        'name': 'Warn',
        'type': 'Others',
        'info': '其余 Warn 信息',
        'keyword': "Warn",
        'rule': "line"
    },
    {
        'name': 'Error',
        'type': 'Others',
        'info': '其余 Error 信息',
        'keyword': "Error",
        'rule': "line"
    },
]