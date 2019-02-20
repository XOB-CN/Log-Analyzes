# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;

match_rules_list = [
    {
        'name': 'JDBC Driver 不兼容',
        'type': 'JDBC Driver',
        'match': "Found unsupported JDBC driver name",
        'solution': 'JDBC Driver 不兼容, 推荐更换 JDBC 驱动版本<br>'
                    '* mysql - 推荐 5.1.4x 以后的版本, 但不能安装 8.x 版本'
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