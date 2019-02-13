# -*- coding:utf-8 -*-

import copy
from mod.tools import LogAnalze, Message, Template_Report, Debug, Check

@Debug.get_time_cost('[Debug] 分析端：')
def cbk_agent_report(queue1, rulelist, queue2, blk_rulelist):
    """
    Connected Backup 的 ZipAgent 日记分析模块
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

@Debug.get_time_cost('[Debug] 分析端：')
def cbk_agent_summary_csv(queue1, queue2):
    """
    Connected Backup 的 ZipAgent 日记分析模块, 本模块仅分析汇总信息
    :param queue1:
    :param queue2:
    :return:
    """

    # 初始化参数
    n = True

    while n:
        data = queue1.get()
        if data == False:
            n = False
        else:
            id = data.get('id')
            log_content = data.get('log_content')

            # 开始整理数据
            event_type = 'Information'
            event_time = ''
            event_status = ''
            agent_version = ''
            agent_account = ''
            event_level = ''
            event_error = ''
            event_warn = ''
            event_diag = ''
            backup_files = ''

            for log_content_list in log_content:
                log_line = log_content_list[0]
                log_content = log_content_list[1]

                # 结束标记
                if LogAnalze.match_start('-------------', log_content):
                    event_level = ''

                # Files 信息
                elif LogAnalze.match_start('Files\n', log_content):
                    event_level = 'Files'

                # Error 信息
                elif LogAnalze.match_start('Errors\n', log_content):
                    event_level = 'Error'

                # Warnings 信息
                elif LogAnalze.match_start('Warnings\n', log_content):
                    event_level = 'Warning'

                # Diagnostics 信息
                elif LogAnalze.match_start('Diagnostics\n', log_content):
                    event_level = 'Diagnostic'

                elif event_level != '':
                    if event_level == 'Files':
                        backup_files = backup_files + log_content.strip() + '\n'
                    elif event_level == 'Error':
                        event_error = event_error + log_content.strip() + '\n'
                    elif event_level == 'Warning':
                        event_warn = event_warn + log_content.strip() + '\n'
                    elif event_level == 'Diagnostic':
                        event_diag = event_diag + log_content.strip() + '\n'

                # Agent 版本
                elif LogAnalze.match_start('Connected Backup/PC Agent Version:', log_content):
                    agent_version = log_content.split(':')[-1].strip()

                # 账号 ID
                elif LogAnalze.match_start('Account Number:', log_content):
                    agent_account = log_content.split(':')[-1].strip()

                # 事件时间
                elif LogAnalze.match_any('\d{4}\/\d+\/\d+ \d+:\d+ - \d{4}\/\d+\/\d+ \d+:\d+', log_content):
                    event_time_list = log_content.split(' ', 6)
                    event_time = event_time_list[1] +' '+ event_time_list[2] +' '+ event_time_list[3] +' '+ event_time_list[4] +' '+ event_time_list[5]

                # 事件类型
                elif LogAnalze.match_any('Backup outcome:|Internal diagnostic outcome:', log_content):
                    event_type = log_content.split(':')[0]
                    event_status = log_content.split(':')[1]


