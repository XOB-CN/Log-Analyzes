# -*- coding:utf-8 -*-

import copy
from mod.tools import LogAnalze, Message, Debug

@Debug.get_time_cost('[Debug] 分析端：')
def cbk_agent_report(queue1, rulelist, queue2):
    """
    Connected Backup 的 ZipAgent 日记分析模块
    :param queue1: input 端放入的数据
    :param rulelist: 匹配列表
    :param queue2: 需要将处理完成的数据放入到消息队列中，数据格式：
    """
    n = True
    tmp_rule_list = copy.deepcopy(rulelist)

    while n:
        queue_data = queue1.get()
        if queue_data == False:
            n = False
        else:
            id = queue_data.get('id')                       # 分段ID
            log_class = queue_data.get('log_class')         # 日记的分类
            filename = queue_data.get('filename')           # 日记的文件名
            log_content = queue_data.get('log_content')     # 日记的内容，包括行数和内容

            for line_id, line in log_content:
                for rule in tmp_rule_list:
                    # 单行匹配流程
                    if LogAnalze.match_any(rule.get('match'), line):
                        if rule.get('log_line') == None:
                            rule['log_line'] = filename + ' ' + line_id
                            rule['content'] = line
                            rule['log_class'] = log_class
                        else:
                            rule['log_line'] = rule.get('log_line') + ', ' + filename + ' ' + line_id
                            rule['content'] = rule.get('content') + '<br>' + line

        # rulelist_copy 是列表数据，内部元素皆为字典
        rulelist_copy = copy.deepcopy(tmp_rule_list)
        tmp_rule_list = copy.deepcopy(rulelist)

        # {'id':id, 'logs':列表数据，内部是字典}
        # 此处添加一个判断 n 的原因是，如果分析进程直接获取的结果是 False, 则直接放入 False
        if n:
            Message.info_message('[Info] 分析端：已分析完第 {n} 段日记'.format(n=id))
            queue2.put({'id': id, 'logs': rulelist_copy})
        else:
            Message.info_message('[Info] 分析端：已经没有待分析的数据了')

    queue2.put(False)