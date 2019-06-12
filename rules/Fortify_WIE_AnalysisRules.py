# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;
# 注意：如果想要显示空格，需要写 &ensp;
log_rules_list = [
    {
        'name': '无法连接 SSC',
        'type': 'SSC 集成',
        'match': "Error connecting to SSC",
        'endmatch': '在 | at',
        'solution': "请根据报错的内容做进一步的排查<br>"
                    "<br>可能情况 - security token 问题<br>"
                    "&ensp;- 如果出现 The security token could not be authenticated or authorized，则请考虑在 SSC 修改完账户密码后，将 WIE 重新初始化的操作"
    },
    {
        'name': '无法 获取/检索 SSC 中的 Applications 或 user 和 Group',
        'type': 'SSC 集成',
        'match': "Unable to retrieve a list of.*applications from SSC|Unable to retrieve a list of user or group|Unable to Get list of user or group from ssc",
        'solution': "请检查日志的其它部分，这通常是由其它问题引起的<br>"
                    "<br>可能情况 - security token 问题<br>"
                    "&ensp;- 如果出现 The security token could not be authenticated or authorized，则请考虑在 SSC 修改完账户密码后，将 WIE 重新初始化的操作"
    },
    {
        'name': '无法获取 Authentication Token',
        'type': 'Login',
        'match': "Unable to Get Authentication Token",
        'endmatch': '在 AmpManagerWS| at AmpManagerWS',
        'solution': "问题原因<br>"
                    "- 可能是在更改 SSC 密码后，由于数据没有同步，所以登录不上 WIE，但是如果先登录 WIE，会导致数据回写至 SSC，造成数据不统一<br><br>"
                    "解决思路<br>"
                    "- 尝试重置 SSC 账户密码，此时不要登陆 WIE，而是执行 Webinspect Enterprise Initialization Wizard"
    },
    {
        'name': '无法获得客户端许可证',
        'type': 'Login',
        'match': "Unable to obtain client license",
        'endmatch': '在| at',
        'solution': "请根据报错的内容做进一步的排查,并且需要进一步检查日志的其它内容，因为这个错误通常是由其它问题导致的<br>"
                    "<br>可能情况 - 日志中包含 Unable to Get Authentication Token<br>"
                    "- 尝试重置 SSC 账户密码，此时不要登陆 WIE，而是执行 Webinspect Enterprise Initialization Wizard"
    },
    {
        'name': '其余登陆错误',
        'type': 'Login',
        'match': "Error occurred when attempting to generate a one-use token|GetCallerIdentity: Cannot find the caller associated with the authentication token",
        'solution': "请根据报错的内容做进一步的排查,并且需要进一步检查日志的其它内容，因为这个错误通常是由其它问题导致的<br>"
                    "<br>可能情况 - 日志中包含 Unable to Get Authentication Token<br>"
                    "- 尝试重置 SSC 账户密码，此时不要登陆 WIE，而是执行 Webinspect Enterprise Initialization Wizard"
    },
    {
        'name': '无法连接数据库',
        'type': 'DataBase',
        'match': "Unable to connect to Repository database",
        'endmatch': 'at SPI|Error Number.*State.*Class.*',
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