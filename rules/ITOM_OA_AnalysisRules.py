# -*- coding:utf-8 -*-

# 分析模块规则匹配库
# 注意：如果想要匹配 < 或 >, 则匹配的规则需要替换为 &lt; 或 &gt;
# 注意：如果想要显示空格，需要写 &ensp;
log_rules_list = [
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
        'name': 'OpC30-797 - OA 在处理 Policy 时发生了错误',
        'type': 'OA Error ID',
        'match': "OpC30-797|OpC30-724|OpC30-761|OpC30-760|OpC30-3400|Can't locate.*in @INC \(@INC contains",
        'solution': '请参考 KM1208518'
                    'OpC30-797 报错仅仅说明 OA 在处理一个 Policy 时发生了错误，但是具体问题需要具体分析<br>'
                    '<br>可能情况 - coda 未完成初始化 - KM433328<br>'
                    '&ensp;- 出现 OpC30-797, OpC30-724, OpC30-761, OpC30-760<br>'
                    '&ensp;- 原因：OA 在启动的过程中，Coda Agent 将经历一个初始化阶段，在此期间它无法响应请求，如果此时连接 Coda，就会出现上述错误代码<br>'
                    '&ensp;- 解决：一般不需要处理，会自动恢复<br>'
                    '&ensp;--- OA 会尝试多次连接 coda，也可以使用 ovconfchg -ns eaagt -set FAILED_COLLECTION_RETRIES 5 命令将尝试次数调整到 5 次（默认为 3 次）<br>'
                    '&ensp;--- OA 如果长时间无法连接 Coda，可能会报出 OpC30-3400 错误，可以使用 ovconfchg -ns eaagt -set FAILED_POLICY_TIME_TO_REACTIVATE 8 命令来减小重试间隔的时间（默认为 24h）<br>'
                    '<br>可能情况 - Perl 脚本问题<br>'
                    "&ensp;- 出现 Can't locate *** in @INC (@INC contains 这样的报错内容<br>"
                    '&ensp;- 原因：Perl 脚本无法找到对应的文件，一般是环境变量出现了问题<br>'
                    '&ensp;- 解决：请尝试添加环境变量<br>',
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
        'name': 'OpC30-613/OpC20-37 - Unknown monitor DBSPI-xxxx',
        'type': 'OA Error ID',
        'match': "DBSPI-.*OpC30-613|DBSPI-.*OpC20-37",
        'solution': '详细内容请参考 KM1226922<br>'
                    '当 DBSPI 收集器发出对度量标准 xxxx 的 opcmon 调用时，相应的 DBSPI-xxxx 模板尚未分配给受管节点，此时就会记录该警告信息<br>'
                    'SPI for Databases 使用两组策略进行正常操作<br>'
                    '- Scheduled Task policies<br>'
                    '- Measurement Threshold policies<br>'
                    '解决办法是需要确保将正确的“测量阈值”策略部署到受管节点，或者如果不需要收集该策略，则会从每个“计划任务”策略中删除该度量标准<br>',
    },
    {
        'name': 'OpC30-613/OpC20-37/OpC30-3404',
        'type': 'OA Error ID',
        'match': "OpC30-613|OpC20-37|OpC30-3404|opcmon の値を受信しないうちに、ポリシー.*の最大待ち時間に達しました",
        'solution': '问题原因<br>'
                    '- OpC30-613/OpC20-37 一般指 OA 收到了一个 policy named 的值，但是这个 policy 并没有部署在此节点上，所以 OA 会忽略这个接收到的值<br>'
                    '- OpC30-3404 一般指 OA 没有收到此 policy 的值，所以 OA 认为应提供此值的脚本未正确运行<br>'
                    '- policy name 可以在这些报错内容中找到, 如果这两个 policy name 不一样，可能是因为重命名过<br><br>'
                    '解决思路<br>'
                    '- 在重命名策略时，还应确保 policy  调用的脚本将值返回到新策略名称<br>'
                    '- 可以在 Program parameters 框中，检查配置的脚本参数<br>'
                    '- 如果日志中没有 OpC30-3404，那么很可能该 policy 已经被删除掉，那么可以考虑使用下列方法来处理<br>'
                    '&ensp;&ensp;# 清除缓存<br>'
                    '&ensp;&ensp;&ensp;&ensp;/opt/OV/bin/opcagt -cleanstart<br>'
                    '&ensp;&ensp;# 重启 OA<br>'
                    '&ensp;&ensp;&ensp;&ensp;ovc -kill<br>'
                    '&ensp;&ensp;&ensp;&ensp;ovc -start<br><br>'
                    '参考资料<br>'
                    'KM00709940 - 很有参考意义的一个KM<br>'
                    'SD02447785',
    },
    {
        'name': 'Perl 脚本执行时发生超时',
        'type': 'Perl Script',
        'match': 'perl.*に対する実行でタイムアウトが発生しました',
        'solution': '可能原因<br>'
                    '- 考虑 Perl 在执行中发生崩溃，请检查系统日志，应该会有相应的记录信息，必要时可以考虑搜集 OA 的 trace 信息',
    },
    {
        'name': '其余 Warn 信息',
        'type': 'Others',
        'match': "Wrn|Warn",
        'rule': "line",
    },
    {
        'name': '其余 Error 信息',
        'type': 'Others',
        'match': "Err|失敗",
        'rule': "line",
    },
]

other_rule_list = [
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
]