# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;
# 注意：如果想要显示空格，需要写 &ensp;
log_rules_list = [
    {
        'name': '日记配置文件错误',
        'type': '配置文件错误',
        'match': "ERROR Attempted to append to closed appender named",
        'solution': '配置文件位置：%topaz_home%conf\\core\\Tools\\log4j\\<br>'
                    '方法1：找到日记配置文件并修改错误的地方<br>'
                    '方法2：重新安装软件，用来还原默认配置<br>',
    },
    {
        'name': '未分配角色的用户所引发的问题',
        'type': '产品 Bug',
        'match': "unexpected exception caught: Origin: UserController at line 105|ERROR ExceptionTranslatorImpl.* - Ambiguous method overloading for method",
        'solution': '在 OMi 10.12 上是一个已知的问题，已经在 OMi version 10.6x (or the latest version 10.70) 上得到修复<br>'
                    '引发原因<br>'
                    '&ensp;&ensp;有未分配角色的用户导致 OMi 处理逻辑出现错误<br>'
                    '解决办法<br>'
                    '&ensp;&ensp;方法1：升级到 OMi 10.6x 版本<br>'
                    '&ensp;&ensp;方法2：安装更新补丁，具体内容请参考 SD02339162<br>'
                    '&ensp;&ensp;方法3：将为被分配角色的用户删除掉<br>'
                    '参考链接<br>'
                    '&ensp;&ensp;https://quixy.swinfra.net/quixy/query/detail.php?ISSUEID=QCIM8D104692<br>'
                    '&ensp;&ensp;https://quixy.swinfra.net/quixy/query/detail.php?ISSUEID=SD01591764',
    },
    {
        'name': '无法正常连接 SQL Server',
        'type': 'DataBase',
        'match': "com\.microsoft\.sqlserver\.jdbc\.SQLServerException",
        'solution': '请考虑数据库问题',
    },
    {
        'name': '内存溢出',
        'type': 'Memory',
        'match': "OutOfMemory|Java heap space",
        'solution': '请参考 Case 5318358550/SD01828653',
    },
    {
        'name': '没有 core id 的情况下获得该 Node 特定的健康检查配置',
        'type': 'HeartBeat',
        'match': "Got node specific health check config without agent core id",
        'solution': '请参考 Case SD01976057<br>'
        '此问题需要搜集 HeartBeat 的 debug 级别日志来做进一步的调查，搜集方法如下：<br>'
        '<br>Gateway 组件<br>'
        '&ensp;%TOPAZ_HOME%\\conf\\core\\Tools\\log4j\\wde\\opr-heartbeat.properties<br>'
        'DPS 组件<br>'
        '&ensp;%TOPAZ_HOME%\\conf\\core\\Tools\\log4j\\opr-backend\\opr-heartbeat.properties<br>'
        '&ensp;%TOPAZ_HOME%\\conf\\core\\Tools\\log4j\\opr-backend\\opr-backend.properties<br>'
        '<br>将上述配置文件修改下列内容<br>'
        '&ensp;loglevel=DEBUG<br>'
        '&ensp;def.file.max.size=20000KB<br>',
    },
    {
        'name': 'OpC40-1905/OpC40-1906/OpC30-36 - 可能是连接性问题',
        'type': 'OBM Error ID',
        'match': "OpC30-36|OpC40-1905|OpC40-1906|サーバーに障害があります。OVO メッセージ レシーバへの|WRN.*Forwarding message/action response to OVO message",
        'solution':
            'OMU 服务器上的心跳轮询 (HBP, Heartbeat polling) 有时会检测到以下错误：<br>'
            '- Message Agent on node ... is buffering messages. (OpC40-1905)<br>'
            '- Message Agent on node ... is buffering messages for this Management Server. (OpC40-1906)<br>'
            '在 System.txt 的对应节点上出现下列错误，则表明出现了消息缓冲已经发生<br>'
            '- Forwarding message/action response to OVO message receiver failed due to server failure. (OpC30-36)<br>'
            '如果在短时间内发生这个问题，则这个问题可以被忽略，如果持续发生，则需要做继续调查，调查步骤请参考 KM633951<br>'
            '<br>可能的原因<br>'
            '- 由于代理节点上的 System.txt 具有 OpC30-36，因此消息代理（opcmsga）可能在当时存在通信问题<br>'
            '- 但是，即使您没有看到（或没有猜测）明显可能的通信问题原因，也可能发生意外缓冲<br>'
            '- 例如，如果 opcmsga(在代理上) 和 ovbbccb (在 OMU 服务器上) 之间建立的 HTTPS(实际上是TCP) 连接被强制断开,<br>'
            '- opcmsga 将无法重用现有连接来发送进一步的消息或动作响应.<br>'
            '- 因此，opcmsga 将 System.txt 中的 OpC30-36 删除，并移动到缓冲状态<br>'
            '- 默认情况下，连接在一分钟内重新建立，如果没有真正的通信问题，缓冲也在一分钟内解决<br>'
            '<br>调查方向<br>'
            '- 如果缓冲在一分钟内自动解决，则可以忽略缓冲消息<br>'
            '- 检查网络连接问题<br>'
            '- 更新 OM Agent 以获取最新的 BBC 组件(最新的BBC组件被增强，以处理未使用的TCP连接)<br>'
            '- 推荐使用最新的 OM 代理版本<br>'
            '<br>补充信息<br>'
            '- 只要在代理上实际发生缓冲，就不能避免 HBP 进行缓冲检测 (OpC40-1905/OpC40-1906)',
    },
    {
        'name': '其余 Warn 信息',
        'type': 'Others',
        'match': "Wrn|Warn",
        'solution': '剩余的 Warn 信息',
    },
    {
        'name': '其余 Error 信息',
        'type': 'Others',
        'match': "Err|失敗",
        'solution': '剩余的 Error 信息',
    },
]

other_rule_list = [
    {
        'name': 'OS Name',
        'type': 'Information',
        'match': "os:",
        'rule': "line.split(':')[-1].strip()",
    },
    {
        'name': 'Hostname',
        'type': 'Information',
        'match': "hostname:",
        'rule': "line.split(':')[-1].strip()",
    },
    {
        'name': 'Physical Memory',
        'type': 'Information',
        'match': "physical memory:",
        'rule': "line.split(':')[-1].strip()",
    },

    {
        'name': 'IP Address',
        'type': 'Information',
        'match': "ip address:",
        'rule': "line.split(':',1)[-1].strip()",
        'mult-value':True,
    },
    {
        'name': 'Mac Address',
        'type': 'Information',
        'match': "mac address:",
        'rule': "line.split(':',1)[-1].strip()",
        'mult-value':True,
    },
    {
        'name': 'Hotfix Info',
        'type': 'Information',
        'match': "Hotfix:",
        'rule': "line.split(':',1)[-1].strip()",
        'mult-value':True,
    },
]