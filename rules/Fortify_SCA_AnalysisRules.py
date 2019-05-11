# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;
# 注意：如果想要显示空格，需要写 &ensp;
log_rules_list = [
    {
        'name': 'nsconsumed-mismatch is currently enabled, but was not in the PCH file',
        'type': 'Bug',
        'match': "error: -Werror=nsconsumed-mismatch is currently enabled, but was not in the PCH file",
        'solution': '在 Fortify SCA 18.20 版本上可能是一个 Bug, 请参考 <a href="https://rdapps.swinfra.net/quixy/#/viewEntity/OCTCR11G188074">OCTCR11G188074</a>',
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
    # {
    #     'name': 'OS 分类',
    #     'type': 'Information',
    #     'match': "os\.name",
    #     'rule': "line.split('=')[-1]"
    # },
]