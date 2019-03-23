# -*- coding:utf-8 -*-

import os, shutil
from mod.tools.template import Template_Report
from mod.tools.debug import Debug
from mod.tools.message import Message
msg = Message()

@Debug.get_time_cost('[debug] 输出端 - 生成结果文件：')
def write_to_html(datas, input_argv):
    """
    将分析后的数据写入到 html 文件中
    需要传入2个参数：一个是整理后的数据，另一个是输入的参数，用来判断是否生成详细信息
    """
    msg.output_write_html_info()
    base_path = os.getcwd()
    file_path = os.path.join(base_path, (input_argv['-f'] + '_report.html'))
    event_type = set()  # 记录目前录入的分类，初始状态是空

    # 生成日记分析的显示数据
    log_content=''
    for data in datas:
        # 如果改规则匹配到了数据，则生成显示数据
        if data.get('detail') != None:
            # 生成分类
            if data.get('type') not in event_type:
                event_type.add(data.get('type'))
                log_content = log_content + Template_Report.html_h(data.get('type'), 2)

            # 特殊分类：Information 需要显示的内容
            if data.get('type') == 'Information':
                log_content = log_content + '<br>' + Template_Report.html_h(data.get('name'), 3, 'title')
                log_content = log_content + Template_Report.html_div(data.get('content'), 'log-line')
                log_content = log_content + Template_Report.html_h('所在位置', 3)
                log_content = log_content + Template_Report.html_div(data.get('log_line'), 'log-line')
                if input_argv.get('-detail') in ['True', 'ture', 'On', 'on']:
                    log_content = log_content + Template_Report.html_h('详细信息', 3)
                    log_content = log_content + Template_Report.html_div(data.get('detail'), 'log-line')

            # 特殊分类：Others 需要显示的内容
            elif data.get('type') == 'Others':
                log_content = log_content + '<br>' + Template_Report.html_h(data.get('name'), 3, 'title')
                log_content = log_content + Template_Report.html_h('所在位置', 3)
                log_content = log_content + Template_Report.html_div(data.get('log_line'), 'log-line')
                if input_argv.get('-detail') in ['True', 'ture', 'On', 'on']:
                    log_content = log_content + Template_Report.html_h('详细信息', 3)
                    log_content = log_content + Template_Report.html_div(data.get('detail'), 'log-line')

            # 常规分类需要显示的内容
            else:
                log_content = log_content + '<br>' + Template_Report.html_h('问题原因', 3, 'title')
                log_content = log_content + Template_Report.html_div(data.get('name'), 'log-line')
                log_content = log_content + Template_Report.html_h('匹配规则', 3)
                log_content = log_content + Template_Report.html_div(data.get('match'), 'keyword')
                log_content = log_content + Template_Report.html_h('解决思路', 3)
                log_content = log_content + Template_Report.html_div(data.get('solution'), 'log-line')
                log_content = log_content + Template_Report.html_h('所在位置', 3)
                log_content = log_content + Template_Report.html_div(data.get('log_line'), 'log-line')
                if input_argv.get('-detail') in ['True', 'ture', 'On', 'on']:
                    log_content = log_content + Template_Report.html_h('详细信息', 3)
                    log_content = log_content + Template_Report.html_div(data.get('detail'), 'log-line')

    # 完整的 html 内容
    html_result = Template_Report.html_template('分析结果', log_content)

    # 将 html 内容写入到文件中
    with open(file_path, mode='w', encoding='utf8', newline='') as f:
        f.write(html_result)

    msg.output_write_html_finish_info()

@Debug.get_time_cost('[debug] 输出端 - 删除临时目录：')
def delete_directory(unarchive_path):
    msg.output_delete_info()
    if unarchive_path != None:
        try:
            shutil.rmtree(unarchive_path)
            msg.output_delete_finish_info()
        except PermissionError as e:
            if os.name == 'nt':
                # rd/s/q 是 windows 平台强制删除命令
                cmd = 'rd/s/q ' + unarchive_path
                os.system(cmd)
                msg.output_delete_finish_info()
            else:
                msg.output_delete_warn(str(e))