# -*- coding:utf-8 -*-

import re
import os, sys, time, zipfile
import chardet
import functools

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..','config.cfg')), encoding='utf-8')

base_path = os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..'))

class Check(object):
    """检查类，主要判断各个参数是否正确以及获取各种配置参数"""

    @staticmethod
    def get_input_args():
        """
        获取并判断输入的参数是否正确，并给出相应的返回值;
        如果参数输入正确，则返回 Ture 以及对应的参数;
        如果参数输入错误，则返回 False 以及错误的信息;
        """
        check_list = ['-f','-t','-out','-detail']
        argv_dict = {}

        if len(sys.argv) == 1:
            return [False, Message.help_info()]

        if len(sys.argv) %2 == 0:
            return [False, '参数个数不正确，请检查后重新输入']

        for i in check_list:
            if i in sys.argv:
                index = sys.argv.index(i)
                argv_dict[i] = sys.argv[index+1]

        try:
            have_f = '-f' in sys.argv
            have_f_data = sys.argv[sys.argv.index('-f') + 1]
            have_out = '-out' in sys.argv
            have_out_data = sys.argv[sys.argv.index('-out') + 1]
        except:
            return [False, '缺少必须参数，请检查后重新输入']

        if have_f and have_f_data and have_out and have_out_data:
            return [True, argv_dict]
        else:
            print('缺少必须参数，请检查后重新输入')
            return [False, '缺少必须参数，请检查后重新输入']

    @staticmethod
    def get_encoding(filename):
        """获取文件编码"""
        if cfg.getboolean('base','auto_detect_encoding'):
            _varchar = b''
            with open(filename, 'rb') as f:
                for i in range(cfg.getint('base','detect_encoding_line')):
                    _varchar = _varchar + f.readline()
            return chardet.detect(_varchar)['encoding']
        else:
            return 'utf-8'

    @staticmethod
    def get_multiprocess_counts():
        """获取可以同时进行的进程数"""
        return cfg.getint('base','multiprocess_counts')

    @staticmethod
    def get_temp_path():
        """获取临时路径"""
        return cfg.get('base','temp_path')

    @staticmethod
    def get_debug_level():
        """获取debug模式的值"""
        return cfg.get('base','debug_level')

    @staticmethod
    def check_input_rule(rule_start, rule_end, rule_any, line):
        """
        分段检查规则，必须返回为 Ture 时才能进行分段，如果匹配到这些规则，则会直接返回 False
        :param rule_start: 匹配开头的列表
        :param rule_end: 匹配结尾的列表
        :param rule_any: 匹配任意的列表
        :param line: 待匹配的日记内容
        :return: 布尔值
        """
        for rule in rule_start:
            if LogAnalze.match_start(rule, line):
                return False
        for rule in rule_end:
            if LogAnalze.match_end(rule, line.strip(), isInclsEnter=False):
                return False
        for rule in rule_any:
            if LogAnalze.match_any(rule, line):
                return False
        return True

class ZipCheck(Check):
    """检查类，主要针对的是压缩包文件（多文件）"""

    @staticmethod
    def get_abspath_list(unzip_path, file_path_list):
        """
        获取文件列表的绝对路径
        :param unzip_path: 解压文件夹的路径
        :param file_path_list: 压缩包内部的文件列表
        :return: 包含待分析的文件列表路径
        """
        abspath = []
        for path in file_path_list:
            abspath.append(os.path.join(unzip_path, path))

        return abspath

    @staticmethod
    def check_zipfile(zip_filename, rule_list):
        """
        检查压缩包中是否包含需要分析的日记信息
        :param zip_filename: 压缩包文件名
        :param rule_list: 需要匹配的规则
        :return: 数据类型为 list, 内容为需要分析的文件路径列表
        """
        if zipfile.is_zipfile(zip_filename):
            zip_file = zipfile.ZipFile(zip_filename)
        else:
            Message.error_message('指定的不是压缩文件，检查后重新输入')

        file_path = []
        for file in zip_file.filelist:
            # 判断文件大小
            if file.file_size != 0:
                # 将对应的日记文件加入到列表中
                for rule in rule_list:
                    if LogAnalze.match_any(rule, file.filename):
                        file_path.append(file.filename)

        return file_path

    @staticmethod
    def unzip(zip_filename):
        """
        解压压缩包，并且返回压缩包的路径
        :param zip_filename: 压缩包所在路径
        :return: 字符串：解压所在的路径
        """
        zip_file = zipfile.ZipFile(zip_filename)
        unzip_file_path = os.path.join(base_path, Check.get_temp_path())
        zip_file.extractall(os.path.join(base_path, Check.get_temp_path()))
        return unzip_file_path

class LogAnalze(object):
    """分析类，判断日记属于什么规则，结果返回布尔值，匹配则返回 True，不匹配则返回 False"""

    @staticmethod
    def match_any(rule, logline):
        """利用正则表达式来进行全局匹配，如果符合则返回 True, 其中 re.I 代表大小写不敏感"""
        return re.findall(rule, logline, re.I) != []

    @staticmethod
    def match_start(rule, logline):
        """从日记开头开始匹配，如果符合则返回 True"""
        return logline[0:len(rule)] == rule

    @staticmethod
    def match_end(rule, logline, isInclsEnter=True):
        """从日记结尾开始匹配，如果符合则返回 True，默认匹配带换行符的"""
        if isInclsEnter:
            print(logline[-len(rule) - 1:-1])
            return logline[-len(rule) - 1:-1] == rule
        else:
            print(logline[-len(rule):])
            return logline[-len(rule):] == rule

