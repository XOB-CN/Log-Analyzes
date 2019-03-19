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
        # 位于 %OvDataDir%\log\System.txt
        'system\.txt',

        # jboss 相关日记
        'jboss7.*\.log',

        # gatway 日志
        'opr-gateway',
        'opr-gateway-flowtrace\.log',

        # DSP 日记
        'opr-backend\.log',
        'opr-ciresolver\.log',
        'opr-flowtrace-backend\.log',

        # MA(Monitoring Automation) 相关日记，位于 %TOPAZ_HOME%\log\jboss\
        'opr-webapp\.log',          # 分配/部署相关
        'opr-configserver\.log',    # MA 以及其它活动，包括 OMi web UIs, Content Pack import, Tool 的执行
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