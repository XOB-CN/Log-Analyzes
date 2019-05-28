# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;
# 注意：如果想要显示空格，需要写 &ensp;
log_rules_list = [
    {
        'name': 'Java Out Of Memory',
        'type': 'Java',
        'match': "java.lang.OutOfMemoryError: GC overhead limit exceeded",
        'solution': '请尝试调整 Tomcat 的 memory pool 大小<br>'
    },
    {
        'name': 'JDBC Driver 不兼容',
        'type': 'JDBC Driver',
        'match': "Found unsupported JDBC driver name",
        'solution': 'JDBC Driver 不兼容, 推荐更换 JDBC 驱动版本<br>'
                    '&ensp;mysql - 推荐 5.1.4x 以后的版本, 但不能安装 8.x 版本'
    },
    {
        'name': 'Duplicate entry（条目）',
        'type': 'MySQL',
        'match': "SQL Error: 1062, SQLState: 23000|Duplicate entry",
        'solution': '如果是全新安装的，可以考虑删除数据库后然后重建<br>'
                    '注意：一定需要注意数据库连接的字符集，SSC 的字符集必须要区分大小写，否则容易出现这个问题！'
    },
    {
        'name': '其余 Warn 信息',
        'type': 'Others',
        'match': "warn|wrn",
        'rule': "line"
    },
    {
        'name': '其余 Error 信息',
        'type': 'Others',
        'match': "error|err",
        'rule': "line"
    },
]

other_rule_list = [
    {
        'name': 'OS 分类',
        'type': 'Information',
        'match': "os\.name",
        'rule': "line.split('=')[-1]"
    },
    {
        'name': 'OS 版本',
        'type': 'Information',
        'match': "os\.version",
        'rule': "line.split('=')[-1]"
    },
    {
        'name': 'Fortify SSC 版本',
        'type': 'Information',
        'match': "Version:\d\d\.\d\d\.\d{4}",
        'rule': "line.split(':')[-1]"
    },
    {
        'name': 'Tomcat 版本',
        'type': 'Information',
        'match': "Server version:",
        'rule': "line.split(':')[-1]"
    },
    {
        'name': 'JRE 版本',
        'type': 'Information',
        'match': "java\.runtime\.version",
        'rule': "line.split('=')[-1]"
    },
    {
        'name': 'Process_Seed_Bundle',
        'type': 'Information',
        'match': "Opening seed bundle:.*Process_Seed_Bundle.*\.zip",
        'rule': "line.split(' - ')[-1]"
    },
    {
        'name': 'Report_Seed_Bundle',
        'type': 'Information',
        'match': "Opening seed bundle:.*Report_Seed_Bundle.*\.zip",
        'rule': "line.split(' - ')[-1]"
    },
    {
        'name': 'PCI_Basic_Seed_Bundle',
        'type': 'Information',
        'match': "Opening seed bundle:.*PCI_Basic_Seed_Bundle.*\.zip",
        'rule': "line.split(' - ')[-1]"
    },
]