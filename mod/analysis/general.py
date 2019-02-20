# -*- coding:utf-8 -*-

import re, copy
from mod.tools import Check, LogAnalze, Template_Report, Message
from mod.tools import Debug

@Debug.get_time_cost('[Debug] 分析端：')
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
                                if Check.get_debug_level() in ['warn', 'debug']:
                                    tmp_rule_list[rule_list_idx]['log_line'] = Template_Report.html_font(log_data[0])
                                    tmp_rule_list[rule_list_idx]['detail'] = Template_Report.html_font('{n} 无法判断本行内容, 请自行检查, 请尝试调整配置文件中 segment_number 的值, 或者修改输入端的分段策略<br>'.format(n=log_data[0])) + \
                                                                             Template_Report.html_font(log_data[0]) + ' ' + Template_Report.html_font(log_data[1])
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
                                if Check.get_debug_level() in ['warn', 'debug']:
                                    tmp_rule_list[rule_list_idx]['log_line'] = Template_Report.html_font(log_data[0])
                                    tmp_rule_list[rule_list_idx]['detail'] = Template_Report.html_font('{n} 无法判断本行内容, 请自行检查, 请尝试调整配置文件中 segment_number 的值, 或者修改输入端的分段策略<br>'.format(n=log_data[0])) + \
                                                                             Template_Report.html_font(log_data[0]) + ' ' + Template_Report.html_font(log_data[1])
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
                                if Check.get_debug_level() in ['warn', 'debug']:
                                    tmp_rule_list[rule_list_idx]['log_line'] = Template_Report.html_font(log_data[0])
                                    tmp_rule_list[rule_list_idx]['detail'] = Template_Report.html_font('{n} 无法判断本行内容, 请自行检查, 请尝试调整配置文件中 segment_number 的值, 或者修改输入端的分段策略<br>'.format(n=log_data[0])) + \
                                                                             Template_Report.html_font(log_data[0]) + ' ' + Template_Report.html_font(log_data[1])
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
                            try:
                                rule['content'] = eval(cmd).strip()
                            except:
                                rule['content'] = line.strip()
                                Message.warn_message('[Warn] 分析端：无法获取指定的值，请检查规则设定')

                        # 常规规则：记录内容
                        tmp_log_line = rule.get('log_line')
                        if tmp_log_line == None:
                            rule['log_line'] = log_data[0]
                            rule['detail'] = log_data[0] + ' ' + line.strip()
                        else:
                            rule['log_line'] = tmp_log_line + ', ' + log_data[0]
                            rule['detail'] = rule['detail'].strip() + "<br>" + log_data[0] + ' ' + line.strip()

                        # break 的作用是如果匹配到了相应的规则，则不再进行匹配，防止重复匹配的问题
                        break

            # rulelist_copy 是列表数据，内部元素皆为字典
            rulelist_copy = copy.deepcopy(tmp_rule_list)
            tmp_rule_list = copy.deepcopy(rulelist)

            # {'id':section_id, 'logs':列表数据，内部是字典}
            Message.info_message('[Info] 分析端：已分析完第 {n} 段日记'.format(n=id))
            queue2.put({'id':id, 'logs':rulelist_copy})

    queue2.put(False)

