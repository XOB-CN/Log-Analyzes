# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;
# 注意：如果想要显示空格，需要写 &ensp;
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
        'name': '未分配角色的用户所引发的问题',
        'type': '产品 Bug',
        'match': "unexpected exception caught: Origin: UserController at line 105|ERROR ExceptionTranslatorImpl.* - Ambiguous method overloading for method",
        'solution': '在 OMi 10.12 上是一个已知的问题，已经在 OMi version 10.6x (or the latest version 10.70) 上得到修复<br>'
                    '引发原因<br>'
                    '&ensp;&ensp;有未分配角色的用户导致 OMi 处理逻辑出现错误<br>'
                    '解决办法<br>'
                    '&ensp;&ensp;方法1：升级到 OMi 10.6x 版本<br>'
                    '&ensp;&ensp;方法2：安装更新补丁，具体内容请参考 SD02339162<br>'
                    '&ensp;&ensp;方法3：将为被分配角色的用户删除掉<br>'
                    '参考链接<br>'
                    '&ensp;&ensp;https://quixy.swinfra.net/quixy/query/detail.php?ISSUEID=QCIM8D104692<br>'
                    '&ensp;&ensp;https://quixy.swinfra.net/quixy/query/detail.php?ISSUEID=SD01591764',
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
        'name': 'Hostname',
        'type': 'Information',
        'match': "hostname:",
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