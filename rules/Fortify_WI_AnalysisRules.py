# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;
# 注意：如果想要显示空格，需要写 &ensp;
log_rules_list = [
    {
        'name': 'Audit Engine 初始化错误',
        'type': 'Scan Log',
        'match': "Audit Engine initialization error|审核引擎初始化错误",
        'solution': "问题描述<br>"
                    "- 尝试初始化审核引擎时发生了不可恢复的错误<br><br>"
                    "解决办法<br>"
                    "- 暂无记录",
    },
    {
        'name': 'Audit 错误',
        'type': 'Scan Log',
        'match': "Audit Error|审核程序错误",
        'solution': "问题描述<br>"
                    "- 尝试初始化审核引擎时发生了不可恢复的错误<br><br>"
                    "解决办法<br>"
                    "- 暂无记录",
    },
    {
        'name': 'Start URL 错误',
        'type': 'Scan Log',
        'match': "Start Url Error|启动 URL 错误",
        'solution': "问题描述<br>"
                    "- 处理启动 URL 时发生不可恢复的错误<br><br>"
                    "解决办法<br>"
                    "- 检查 URL 语法，如果语法正确，请升级给 MicroFocus 后线工程师",
    },
    {
        'name': 'Start URL 被拒绝',
        'type': 'Scan Log',
        'match': "Start Url Rejected|启动 URL 被拒绝",
        'solution': "问题描述<br>"
                    "- URL 因请求拒绝设置而被拒绝<br><br>"
                    "解决办法<br>"
                    "- 对设置进行修改或使用其他启动 URL",
    },
    {
        'name': 'Web Macro 错误',
        'type': 'Scan Log',
        'match': "Web Macro Error|Web 宏错误",
        'solution': "问题描述<br>"
                    "- Web 宏播放期间发生了错误，具体取决于遇到的错误<br><br>"
                    "解决办法<br>"
                    "- 对于 RequestAborted 错误，服务器在宏播放期间未作出响应。如果经常发生这种情况，则应增大请求超时值<br>"
                    "- 有关其他可能的解决方案，请考虑连接问题部分",
    },
    {
        'name': 'Web Macro 状态错误',
        'type': 'Scan Log',
        'match': "Web Macro Status.*Expected:302.*Actual:200|Web 宏状态.*预期为.*302.*实际为.*200",
        'solution': "问题描述<br>"
                    "- Fortify WebInspect 在宏播放期间接收到的响应与在宏录制期间获取的响应不匹配<br><br>"
                    "解决办法<br>"
                    "- 这可能表示 Fortify WebInspect 在已登录的情况下正在尝试登录，或者表示 Fortify WebInspect 无法登录<br>"
                    "- 请检查扫描期间 Fortify WebInspect 是否已成功登录<br>"
                    "- 如果没有，请再次录制登录宏",
    },
    {
        'name': 'Check Error',
        'type': 'Scan Log',
        'match': "Check error.*session|检查错误.*会话",
        'solution': "问题描述<br>"
                    "- 执行检查时发生了错误<br><br>"
                    "解决办法<br>"
                    "- 安装最新版的 SmartUpdate",
    },
    {
        'name': '连接问题',
        'type': 'Scan Log',
        'match': "Connectivity issue.*Reason|连接问题.*原因",
        'solution': "问题描述<br>"
                    "- 此消息表示出现了网络连接问题, Fortify WebInspect 无法与远程主机通信<br>"
                    "解决办法<br>"
                    "- 重新启动网络硬件<br>"
                    "- 请使用 Microsoft 网络诊断工具<br><br>"
                    "- 检查连接设置<br>"
                    "- 检查防火墙及其相关设备",
    },
    {
        'name': '爬网程序（Crawler）错误',
        'type': 'Scan Log',
        'match': "Crawler error.*session|爬网程序错误.*会话",
        'solution': "问题描述<br>"
                    "- 爬网程序无法处理会话<br><br>"
                    "解决办法<br>"
                    "- 请联系 MicroFocus 后线工程师",
    },
    {
        'name': '设置覆盖',
        'type': 'Settings',
        'match': "Settings Override.*Setting|设置替代.*设置",
        'solution': "问题描述<br>"
                    "- 设置被产品更改, 可能表示存在设置升级问题<br><br>"
                    "解决办法<br>"
                    "- 恢复出厂默认值，并重新应用自定义设置<br>",
    },
    {
        'name': '达到内存限制',
        'type': 'Memory',
        'match': "Memory limit reached",
        'solution': "问题描述<br>"
                    "- 已达到 WI 进程的内存限制<br><br>"
                    "解决办法<br>"
                    "- 关闭其他未运行的扫描<br>"
                    "- 在给定的 Fortify WebInspect 实例中一次仅运行一个扫描",
    },
    {
        'name': '数据库连接问题',
        'type': 'DataBase',
        'match': "SPI.Scanners.Web.Framework.Session in updateExisting.*retries failed.*giving up calling iDbConnetivityHandler.OnConnectivityIssueDetected",
        'solution': "问题描述<br>"
                    "- 此消息表示该数据库已停止响应<br><br>"
                    "解决办法<br>"
                    "- 确保此数据库服务器正在运行且可以作出响应",
    },
    {
        'name': 'License 问题',
        'type': 'License',
        'match': "License Deactivated",
        'solution': "问题描述<br>"
                    "- 许可证出现问题<br><br>"
                    "解决办法<br>"
                    "- 确保 Fortify WebInspect 已获得适当许可",
    },
    {
        'name': 'SendResponse 异常',
        'type': 'Network',
        'match': "SPI.Net.Proxy.RequestReader in SendResponse.*swallowing exception",
        'endmatch': 'at ',
        'solution': "问题描述<br>"
                    "- 可能是由于 Network 或 connection 问题引起的<br><br>"
                    "解决办法<br>"
                    "- 暂时关闭防火墙以及反病毒软件<br>"
                    "- 检查代理服务器的情况<br>"
                    "- 检查 Login Macro 能否正常工作<br><br>"
                    "参考资料<br>"
                    "- SD02454909",
    },
    {
        'name': '其它异常 - swallowing exception',
        'type': 'Others',
        'match': "swallowing exception",
        'endmatch':'at ',
        'solution': "请根据具体的错误来做进一步的分析",
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
        'name': 'Web Inspect 版本',
        'type': 'Information',
        'match': "AscVersion=",
        'rule': "line.split('=')[-1]",
    },
    {
        'name': 'Scan 开始',
        'type': 'Information',
        'match': "Scan Start.*ScanID|扫描启动.*ScanID",
        'rule': "line"
    },
    {
        'name': 'Scan 开始错误',
        'type': 'Scan Information',
        'match': "Scan Start error|扫描启动错误",
        'rule': "line"
    },
    {
        'name': 'Scan 失败',
        'type': 'Scan Information',
        'match': "Scan Failed|扫描失败",
        'rule': "line"
    },
    {
        'name': 'Scan 停止',
        'type': 'Information',
        'match': "Scan Stop.*ScanID|扫描停止.*ScanID",
        'rule': "line"
    },
]