@Debug.get_time_cost('[Debug] 分析端：')
def archive_general_report(queue1, rulelist, queue2, blk_rulelist):
    """
    针对压缩包的通用日记分析模块
    :param queue1: input 端放入的数据
    :param rulelist: 匹配列表
    :param queue2: 需要将处理完成的数据放入到消息队列中
    :param blk_rulelist: 黑名单列表, 匹配到的内容直接不匹配
    """
    n = True
    tmp_rule_list = copy.deepcopy(rulelist)

    # 多行匹配参数
    rule_list_idx = 0
    muline_match_str = False
    muline_match_end = False

    while n:
        queue_data = queue1.get()
        if queue_data == False:
            n = False
        else:
            id = queue_data.get('id')                       # 分段ID
            filename = queue_data.get('filename')           # 日记的文件名
            log_content = queue_data.get('log_content')     # 日记的内容，包括行数和内容

            for line_id, line in log_content:
                # 初始化变量
                log_index = filename + ' ' + line_id
                black_rule = True

                # 替换特殊字符 (用于能正确显示 html 内容)
                if '<' in line or '>' in line:
                    line = line.replace('<','&lt;').replace('>','&gt;')

                # 黑名单规则
                for blk_rule in blk_rulelist:
                    if LogAnalze.match_any(blk_rule, line):
                        black_rule = False

                if black_rule:
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
                                    tmp_rule_list[rule_list_idx]['log_line'] = tmp_log_line + ', ' + line_id
                                    tmp_rule_list[rule_list_idx]['detail'] = tmp_rule_list[rule_list_idx]['detail'].strip() + "<br>" + log_index + ' ' + line.strip()
                                    break
                                except Exception as e:
                                    if Check.get_debug_level() in ['warn', 'debug']:
                                        tmp_rule_list[rule_list_idx]['log_line'] = Template_Report.html_font(line_id)
                                        tmp_rule_list[rule_list_idx]['detail'] = Template_Report.html_font('{n} 无法判断本行内容, 请自行检查, 请尝试调整配置文件中 segment_number 的值, 或者修改输入端的分段策略<br>'.format(n=log_index)) + \
                                                                                 Template_Report.html_font(log_index) + ' ' + Template_Report.html_font(line.strip())
                                    muline_match_str = False
                                    muline_match_end = False
                                    break

                            # 多次匹配到 endmatch 中的内容
                            elif LogAnalze.match_any(tmp_rule_list[rule_list_idx].get('endmatch'), line) and muline_match_end == True:
                                try:
                                    tmp_log_line = tmp_rule_list[rule_list_idx].get('log_line')
                                    tmp_rule_list[rule_list_idx]['log_line'] = tmp_log_line + ', ' + line_id
                                    tmp_rule_list[rule_list_idx]['detail'] = tmp_rule_list[rule_list_idx]['detail'].strip() + "<br>" + log_index + ' ' + line.strip()
                                    break
                                except Exception as e:
                                    if Check.get_debug_level() in ['warn', 'debug']:
                                        tmp_rule_list[rule_list_idx]['log_line'] = Template_Report.html_font(line_id)
                                        tmp_rule_list[rule_list_idx]['detail'] = Template_Report.html_font('{n} 无法判断本行内容, 请自行检查, 请尝试调整配置文件中 segment_number 的值, 或者修改输入端的分段策略<br>'.format(n=log_index)) + \
                                                                                 Template_Report.html_font(log_index) + ' ' + Template_Report.html_font(line.strip())
                                    muline_match_str = False
                                    muline_match_end = False
                                    break

                            # 没有匹配到 endmatch, 但是多行匹配已经开启
                            elif LogAnalze.match_any(tmp_rule_list[rule_list_idx].get('endmatch'), line) == False and muline_match_end == False:
                                try:
                                    tmp_log_line = tmp_rule_list[rule_list_idx].get('log_line')
                                    tmp_rule_list[rule_list_idx]['log_line'] = tmp_log_line + ', ' + line_id
                                    tmp_rule_list[rule_list_idx]['detail'] = tmp_rule_list[rule_list_idx]['detail'].strip() + "<br>" + log_index + ' ' + line.strip()
                                    break
                                except Exception as e:
                                    if Check.get_debug_level() in ['warn', 'debug']:
                                        tmp_rule_list[rule_list_idx]['log_line'] = Template_Report.html_font(line_id)
                                        tmp_rule_list[rule_list_idx]['detail'] = Template_Report.html_font('{n} 无法判断本行内容, 请自行检查, 请尝试调整配置文件中 segment_number 的值, 或者修改输入端的分段策略<br>'.format(n=log_index)) + \
                                                                                 Template_Report.html_font(log_index) + ' ' + Template_Report.html_font(line.strip())
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
                                rule['log_line'] = Template_Report.html_font(filename, color='Green') + '<br>' + line_id
                                rule['detail'] = Template_Report.html_font(log_index, color='Green') + ' ' + line.strip()

                            else:
                                rule['log_line'] = tmp_log_line + ', ' + line_id
                                rule['detail'] = rule['detail'].strip() + "<br>" + Template_Report.html_font(log_index, color='Green') + ' ' + line.strip()
                            break

                        # 单行匹配流程
                        elif LogAnalze.match_any(rule.get('match'), line):
                            # 特殊规则：搜集信息
                            if rule.get('type') == 'Information' or rule.get('type') == 'Others':
                                cmd = rule.get('rule')
                                try:
                                    rule['content'] = eval(cmd).strip()
                                except:
                                    rule['content'] = line.strip()
                                    Message.warn_message('[Warn] 分析端：无法获取指定的值，请检查规则设定')

                            if rule.get('log_line') == None:
                                rule['log_line'] = Template_Report.html_font(filename, color='Green') + '<br>' + line_id
                                rule['detail'] = Template_Report.html_font(log_index, color='Green') + ' ' + line
                                break
                            else:
                                rule['log_line'] = rule.get('log_line') + ', ' + line_id
                                rule['detail'] = rule.get('detail') + '<br>' + Template_Report.html_font(log_index, color='Green') + ' ' + line
                                # break 的作用是如果匹配到了相应的规则，则不再进行匹配，防止重复匹配的问题
                                break

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