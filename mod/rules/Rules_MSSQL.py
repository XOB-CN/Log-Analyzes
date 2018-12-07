# -*- coding:utf-8 -*-

RulesList = [
    {
        'name':'Memory Pageout',
        'type':'Memory',
        'match':"A significant part of sql server process memory has been paged out",
        'solution':"添加内存或限制SQL内存使用量"
    },
    {
        'name': 'EventID 18056 - The client was unable to reuse a session with SPID ***',
        'type': 'EventID',
        'match': "Error: 18056",
        'solution':'考虑增加 IIS 连接池大小<br>'
                   '<a href="https://blog.csdn.net/yangzhawen/article/details/8209167">'
                   'https://blog.csdn.net/yangzhawen/article/details/8209167</a>'
    },
    {
        'name': 'EventID 18456 - 登陆失败',
        'type': 'EventID',
        'match': "Error: 18456",
        'solution': '请检查账户登陆相关的设置<br>'
                    '<a href="https://docs.microsoft.com/en-us/sql/relational-databases/errors-events/mssqlserver-18456-database-engine-error?view=sql-server-2017">'
                    'https://docs.microsoft.com/en-us/sql/relational-databases/errors-events/mssqlserver-18456-database-engine-error?view=sql-server-2017</a>'
    },
    {
        'name': 'EventID 26073 - TCP connection closed',
        'type': 'EventID',
        'match': "Error: 26073",
        'solution':'<a href="https://support.microsoft.com/zh-cn/help/2491214/non-yielding-scheduler-error-and-sql-server-2008-or-sql-server-2008-r2">'
                   'https://support.microsoft.com/zh-cn/help/2491214/non-yielding-scheduler-error-and-sql-server-2008-or-sql-server-2008-r2</a>'
    },
    {
        'name': '其余 EventID 事件',
        'type': 'EventID',
        'match': "Error: \d{4,6},",
        'solution': '<a href="https://docs.microsoft.com/en-us/sql/relational-databases/errors-events/errors-and-events-reference-database-engine?view=sqlallproducts-allversions">'
                    '请参考 Microsoft SQL Server Errors and Events Reference</a>'
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

