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
        'match': "unexpected exception caught.*Origin.*UserController at line 105|ERROR ExceptionTranslatorImpl.* - Ambiguous method overloading for method",
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
        'name': 'odb boot（ucmdb）/ bsm_sdk_ucmdb_server.log / opr-script-host.log 显示下列错误时',
        'type': '产品 Bug',
        'match': "Failed to register listener due to following failure.*Authentication failed|gateway.*Failed to register listener due to following failure.*Customer not available",
        'solution': '请参考 QCCR1H119896<br>',
    },
    {
        'name': '升级到 OMi 10.71 后, LDAP login 失败',
        'type': '产品 Bug',
        'match': "ERROR DBLayerImpl\.getCountOfSettingValue.*Fail to get getContextResultSet.*unique Domain:ldap\.unique\.domain\.name",
        'solution': '该问题应该在 &lt;TOPAZ_HOME&gt;/log/jboss/setting.log 中能被发现<br>'
                    '修复请参考 QCCR8D107613<br>',
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
        'type': 'OA Error ID',
        'match': "OpC30-36|OpC40-1905|OpC40-1906|OpC30-100|サーバーに障害があります。OVO メッセージ レシーバへの|WRN.*Forwarding message/action response to OVO message",
        'solution': 'OMU 服务器上的心跳轮询 (HBP, Heartbeat polling) 有时会检测到以下错误：<br>' 
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
                    '- 只要在代理上实际发生缓冲，就不能避免 HBP 进行缓冲检测 (OpC40-1905/OpC40-1906)<br>'
                    '- OpC30-100 一般代表着 OA 已不再缓存信息',
    },
    {
        'name': 'odb 日志（ucmdb）显示删除 row 的请求',
        'type': '其它已知问题',
        'match': "failed removing row.*please delete it manually",
        'solution': '停止所有服务，然后执行下列命令 (如果嵌入了postgres，则只启动DB，对于其他postgres，只需登录到它们的SQL提示符即可)<br>'
                    '&ensp;delete from rtsm.ha_writer;<br>'
                    '&ensp;delete from rtsm.jgroupsping;<br>'
                    '&ensp;commit;<br>'
                    '重启所有服务',
    },
    {
        'name': 'odb 日志（ucmdb）显示缺失 encryption.bin 和 cmdbSuperIntegrationCredentials.bin',
        'type': '其它已知问题',
        'match': "Can't read the encryption file.*encryption.bin|Can't read the superIntegrationUser credentials file",
        'solution': '停止所有服务<br>'
                    '导航到&lt;Unzipped_Install_Media_Dir&gt;/Software/packages<br>'
                    '重新安装名为“HPBsmRTSMGw*.[msi|rpm]”的安装包<br>'
                    '如果是 linux, 执行 rpm -ivh HPBsmRTSMGw* --force --nodeps<br>'
                    '重启所有服务',
    },
    {
        'name': '升级到 OMi 10.7x 后, DB backup-restore/schema-registration 步骤失败：citing missing UCMDB files',
        'type': '其它已知问题',
        'match': "lib folder C:.HPBSM.ucmdb.lib does not exist",
        'solution': '问题描述<br>'
                    '这个错误应该在&lt;TOPAZ_HOME&gt;/log/upgrade/upgrade.wizard.log 中能看到<br>'
                    '这很可能是因为在新OMi版本的安装阶段，由于磁盘空间不足，导致UCMDB安装失败<br>'
                    '虽然实际安装完成时屏幕上没有明显的错误，但是&lt;TOPAZ_HOME&gt;/log/configserver/postinstall_all.log 应该会显示以下错误<br>'
                    'Windows 内容<br>'
                    '&ensp;ERROR - Failed to install ucmdb. Exit code -1<br>'
                    '&ensp;Possibly there is not enough disk space available. Check installation output in %localappdata%/Temp/1 or %localappdata%/Temp/2<br>'
                    'Linux 内容<br>'
                    '&ensp;WARNING: /tmp does not have enough disk space! Attempting to use /root for install base and tmp dir.<br>'
                    '&ensp;WARNING! The amount of /root disk space required to perform this installation is greater than what is available<br>'
                    '&ensp;ERROR - Failed to install ucmdb. Exit code 12<br>'
                    '解决方法<br>'
                    '&ensp;确保磁盘上至少有 15-20 GB 的剩余空间，否则，导出 IATEMPDIR 和_JAVA_OPTIONS 来指向具有足够空间的驱动器',
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