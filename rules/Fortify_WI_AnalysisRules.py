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
    # {
    #     'name':'WebInspect 版本',
    #     'type':'Information',
    #     'match':"WebInspect Sensor for EXE version",
    #     'rule':"line.split(' ', 10)[-1]"
    # },
    # {
    #     'name':'NET Framework 版本',
    #     'type':'Information',
    #     'match':"Running on .NET Framework version",
    #     'rule':"line.split(' ', 9)[-1]"
    # },
]