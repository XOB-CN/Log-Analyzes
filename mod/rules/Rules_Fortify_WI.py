# -*- coding:utf-8 -*-

RulesList = [
    {
        'name':'WebInspect 版本',
        'type':'Information',
        'match':"WebInspect Sensor for EXE version",
        'rule':"line.split(' ', 10)[-1]"
    },
    {
        'name':'NET Framework 版本',
        'type':'Information',
        'match':"Running on .NET Framework version",
        'rule':"line.split(' ', 9)[-1]"
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