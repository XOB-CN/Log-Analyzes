# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;
log_rules_list = [
    {
        'name': '日记配置文件错误',
        'type': 'Log 配置文件',
        'match': "ERROR Attempted to append to closed appender named",
        'solution': '配置文件位置：%topaz_home%conf\\core\\Tools\\log4j\\<br>'
                    '方法1：找到日记配置文件并修改错误的地方<br>'
                    '方法2：重新安装软件，用来还原默认配置<br>',
    },
    {
        'name': '无法正常连接 SQL Server',
        'type': 'DataBase',
        'match': "com\.microsoft\.sqlserver\.jdbc\.SQLServerException",
        'solution': '请考虑数据库问题',
    },
    {
        'name': '内存溢出',
        'type': 'Memory',
        'match': "OutOfMemory|Java heap space",
        'solution': '请参考 Case: 5318358550/SD01828653',
    },
    {
        'name': '其余 Warn 信息',
        'type': 'Others',
        'match': "Wrn|Warn",
        'solution': '剩余的 Warn 信息',
    },
    {
        'name': '其余 Error 信息',
        'type': 'Others',
        'match': "Err|失敗",
        'solution': '剩余的 Error 信息',
    },
]

other_rule_list = [
    {
        'name': 'OS Name',
        'type': 'Information',
        'match': "os:",
        'rule': "line.split(':')[-1].strip()",
    },
    {
        'name': 'OBM Version',
        'type': 'Information',
        'match': "Version: \d+\.\d+",
        'rule': "line.split(':')[-1].strip()",
    },
    {
        'name': 'Hostname',
        'type': 'Information',
        'match': "hostname:",
        'rule': "line.split(':')[-1].strip()",
    },
    {
        'name': 'Domain',
        'type': 'Information',
        'match': "domain:",
        'rule': "line.split(':')[-1].strip()",
    },
    {
        'name': 'Physical Memory',
        'type': 'Information',
        'match': "physical memory:",
        'rule': "line.split(':')[-1].strip()",
    },

    {
        'name': 'IP Address',
        'type': 'Information',
        'match': "ip address:",
        'rule': "line.split(':')[-1].strip()",
        'mult-value':True
    },
    {
        'name': 'Mac Address',
        'type': 'Information',
        'match': "mac address:",
        'rule': "line.split(':',1)[-1].strip()",
        'mult-value':True
    },
    {
        'name': 'Hotfix Info',
        'type': 'Information',
        'match': "Hotfix:",
        'rule': "line.split(':',1)[-1].strip()",
        'mult-value':True
    },
]