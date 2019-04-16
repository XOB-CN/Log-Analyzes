# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;
# 注意：如果想要显示空格，需要写 &ensp;
log_rules_list = [
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
        'match': "OS Name:",
        'rule': "line.split(':')[-1]"
    },
    {
        'name': 'OS 版本',
        'type': 'Information',
        'match': "OS Version:",
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
        'match': "JVM Version:",
        'rule': "line.split(':')[-1]"
    },
]