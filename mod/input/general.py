# -*- coding:utf-8 -*-

from mod.tools.check import Check
from mod.tools.message import Message
msg = Message()

def archive_general(file_abspath_dict, Queue_Input, match_rule=None):
    """
    通用的输入端读取日志，不需要处理日志的排序问题
    :param file_abspath_dict: 包含需要分析的文件列表，按照字典进行分类
    :param Queue_Input: 将预读取完成的数据放到 Queue_Input 中
    :param match_rule: 可选的过滤规则，可以进一步过滤 file_abspath_dict.get('logs') 中的内容，例如使用时间来过滤
    :return:
    """

    section_id = 0 # 记录分段的个数序号，用于记录顺序
    section_line = 0  # 记录每段内容的行数
    src_log_line = 0  # 记录原始日记的行数
    log_content = []  # 存放初步整理的数据

    def_encoding = Check.get_def_encoding()

    # 由于 other 类型的日志内容一般都是配置文件信息，所以将读取后的文件内容处理后发送到 Queue_Input 即可
    for filepath in file_abspath_dict.get('other'):
        try:
            with open(filepath, mode='r', encoding=def_encoding) as f:
                n = 0
                for line in f:
                    n += 1
                    log_content.append(['['+ str(n) +'] ', line])
            # 将数据放入 Queue_Input 中
            # 数据格式为 {'section_id':section_id, 'type':'other', 'filepath':filepath, 'log_content':log_content}
            section_id += 1
            Queue_Input.put({'section_id':section_id, 'type':'other', 'filepath':filepath, 'log_content':log_content})
        except:
            try:
                encoding = Check.get_encoding(filepath)
                with open(filepath, mode='r', encoding=encoding) as f:
                    n = 0
                    for line in f:
                        n += 1
                        log_content.append(['[' + str(n) + '] ', line])
                section_id += 1
                Queue_Input.put(
                    {'section_id': section_id, 'type': 'other', 'filepath': filepath, 'log_content': log_content})
            except:
                msg.input_warn(filepath)

    for filepath in file_abspath_dict.get('logs'):
        # try:
        #     with open(filepath, mode='r', encoding=def_encoding) as f:
        #         pass
        # except:
        #     try:
        #         encoding = Check.get_encoding(filepath)
        #         with open(filepath, mode='r', encoding=encoding) as f:
        #             pass
        #     except:
        #         pass
        try:
            with open(filepath, mode='r', encoding=def_encoding) as f:
                n = 0
                for line in f:
                    n += 1
                    log_content.append(['['+ str(n) +'] ', line])
            section_id += 1
            #Queue_Input.put({'section_id':section_id, 'type':'other', 'filepath':filepath, 'log_content':log_content})
        except:
            try:
                encoding = Check.get_encoding(filepath)
                print(encoding)
                with open(filepath, mode='r', encoding=encoding) as f:
                    n = 0
                    for line in f:
                        n += 1
                        log_content.append(['[' + str(n) + '] ', line])
                    section_id += 1
                    #Queue_Input.put({'section_id': section_id, 'type': 'other', 'filepath': filepath, 'log_content': log_content})
            except UnicodeDecodeError as e:
                msg.input_warn(filepath)