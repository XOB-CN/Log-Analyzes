# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;
match_rules_list = [
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
        'name': 'Agent 连接信息',
        'type': 'Information',
        'match': "&lt;Host&gt;&lt;!\[.*\]&gt;&lt;/Host&gt;",
        'rule': "line.split('[')[-1].split(']')[0]"
    },
    {
        'name': '无法加载配置文件',
        'type': 'Service',
        'match': "failed to load external entity",
        'solution': '考虑程序本身问题，建议尝试重新安装 Agent'
    },
    {
        'name': '无法连接到 DataCenter',
        'type': 'Network',
        'match': "Bouncing due to NetworkException at Line",
        'endmatch':'Error Code',
        'solution': '通常不会是网络问题，请优先考虑 AgentService 是否启动正常，之后考虑使用 dsping 或 dsping80 来检查到 DataCenter 是否能正常通信，如果不正常，请检查证书相关，或者连接相关的配置信息'
    },
    {
        'name': '没有本地数据库',
        'type': 'DataBase',
        'match': "Database path does not exist :",
        'solution': '没有本地数据库，一般在软件首次安装的时候会遇到这个错误，一般不用理会'
    },
    {
        'name': '本地 SQLite 数据库被锁定',
        'type': 'DataBase',
        'match': "Attempt \d+ failed; giving up",
        'endmatch':'Sqlite Error: database is locked',
        'solution': '通常都代表着数据库被损坏，请尝试删除本地 sqlite 数据库'
    },
    {
        'name': '本地 SQLite 数据有问题',
        'type': 'DataBase',
        'match': "Sqlite Error: SQL logic error or missing database",
        'solution': '通常都代表着数据库被损坏，请尝试删除本地 sqlite 数据库'
    },
    {
        'name': '本地 SQLite 变成只读',
        'type': 'DataBase',
        'match': "Sqlite Error: attempt to write a readonly database",
        'solution': '通常都代表着数据库被损坏，请尝试删除本地 sqlite 数据库'
    },
    {
        'name': '磁盘主文件表(Master File Table)有问题',
        'type': 'Disk Drive',
        'match': "Error retrieving Sec Decr ID",
        'solution': '通常代表计算机上的磁盘有问题，建议执行磁盘扫描，请参考 chkdsk 命令'
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