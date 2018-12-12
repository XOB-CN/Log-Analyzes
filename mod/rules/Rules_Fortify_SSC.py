# -*- coding:utf-8 -*-

RulesList = [
    {
        'name': '操作系统分类',
        'type': 'Information',
        'match': "os.name",
        'rule': "line.split('=')[-1]"
    },
    {
        'name': '操作系统版本',
        'type': 'Information',
        'match': "os.version",
        'rule': "line.split('=')[-1]"
    },
    {
        'name': 'Microsoft SQL JDBC 版本',
        'type': 'Information',
        'match': "/bin/sqljdbc",
        'rule': "re.search('sqljdbc(.*?)jar', line).group()"
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