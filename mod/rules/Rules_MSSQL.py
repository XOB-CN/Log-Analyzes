# -*- coding:utf-8 -*-

ErrorLogList = [
    {
        'name':'Memory_pageout',
        'type':'Memory',
        'info':'内存不足',
        'keyword':"A significant part of sql server process memory has been paged out",
        'solution':"添加内存或限制SQL内存使用量"
    },
    {
        'name': 'Security_login',
        'type': 'Security',
        'info': '登陆失败',
        'keyword': "Login failed for user",
        'solution': "请检查账户登陆相关的设置"
    },
    {
        'name': 'EventID_18056',
        'type': 'EventID',
        'info': 'The client was unable to reuse a session with SPID ***',
        'keyword': "Error: 18056",
        'solution':'考虑增加 IIS 连接池大小<br>'
                   '<a href="https://blog.csdn.net/yangzhawen/article/details/8209167">'
                   'https://blog.csdn.net/yangzhawen/article/details/8209167</a>'
    },
    {
        'name': 'EventID_26073',
        'type': 'EventID',
        'info': 'TCP connection closed',
        'keyword': "Error: 26073",
        'solution':'<a href="https://support.microsoft.com/zh-cn/help/2491214/non-yielding-scheduler-error-and-sql-server-2008-or-sql-server-2008-r2">'
                   'https://support.microsoft.com/zh-cn/help/2491214/non-yielding-scheduler-error-and-sql-server-2008-or-sql-server-2008-r2</a>'
    },
]
