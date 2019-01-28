# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;
match_rules_list = [
    {
        'name': 'OPC NodeName',
        'type': 'Information',
        'match': "OPC_NODENAME",
        'rule': 'line.split("=")[1]'
    },
    {
        'name': 'Certificate Server',
        'type': 'Information',
        'match': "CERTIFICATE_SERVER",
        'rule': 'line.split("=")[1]'
    },
    {
        'name': 'OpC30-797 - Policies cannot connect to coda',
        'type': 'OA Error ID',
        'match': "OpC30-797",
        'solution': '请参考 KM1208518'
    },
    {
        'name': '其余 Warn 信息',
        'type': 'Others',
        'match': "Wrn",
        'rule': "line"
    },
    {
        'name': '其余 Error 信息',
        'type': 'Others',
        'match': "Err",
        'rule': "line"
    },
]