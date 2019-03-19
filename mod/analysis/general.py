# -*- coding:utf-8 -*-

import copy

def archive_general_report(Queue_Input, ruledict, Queue_Output, black_list):
    """
    针对压缩包的通用日记分析模块
    :param Queue_Input: input 端放入的数据
    :param ruleldict: 包含 logs / other 这两部分列表的字典数据
    :param Queue_Output: 需要将处理完成的数据放入到消息队列中
    :param black_list: 黑名单列表, 匹配到的内容直接不匹配
    """
    # 初始化参数
    n = True
    tmp_rule_dict = copy.deepcopy(ruledict)

    # 多行匹配参数
    rule_list_idx = 0
    muline_match_str = False
    muline_match_end = False

    while n:
        queue_data = Queue_Input.get()
        if queue_data == False:
            n = False
        else:
            # {'section_id': section_id, 'type': 'logs', 'filepath': filepath, 'log_content': log_content_copy})
            id = queue_data.get('section_id')
            type = queue_data.get('type')
            filepath = queue_data.get('filepath')
            log_data = queue_data.get('log_content')

            for logs in log_data:
                log_line = logs[0]
                log_content = logs[1]

                # 解析 ohter 类型日志, 通常是配置文件, 仅需要单行匹配即可
                if type == 'other':
                    print(log_content)