class Output(object):
    """输出类，将数据输出到指定位置"""

    @staticmethod
    def write_to_html(datas, input_args):
        """
        将分析后的数据写入到 html 文件中
        需要传入2个参数：一个是整理后的数据，另一个是输入的参数，用来判断是否生成详细信息
        """
        base_path = os.getcwd()
        file_path = os.path.join(base_path, (input_args['-f'] + '_report.html'))
        event_type = set()  # 记录目前录入的分类，初始状态是空

        # 生成日记分析的显示数据
        log_content=''
        for data in datas:
            # 如果改规则匹配到了数据，则生成显示数据
            if data.get('log_line') != None:
                # 生成分类
                if data.get('type') not in event_type:
                    event_type.add(data.get('type'))
                    log_content = log_content + Template_Report.html_h(data.get('type'), 2)

                # 特殊分类：Information 需要显示的内容
                if data.get('type') == 'Information':
                    log_content = log_content + '<br>' + Template_Report.html_h(data.get('name'), 3, 'title')
                    log_content = log_content + Template_Report.html_div(data.get('content'), 'log-line')
                    log_content = log_content + Template_Report.html_h('对应行数', 3)
                    log_content = log_content + Template_Report.html_div(data.get('log_line'), 'log-line')
                    if input_args.get('-detail') in ['True', 'ture', 'On', 'on']:
                        log_content = log_content + Template_Report.html_h('详细信息', 3)
                        log_content = log_content + Template_Report.html_div(data.get('detail'), 'log-line')

                # 特殊分类：Others 需要显示的内容
                elif data.get('type') == 'Others':
                    log_content = log_content + '<br>' + Template_Report.html_h(data.get('name'), 3, 'title')
                    log_content = log_content + Template_Report.html_h('对应行数', 3)
                    log_content = log_content + Template_Report.html_div(data.get('log_line'), 'log-line')
                    if input_args.get('-detail') in ['True', 'ture', 'On', 'on']:
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
                    log_content = log_content + Template_Report.html_h('对应行数', 3)
                    log_content = log_content + Template_Report.html_div(data.get('log_line'), 'log-line')
                    if input_args.get('-detail') in ['True', 'ture', 'On', 'on']:
                        log_content = log_content + Template_Report.html_h('详细信息', 3)
                        log_content = log_content + Template_Report.html_div(data.get('detail'), 'log-line')

        # 完整的 html 内容
        html_result = Template_Report.html_template('分析结果', log_content)

        # 将 html 内容写入到文件中
        Message.info_message('[Info] 输出端：正在将结果写入到文件中，请稍后')
        with open(file_path, mode='w', encoding='utf8', newline='') as f:
            f.write(html_result)

class Template_Report(Output):
    """Report输出模板"""

    @staticmethod
    def html_template(title, content):
        """str.format()的转义字符是两个大括号：{{}}"""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                h2{{font-weight:bold; text-align:center;}}
                h3{{font-size:18px; font-weight:bold;}}
                .title{{color:blue;}}
                .log-line{{font-size:12px;}}
                .keyword{{font-size:12px; color:red;}}
                .detail{{font-size:12px;}}
            </style>
        </head>
        <body>
        {content}
        </body>
        </html>"""
        return html_content.format(title=title, content=content)

    @staticmethod
    def html_h(content, number, html_class='noting'):
        """html 的 h 标签"""
        return "<h"+str(number) +' class='+ html_class + ">" + content + "</h"+str(number)+">" + "\n"

    @staticmethod
    def html_div(content, html_class):
        """html 的 div 标签"""
        return "<div class=" + html_class + ">"+ content +"</div>" + "\n"

    @staticmethod
    def html_font(content, color='red'):
        """html 的 font 标签"""
        return '<font color="{color}">{content}</font>'.format(content=content, color=color)

class Message(object):
    """信息类，显示各种提示信息"""

    @staticmethod
    def info_message(message):
        print(message)

    @staticmethod
    def warn_message(message):
        print(message)

    @staticmethod
    def error_message(message):
        print(message)
        exit()

    @staticmethod
    def help_info():
        print("\n"
              "To MySQL:\n"
              "-f       必须：指定要读取的文件名\n"
              "-t       必须：指定要保存的数据表的名字\n"
              "-d       可选：需要创建的数据库名，默认为当前时间\n"
              "-out     必须：指定要输出的类型，此处应该设置为 mysql \n\n"
              "To CSV:\n"
              "-f       必须：指定要读取的文件名\n"
              "-out     必须：指定要输出的类型，此处应该设置为 csv\n\n"
              "To Report:\n"
              "-f       必须：指定要读取的文件名\n"
              "-out     必须：指定要输出的类型，此处应该设置为 report\n"
              "-detail  可选：可以输出更详细的内容，默认不启用，当该值为 on、On、True 时生效\n")
        exit()

class Debug(object):
    """调试类，显示调试信息"""

    @staticmethod
    def get_time_cost(func_name):
        """
        装饰器，如果debug模式开启，则显示函数运行的时间
        :param func_name: 函数名，仅仅作为显示，类行为字符串
        """
        def decorator(func):
            @functools.wraps(func)  # 处理原始函数__name__等属性
            def wrapper(*args, **kwargs):
                if Check.get_debug_level() == 'debug':
                    start_time = time.time()
                    func(*args, **kwargs)
                    end_time = time.time()
                    cost_time = end_time - start_time
                    print('{func_name}耗时 {cost_time} ms'.format(func_name=func_name, cost_time=cost_time))
                else:
                    return func(*args, **kwargs)
            return wrapper
        return decorator