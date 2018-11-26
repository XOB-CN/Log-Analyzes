# -*- coding:utf-8 -*-

RulesList = [
    {
        'name': 'OS Name',
        'type': 'Information',
        'info': '操作系统分类',
        'keyword': "os.name",
        'rule': "line.split('=')[-1]"
    },
    {
        'name': 'OS Version',
        'type': 'Information',
        'info': '操作系统版本',
        'keyword': "os.version",
        'rule': "line.split('=')[-1]"
    },
    {
        'name': 'JDBC Version',
        'type': 'Information',
        'info': 'JDBC 版本',
        'keyword': "/bin/sqljdbc",
        'rule': "re.search('sqljdbc(.*?)jar', line).group()"
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