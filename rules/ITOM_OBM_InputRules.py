# -*- coding:utf-8 -*-

"""
如果匹配到下列列表中的规则，则本行不能被分段
match_start: 从行首开始匹配
match_end: 从行尾开始匹配
match_any: 利用正则表达式，全行任意位置匹配
"""
match_start=[]
match_end=[]
match_any=[]

# 需要分析的文件字典
need_files = {
    # 日志类型
    'logs':[
        # LCore 和 Operations Agent 的日志文件
        'system\.txt',                  # %OvDataDir%\log\System.txt

        # 心跳（heartbeat）相关
        'opr-heartbeat\.log',           # <OMi_HOME>\log\wde\opr-heartbeat.log 和 <OMi_HOME>\log\opr-backend\opr-heartbeat.log

        # Data Processing 事件流程
        # Gateway Server
          # <OMi_HOME>\log\wde\opr-gateway.log
          # <OMi_HOME>\log\wde\opr-gateway-flowtrace.log
          # <OMi_HOME>\log\opr-scripting-host\opr-scripting-host.log
        # Data Processing Server
          # <OMi_HOME>\log\opr-backend\opr-backend.log
          # <OMi_HOME>\log\opr-backend\opr-flowtrace-backend.log
          # <OMi_HOME>\log\opr-backend\opr-ciresolver.log
          # <OMi_HOME>\log\opr-scripting-host\opr-scripting-host.log
          # <OMi_HOME>\log\opr-scripting-host\scripts.log
        'opr-gateway\.log',             # OBM Gateway processing 日志，检查 OBM 是否接收到新事件或更改后的事件
        'opr-gateway-flowtrace\.log',   # 到达 Gateway 的事件和事件更改的 Flowtrace 日志条目
        'opr-scripting-host\.log',      # 自定义操作，外部事件处理（External event processing），外部指令文本查找（External instruction text lookup）

        'opr-backend\.log',             # OBM backend process，检查 OBM 是否处理新事件或已更改的事件
        'opr-flowtrace-backend\.log',   # 来自 OBM 网关进程的事件的 Flowtrace 日志条目
        'opr-ciresolver\.log',          # OBM backend process CI resolution
        'opr-scripting-host.log',       # EPI processing
        'scripts\.log',                 # EPI script errors

        # MA (Monitoring Automation) 相关
        # Gateway Server
          # <OMi_HOME>\log\jboss\opr-webapp.log
          # <OMi_HOME>\log\jboss\opr-configserver.log
        'opr-webapp\.log',              # OBM Web UI 的日志文件，监控自动化（Monitoring Automation），内容包导入，工具执行
        'opr-configserver\.log',        # Monitoring Automation 以及其它活动，包括 OMi web UIs, Content Pack import, Tool 的执行

        # 用户/登陆
        # Gateway Server
          # <OMi_HOME>\log\jboss\login.log
          # <OMi_HOME>\log\jboss\UserActions.servlets.log
        'login\.log',                   # LDAP, LWSSO
        'UserActions.servlets\.log',    # Log-in attempts（尝试登陆）

        # jboss (MercuryAS) 相关
        # Gateway Server
          # <OMi_HOME>\log\jboss7_boot.log
          # <OMi_HOME>\log\jboss\* -->  # Jboss (MercuryAS) Application Server log files
        'jboss7_boot\.log',             # Jboss (MercuryAS) start-up log file
        'content-manager\.log',         # 内容管理器功能（Content Manager functionality）
        'kes\.contentpack\.log',        # 内容管理器功能（Content Manager functionality）
        'downtime\.log',                # Downtime
        'opr-ue\.log',                  # User Engagement（用户参与）


        # Tomcat 部分
        # Gateway Server
          # <OMi_HOME>\log\wde\*  -->   # Tomcat (wde) log files
        
        # opr-* Command-Line Interfaces
        # Gateway Server
          # <OMi_HOME>\log\opr-clis.log
        'opr-clis.log',                 # opr-* Command-Line Interfaces
    ],
    # 其余类型
    'other':[
        # 测试规则
        'system\.txt',
    ],
}

# 内容黑名单，匹配到的内容直接忽略，不匹配
black_list = [
    # eg:如果该行包括 content 则直接忽略
    # 'content',
]