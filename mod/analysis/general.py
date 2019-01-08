# -*- coding:utf-8 -*-

import re, copy
from mod.tools import LogAnalze, Message

def general_report(queue1, rulelist, queue2):
    """
    通用的日记分析模块；
    会将处理的结果放到 queue2 队列中，数据格式为：{'id':section_id, 'logs':列表数据，内部是字典}
    """
    # 初始化参数
    n = True
    tmp_rule_list = copy.deepcopy(rulelist)

    # 多行匹配参数
    rule_list_idx = 0
    muline_match_str = False
    muline_match_end = False

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

                    # 多行匹配流程
                    if muline_match_str:
                        # 第一次匹配到 endmatch 中的内容
                        if LogAnalze.match_any(tmp_rule_list[rule_list_idx].get('endmatch'), line) and muline_match_end == False:
                            muline_match_end = True
                            # 由于已经匹配到 endmatch 中的内容，所以数据肯定不为空
                            # 有一种可能情况，就是输入端分段的时候没有将多行匹配的内容完整的分成一段，这样会导致无法完成多行匹配
                            # 此时执行 except 中的代码，终止多行匹配流程，强制进入单行匹配流程
                            try:
                                tmp_log_line = tmp_rule_list[rule_list_idx].get('log_line')
                                tmp_rule_list[rule_list_idx]['log_line'] = tmp_log_line + ', ' + log_data[0]
                                tmp_rule_list[rule_list_idx]['detail'] = tmp_rule_list[rule_list_idx]['detail'].strip() + "<br>" + log_data[0] + ' ' + line.strip()
                                break
                            except Exception as e:
                                # tmp_rule_list[rule_list_idx]['log_line'] = '<font color="red">' + log_data[0] + '</font>'
                                # tmp_rule_list[rule_list_idx]['detail'] = '<font color="red">' + log_data[0] + ' ' + log_data[1] + '</font>'
                                muline_match_str = False
                                muline_match_end = False
                                break

                        # 多次匹配到 endmatch 中的内容
                        elif LogAnalze.match_any(tmp_rule_list[rule_list_idx].get('endmatch'), line) and muline_match_end == True:
                            # 直接录入数据就好，不需要做特殊处理
                            try:
                                tmp_log_line = tmp_rule_list[rule_list_idx].get('log_line')
                                tmp_rule_list[rule_list_idx]['log_line'] = tmp_log_line + ', ' + log_data[0]
                                tmp_rule_list[rule_list_idx]['detail'] = tmp_rule_list[rule_list_idx]['detail'].strip() + "<br>" + log_data[0] + ' ' + line.strip()
                                break
                            except Exception as e:
                                # tmp_rule_list[rule_list_idx]['log_line'] = '<font color="red">' + log_data[0] + '</font>'
                                # tmp_rule_list[rule_list_idx]['detail'] = '<font color="red">' + log_data[0] + ' ' + log_data[1] + '</font>'
                                muline_match_str = False
                                muline_match_end = False
                                break

                        # 没有匹配到 endmatch, 但是多行匹配已经开启
                        elif LogAnalze.match_any(tmp_rule_list[rule_list_idx].get('endmatch'), line) == False and muline_match_end == False:
                            # 直接录入数据就好，不需要做特殊处理
                            try:
                                tmp_log_line = tmp_rule_list[rule_list_idx].get('log_line')
                                tmp_rule_list[rule_list_idx]['log_line'] = tmp_log_line + ', ' + log_data[0]
                                tmp_rule_list[rule_list_idx]['detail'] = tmp_rule_list[rule_list_idx]['detail'].strip() + "<br>" + log_data[0] + ' ' + line.strip()
                                break
                            except Exception as e:
                                # tmp_rule_list[rule_list_idx]['log_line'] = '<font color="red">' + log_data[0] + '</font>'
                                # tmp_rule_list[rule_list_idx]['detail'] = '<font color="red">' + log_data[0] + ' ' + log_data[1] + '</font>'
                                muline_match_str = False
                                muline_match_end = False
                                break

                        # 代表上一行已经是该事件的最后一行，本行将要进入单行匹配流程
                        elif LogAnalze.match_any(tmp_rule_list[rule_list_idx].get('endmatch'), line) == False and muline_match_end == True:
                            muline_match_str = False
                            muline_match_end = False

                    # 开启多行匹配
                    elif LogAnalze.match_any(rule.get('match'), line) and rule.get('endmatch') != None:
                        muline_match_str = True
                        rule_list_idx = tmp_rule_list.index(rule)

                        # 常规规则：记录内容
                        tmp_log_line = rule.get('log_line')
                        if tmp_log_line == None:
                            rule['log_line'] = log_data[0]
                            rule['detail'] = log_data[0] + ' ' + line.strip()
                            break
                        else:
                            rule['log_line'] = tmp_log_line + ', ' + log_data[0]
                            rule['detail'] = rule['detail'].strip() + "<br>" + log_data[0] + ' ' + line.strip()
                            break

                    # 单行匹配流程
                    elif LogAnalze.match_any(rule.get('match'), line):
                        # 特殊规则：搜集信息
                        if rule.get('type') == 'Information' or rule.get('type') == 'Others':
                            cmd = rule.get('rule')
                            rule['content'] = eval(cmd).strip()
                        # 常规规则：记录内容
                        tmp_log_line = rule.get('log_line')
                        if tmp_log_line == None:
                            rule['log_line'] = log_data[0]
                            rule['detail'] = log_data[0] + ' ' + line.strip()
                        else:
                            rule['log_line'] = tmp_log_line + ', ' + log_data[0]
                            rule['detail'] = rule['detail'].strip() + "<br>" + log_data[0] + ' ' + line.strip()

            # rulelist_copy 是列表数据，内部元素皆为字典
            rulelist_copy = copy.deepcopy(tmp_rule_list)
            tmp_rule_list = copy.deepcopy(rulelist)

            # {'id':section_id, 'logs':列表数据，内部是字典}
            Message.info_message('分析端：已分析完第{n}段日记'.format(n=id))
            queue2.put({'id':id, 'logs':rulelist_copy})

    queue2.put(False)