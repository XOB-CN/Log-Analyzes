# -*- coding:utf-8 -*-

import re, copy
from mod.tools import LogAnalze

def general_report(queue1, rulelist, queue2):
    """
    通用的日记分析模块；
    会将处理的结果放到 queue2 队列中，数据格式为：{'id':section_id, 'logs':列表数据，内部是字典}
    """
    # 初始化参数
    n = True
    tmp_rule_list = copy.deepcopy(rulelist)

    # 开始读取数据
    while n:
        queue_data = queue1.get()
        if queue_data == False:
            n = False
        else:
            # queue_data:{'id':section_id, 'logs':'log_content'}
            id = queue_data.get('id')
            logs = queue_data.get('logs')

            for log_data in logs:
                line = log_data[1]
                for rule in tmp_rule_list:
                    # 单行匹配流程
                    if LogAnalze.match_any(rule.get('match'), line):
                        # 特殊规则：搜集信息
                        if rule.get('type') == 'Information' or rule.get('type') == 'Others':
                            cmd = rule.get('rule')
                            rule['content'] = eval(cmd).strip()
                        # 常规规则：记录内容
                        tmp_log_line = rule.get('log_line')
                        if tmp_log_line == None:
                            rule['log_line'] = log_data[0]
                            rule['detail'] = log_data[0] + ' ' + line
                        else:
                            rule['log_line'] = tmp_log_line + ', ' + log_data[0]
                            rule['detail'] = rule['detail'] + "<br>" + log_data[0] + ' ' + line.strip()

            # rulelist_copy 是列表数据，内部元素皆为字典
            rulelist_copy = copy.deepcopy(tmp_rule_list)
            tmp_rule_list = copy.deepcopy(rulelist)

            # {'id':section_id, 'logs':列表数据，内部是字典}
            queue2.put({'id':id, 'logs':rulelist_copy})

    queue2.put(False)