# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;
# 注意：如果想要显示空格，需要写 &ensp;
log_rules_list = [
    {
        'name': '无法连接数据库',
        'type': 'DataBase',
        'match': "Unable to connect to Repository database",
        'endmatch': 'at SPI',
        'solution': "检查数据库连接是否正常<br>"
                    "- 请详细检查报错的详细内容，里面可能会包含无法连接的 sql 账户以及 database 的名字"
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
        'name': 'APP 版本',
        'type': 'Information',
        'match': "appVersion=",
        'rule': "line.split('=')[-1]"
    },
]