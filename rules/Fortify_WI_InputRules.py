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
        # log 类型的日志信息
        'Framework\.log',
        'Scanner\.log',
        'StateRequestor\.log',
        'Client\.log',
        'Memory\.log',
        'FailedRequests\.log',
        'Statistics\.log',
        'Crawl\.log',
        'WebInspectWCFService\.log',
        'Error\.log',
        'Scanner\.log',
        'App\.log',
        'RejectManager\.log',
        'Proxy\.log',

    ],
    # 其余类型
    'other':[
        # 信息搜集
        'Audit\.log',
        'ScanLog\.log',
    ],
}

# 内容黑名单，匹配到的内容直接忽略，不匹配
black_list = [
    # eg:如果该行包括 content 则直接忽略
    # 'content',

    # Client.log
    'Process browser with pId.*was killed',
    'App.Main - entering Main',
    'App.Main - exiting Main',
    # Crawl.log
    'SPI.Scanners.Web.Crawl.Crawler in getIncludeResponse, request rejected, returning null',
    # Framework.log
    'SPI.Scanners.Web.Framework.Scan entering Scan()',
    'SPI.Scanners.Web.Framework.Scan exiting Scan()',
    # Memory.log
    'HandleOutOfMemoryExceptionCount.0',        # 处理内存异常数：0
    'SPI.Utils.Memory.MemoryMonitor starting memory monitor',       # 内存监控开始，没有实际意义
    'SPI.Utils.Memory.MemoryMonitor in timerCallback',
    'SPI.Diagnostics.GCUtils.*forceGCInternal',
    # Proxy.log
    'SPI.Net.Proxy.RequestReaderThreadPool in startThreadsIfNecessary.*MaximumConcurrency:.*',      # 感觉没啥用
    'SPI.Net.Proxy.RequestReaderThreadPool in Stop.*PoolName.*MaximumConcurrency:.*',               # 感觉没啥用
    'SPI.Net.Proxy.RequestReaderThreadPool entering Stop',      # 代理停止，目前看应该不是核心问题
    # Statistic.log
    'SPI.Scanners.Web.Statistics.ScanStatisticsWriter exiting _writerThreadProc, maxCount:',
]