# -*- coding:utf-8 -*-

import os
import copy
from mod.tools.match import Match
from mod.tools.check import Check
from mod.tools.template import Template_Report

def archive_general_report(Queue_Input, ruledict, Queue_Output, black_list):
    """
    针对压缩包的通用日记分析模块, 输出的数据格式为：{'id':id, 'logs':data_copy}
    :param Queue_Input: input 端放入的数据
    :param ruleldict: 包含 logs / other 这两部分列表的字典数据
    :param Queue_Output: 需要将处理完成的数据放入到消息队列中
    :param black_list: 黑名单列表, 匹配到的内容直接不匹配
    """
    # 初始化参数
    n = True
    tag_logs = False
    tag_other = False

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
            log_type = queue_data.get('type')
            filepath = queue_data.get('filepath')
            filename = os.path.split(filepath)[-1]
            log_data = queue_data.get('log_content')
            tmp_rule_logs = copy.deepcopy(ruledict.get('logs'))
            tmp_rule_other = copy.deepcopy(ruledict.get('other'))

            for logs in log_data:
                log_line = logs[0]
                log_index = filename + ' ' + log_line
                line = logs[1].strip()

                # 替换特殊字符 (用于能正确显示 html 内容)
                if '<' in line or '>' in line:
                    line = line.replace('<', '&lt;').replace('>', '&gt;')

                # 解析 ohter 类型日志, 通常是配置文件, 仅需要单行匹配即可
                if log_type == 'other':
                    tag_logs = False
                    tag_other = True

                    for rule in tmp_rule_other:
                        if Match.match_any(rule.get('match'), line):
                            cmd = rule.get('rule')
                            try:
                                rule['content'] = eval(cmd).strip()
                            except:
                                rule['content'] = line

                            tmp_log_line = rule.get('log_line')
                            if tmp_log_line == None:
                                rule['log_line'] = Template_Report.html_font(filepath, color='Green') + '<br>' +log_line
                                rule['detail'] = Template_Report.html_font(filename, color='Green') + ' ' + log_line + ' ' + line
                            else:
                                rule['log_line'] = tmp_log_line + ', ' + log_line
                                rule['detail'] = rule.get('detail') + "<br>" + Template_Report.html_font(filename, color='Green') + ' '+ log_line + ' ' + line

                # 解析 logs 类型日志, 需要多行匹配
                if log_type == 'logs':
                    tag_logs = True
                    tag_other = False

                    for rule in tmp_rule_logs:
                        # 多行匹配流程
                        if muline_match_str:
                            # 第一次匹配到 endmatch 中的内容
                            if Match.match_any(tmp_rule_logs[rule_list_idx].get('endmatch'), line) and muline_match_end == False:
                                muline_match_end = True
                                # 由于已经匹配到 endmatch 中的内容，所以数据肯定不为空
                                # 有一种可能情况，就是输入端分段的时候没有将多行匹配的内容完整的分成一段，这样会导致无法完成多行匹配
                                # 此时执行 except 中的代码，终止多行匹配流程，强制进入单行匹配流程
                                try:
                                    tmp_log_line = tmp_rule_logs[rule_list_idx].get('log_line')
                                    tmp_rule_logs[rule_list_idx]['log_line'] = tmp_log_line + ', ' + log_line
                                    tmp_rule_logs[rule_list_idx]['detail'] = tmp_rule_logs[rule_list_idx]['detail'].strip()+ "<br>" + log_index + ' ' + line
                                    break
                                except Exception as e:
                                    if Check.get_debug_level() in ['warn', 'debug']:
                                        tmp_rule_logs[rule_list_idx]['log_line'] = Template_Report.html_font(log_line)
                                        tmp_rule_logs[rule_list_idx]['detail'] = Template_Report.html_font('{n} 无法判断本行内容, 请自行检查, 请尝试调整配置文件中 segment_number 的值, 或者修改输入端的分段策略<br>'.
                                                                                                           format(n=log_index) + Template_Report.html_font(log_index) + ' ' + Template_Report.html_font(line))
                                    muline_match_str = False
                                    muline_match_end = False
                                    break

                            # 多次匹配到 endmatch 中的内容
                            elif Match.match_any(tmp_rule_logs[rule_list_idx].get('endmatch'), line) and muline_match_end == True:
                                # 直接录入数据就好，不需要做特殊处理
                                try:
                                    tmp_log_line = tmp_rule_logs[rule_list_idx].get('log_line')
                                    tmp_rule_logs[rule_list_idx]['log_line'] = tmp_log_line + ', ' + log_line
                                    tmp_rule_logs[rule_list_idx]['detail'] = tmp_rule_logs[rule_list_idx]['detail'].strip() + "<br>" + log_index + ' ' + line
                                    break
                                except Exception as e:
                                    if Check.get_debug_level() in ['warn', 'debug']:
                                        tmp_rule_logs[rule_list_idx]['log_line'] = Template_Report.html_font(log_line)
                                        tmp_rule_logs[rule_list_idx]['detail'] = Template_Report.html_font('{n} 无法判断本行内容, 请自行检查, 请尝试调整配置文件中 segment_number 的值, 或者修改输入端的分段策略<br>'.
                                                                                                           format(n=log_index)) + Template_Report.html_font(log_index) + ' ' + Template_Report.html_font(line)
                                    muline_match_str = False
                                    muline_match_end = False
                                    break

                            # 没有匹配到 endmatch, 但是多行匹配已经开启
                            elif Match.match_any(tmp_rule_logs[rule_list_idx].get('endmatch'), line) == False and muline_match_end == False:
                                try:
                                    tmp_log_line = tmp_rule_logs[rule_list_idx].get('log_line')
                                    tmp_rule_logs[rule_list_idx]['log_line'] = tmp_log_line + ', ' + log_line
                                    tmp_rule_logs[rule_list_idx]['detail'] = tmp_rule_logs[rule_list_idx]['detail'].strip() + "<br>" + log_index + ' ' + line
                                    break
                                except Exception as e:
                                    if Check.get_debug_level() in ['warn', 'debug']:
                                        tmp_rule_logs[rule_list_idx]['log_line'] = Template_Report.html_font(log_line)
                                        tmp_rule_logs[rule_list_idx]['detail'] = Template_Report.html_font('{n} 无法判断本行内容, 请自行检查, 请尝试调整配置文件中 segment_number 的值, 或者修改输入端的分段策略<br>'.
                                                                                                           format(n=log_index)) + Template_Report.html_font(log_index) + ' ' + Template_Report.html_font(line)
                                    muline_match_str = False
                                    muline_match_end = False
                                    break

                            # 代表上一行已经是该事件的最后一行，本行将要进入单行匹配流程
                            elif Match.match_any(tmp_rule_logs[rule_list_idx].get('endmatch'), line) == False and muline_match_end == True:
                                muline_match_str = False
                                muline_match_end = False

                        # 开启多行匹配
                        elif Match.match_any(rule.get('match'), line) and rule.get('endmatch') != None:
                            muline_match_str = True
                            rule_list_idx = tmp_rule_logs.index(rule)

                            # 常规规则：记录内容
                            tmp_log_line = rule.get('log_line')
                            if tmp_log_line == None:
                                rule['log_line'] = Template_Report.html_font(filepath, color='Green') + '<br>' + log_line
                                rule['detail'] = Template_Report.html_font(log_index, color='Green') + ' ' + line
                            else:
                                rule['log_line'] = tmp_log_line + ', ' + log_line
                                rule['detail'] = rule['detail'].strip() + "<br>" + Template_Report.html_font(log_index, color='Green') + ' ' + line
                            break

                        # 单行匹配流程
                        elif Match.match_any(rule.get('match'), line):
                            if rule.get('log_line') == None:
                                rule['log_line'] = Template_Report.html_font(filepath, color='Green') + '<br>' + log_line
                                rule['detail'] = Template_Report.html_font(log_index, color='Green') + ' ' + line
                                break
                            else:
                                rule['log_line'] = rule.get('log_line') + ', ' + log_line
                                rule['detail'] = rule.get('detail') + '<br>' + Template_Report.html_font(log_index, color='Green') + ' ' + line
                                # break 的作用是如果匹配到了相应的规则，则不再进行匹配，防止重复匹配的问题
                                break

            if tag_logs:
                data_copy = copy.deepcopy(tmp_rule_logs)
                tag_logs = False
                tag_other = False
            else:
                data_copy = copy.deepcopy(tmp_rule_other)
                tag_logs = False
                tag_other = False

            Queue_Output.put({'id':id, 'logs':data_copy})

        if n:
            pass
        else:
            pass

    Queue_Output.put(False)