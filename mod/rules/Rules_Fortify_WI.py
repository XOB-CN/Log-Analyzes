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
]