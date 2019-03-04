# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;
match_rules_list = [
    {
        'name': 'OA NodeName',
        'type': 'Information',
        'match': "OPC_NODENAME",
        'rule': 'line.split("=")[-1]',
    },
    {
        'name': 'OA Version',
        'type': 'Information',
        'match': "OPC_INSTALLED_VERSION",
        'rule': 'line.split("=")[-1]',
    },
    {
        'name': 'OA IP Address',
        'type': 'Information',
        'match': "OPC_IP_ADDRESS",
        'rule': 'line.split("=")[-1]',
    },
    {
        'name': 'OS Type',
        'type': 'Information',
        'match': "ostype=",
        'rule': 'line.split("=")[-1]',
    },
    {
        'name': 'OS Name',
        'type': 'Information',
        'match': "osname=",
        'rule': 'line.split("=")[-1]',
    },
    {
        'name': 'OS Kernel',
        'type': 'Information',
        'match': "osversion=",
        'rule': 'line.split("=")[-1]',
    },
    {
        'name': 'Certificate Server',
        'type': 'Information',
        'match': "CERTIFICATE_SERVER",
        'rule': 'line.split("=")[-1]',
    },
    {
        'name': 'OA 相关进程被终止',
        'type': 'OA Process',
        'match': "が終了されました",
        'solution': '请结合时间点以及其余信息来做判断',
    },
    {
        'name': 'OpC30-712/750 - Perl Script 执行错误',
        'type': 'OA Error ID',
        'match': "OpC30-712|OpC30-750",
        'solution': '应该是一个 Bug，请参考 QCIM8D89282(QCIM1A190626), 在 QCCR1A189077 中提供了修复补丁的相关信息<br>'
                    'QCCR1A189077：同时执行多个相同类型的 policies 可能会引发 OpC30-797/OpC30-728/OpC30-714/OpC30-750 errors',
    },
    {
        'name': 'OpC30-797 - Policies cannot connect to coda',
        'type': 'OA Error ID',
        'match': "OpC30-797",
        'solution': '请参考 KM1208518',
    },
    {
        'name': '其余 Warn 信息',
        'type': 'Others',
        'match': "Wrn",
        'rule': "line",
    },
    {
        'name': '其余 Error 信息',
        'type': 'Others',
        'match': "Err|失敗",
        'rule': "line",
    },
]