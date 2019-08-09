# -*- coding:utf-8 -*-

import copy
from mod.tools.check import Check
from mod.tools.debug import Debug
from mod.tools.match import Match
from mod.tools.message import Message
msg = Message()

@Debug.get_time_cost('[debug] 输入端 - 运行的总耗时：')
def archive_general(file_abspath_dict, Queue_Input, InputRule, input_argv):
    """
    通用的输入端读取日志，不需要处理日志的排序问题
    :param file_abspath_dict: 包含需要分析的文件列表，按照字典进行分类
    :param Queue_Input: 将预读取完成的数据放到 Queue_Input 中
    :param InputRule: 类型是字典数据
    :param input_argv: 可选的过滤规则，可以进一步过滤 file_abspath_dict.get('logs') 中的内容，例如使用时间来过滤
    :return:
    """

    # 初始化变量
    section_id = 0 # 记录分段的个数序号，用于记录顺序
    section_line = 0  # 记录每段内容的行数
    src_log_line = 0  # 记录原始日记的行数
    log_content = []  # 存放初步整理的数据
    def_encoding = Check.get_def_encoding()  # 获取配置文件中的默认编码

    # 由于 other 类型的日志内容一般都是配置文件信息，所以将读取后的文件内容处理后发送到 Queue_Input 即可
    for filepath in file_abspath_dict.get('other'):
        try:
            with open(filepath, mode='r', encoding=def_encoding) as f:
                n = 0
                for line in f:
                    n += 1
                    log_content.append(['['+ str(n) +'] ', line])
            # 数据格式为 {'section_id':section_id, 'type':'other', 'filepath':filepath, 'log_content':log_content_copy}
            section_id += 1
            log_content_copy = copy.deepcopy(log_content)
            Queue_Input.put({'section_id':section_id, 'type':'other', 'filepath':filepath, 'log_content':log_content_copy})
            log_content.clear()

            # 显示提示信息
            msg.input_info(section_id)

        except:
            try:
                # log_content.clear(): 如果上面的数据中途出错，则将之前的数据全部清除掉，然后重新开始录入，防止数据出现重复的情况
                log_content.clear()
                encoding = Check.get_encoding(filepath)
                with open(filepath, mode='r', encoding=encoding, errors='replace') as f:
                    n = 0
                    for line in f:
                        n += 1
                        log_content.append(['[' + str(n) + '] ', line])
                section_id += 1
                log_content_copy = copy.deepcopy(log_content)
                Queue_Input.put({'section_id': section_id, 'type': 'other', 'filepath': filepath, 'log_content': log_content_copy})
                log_content.clear()
                msg.input_info(section_id)

            except:
                msg.input_warn(encoding +' '+ filepath)

    # logs 类型的日志内容可能有进一步过滤的需求
    for filepath in file_abspath_dict.get('logs'):
        try:
            with open(filepath, mode='r', encoding=def_encoding) as f:
                tag_start = False
                for line in f:
                    # 记录该文件已经读取的行数
                    src_log_line += 1
                    # 额外的匹配条件
                    if input_argv.get('-ge') == input_argv.get('-le') == None:
                        tag_start = True
                    elif input_argv.get('-ge') != None and tag_start == False:
                        tag_start = Match.match_time_ge(input_argv.get('-ge'), line)
                    if input_argv.get('-le') != None and tag_start ==True:
                        tag_start = Match.match_time_le(input_argv.get('-le'), line)

                    if tag_start == True:
                        section_line += 1
                        log_content.append(['[' + str(src_log_line) + '] ', line])

                        if section_line >= Check.get_segment_number() and Check.check_input_rule(match_start=InputRule.get('match_start'), match_end=InputRule.get('match_end'), match_any=InputRule.get('match_any'), line=line):
                            section_id += 1
                            log_content_copy = copy.deepcopy(log_content)
                            Queue_Input.put({'section_id': section_id, 'type': 'logs', 'filepath': filepath, 'log_content': log_content_copy})
                            log_content.clear()
                            section_line = 0
                            msg.input_info(section_id)

            # 将最后一部分日记数据放入到队列中
            section_id += 1
            log_content_copy = copy.deepcopy(log_content)
            Queue_Input.put({'section_id': section_id, 'type': 'logs', 'filepath': filepath, 'log_content': log_content_copy})
            log_content.clear()
            src_log_line = 0
            msg.input_info(section_id)

        except:
            try:
                # log_content.clear(): 如果上面的数据中途出错，则将之前的数据全部清除掉，然后重新开始录入，防止数据出现重复的情况
                log_content.clear()
                encoding = Check.get_encoding(filepath)
                with open(filepath, mode='r', encoding=encoding, errors='replace') as f:
                    tag_start = False
                    for line in f:
                        # 记录该文件已经读取的行数
                        src_log_line += 1
                        # 额外的匹配条件
                        if input_argv.get('-ge') == input_argv.get('-le') == None:
                            tag_start = True
                        elif input_argv.get('-ge') != None and tag_start == False:
                            tag_start = Match.match_time_ge(input_argv.get('-ge'), line)
                        if input_argv.get('-le') != None and tag_start ==True:
                            tag_start = Match.match_time_le(input_argv.get('-le'), line)

                        if tag_start == True:
                            section_line += 1
                            log_content.append(['[' + str(src_log_line) + '] ', line])

                            if section_line >= Check.get_segment_number() and Check.check_input_rule(match_start=InputRule.get('match_start'), match_end=InputRule.get('match_end'), match_any=InputRule.get('match_any'), line=line):
                                section_id += 1
                                log_content_copy = copy.deepcopy(log_content)
                                Queue_Input.put({'section_id': section_id, 'type': 'logs', 'filepath': filepath, 'log_content': log_content_copy})
                                log_content.clear()
                                section_line = 0
                                msg.input_info(section_id)

                # 将最后一部分日记数据放入到队列中
                section_id += 1
                log_content_copy = copy.deepcopy(log_content)
                Queue_Input.put({'section_id': section_id, 'type': 'logs', 'filepath': filepath, 'log_content': log_content_copy})
                log_content.clear()
                src_log_line = 0
                msg.input_info(section_id)

            except:
                msg.input_warn(encoding +' '+ filepath)

    # 放入 False, 作为进程终止的判断条件
    for i in range(Check.get_multiprocess_counts() - 1):
        Queue_Input.put(False)