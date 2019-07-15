# -*- coding:utf-8 -*-

import os, sys
import re, time
import zipfile, tarfile, chardet

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..\..','config.cfg')), encoding='utf-8')

from mod.tools.match import Match
from mod.tools.debug import Debug

class Check(object):
    """检查类，主要判断各个参数是否正确以及获取各种配置参数"""
    @staticmethod
    def get_input_args():
        """
        获取并判断输入的参数是否正确，并给出相应的返回值;
        如果参数输入正确，则返回 参数列表;
        如果参数输入错误，则返回 False;
        :return: list or False
        """
        input_argv = sys.argv
        input_dict = {}
        check_list = ['-f', '-out', '-detail', '-t', '-le', '-ge', '-db_name', '-col_name', '-freq']
        to_summary = False

        # 实例化 message 类
        from mod.tools.message import Message
        msg = Message()

        # 没有输入参数的情况
        if len(input_argv) == 1:
            msg.general_help()
        # 检查输入的参数是否是 -h 或 -help
        elif '-h' in input_argv or '-help' in input_argv:
            return 'cmd_help'
        # 输入的参数是奇数的情况，不包含1
        elif len(input_argv) %2 == 0 and len(input_argv) > 2:
            msg.general_input_error()

        # 生成参数字典
        for i in check_list:
            if i in input_argv:
                idx = input_argv.index(i)
                input_dict[i] = input_argv[idx+1]

        # 处理 '-le' 和 '-ge' 参数的问题
        time_format_list = ['%Y-%m-%d %H:%M:%S','%Y-%m-%d %H:%M','%Y-%m-%d %H','%Y-%m-%d','%Y-%m','%Y']

        if input_dict.get('-ge') != None:
            if input_dict.get('-out') not in ['summary_by_time','summary_by_date','summary_by_count']:
                for time_format in time_format_list:
                    try:
                        input_time = time.strptime(input_dict.get('-ge'), time_format)
                        input_time = time.mktime(input_time)
                        input_dict['-ge'] = input_time
                    except:
                        pass

        if input_dict.get('-le') != None:
            if input_dict.get('-out') not in ['summary_by_time','summary_by_date','summary_by_count']:
                for time_format in time_format_list:
                    try:
                        input_time = time.strptime(input_dict.get('-le'), time_format)
                        input_time = time.mktime(input_time)
                        input_dict['-le'] = input_time
                    except:
                        pass

        try:
            have_f = '-f' in sys.argv
            have_f_data = sys.argv[sys.argv.index('-f') + 1]
            have_out = '-out' in sys.argv
            have_out_data = sys.argv[sys.argv.index('-out') + 1]
        except:
            if input_dict.get('-out') in ['summary_by_time','summary_by_date','summary_by_count']:
                to_summary = True
            else:
                msg.general_input_error()

        if to_summary:
            return input_dict
        elif have_f and have_f_data and have_out and have_out_data:
            return input_dict
        else:
            msg.general_input_error()

    @staticmethod
    def get_display_language():
        return cfg.get('display','display_language')

    @staticmethod
    def get_temp_path():
        return cfg.get('system','temp_path')

    @staticmethod
    def get_debug_level():
        return cfg.get('system','debug_level')

    @staticmethod
    def get_encoding(filename):
        """获取文件编码"""
        if cfg.getboolean('input','auto_detect_encoding'):
            _varchar = b''
            with open(filename, 'rb') as f:
                for i in range(cfg.getint('input','detect_encoding_line')):
                    _varchar = _varchar + f.readline()
            return chardet.detect(_varchar)['encoding']
        else:
            return 'utf-8'

    @staticmethod
    def get_def_encoding():
        return cfg.get('input', 'default_encoding')

    @staticmethod
    def get_segment_number():
        return cfg.getint('input','segment_number')

    @staticmethod
    def check_input_rule(match_start, match_end, match_any, line):
        """
        分段检查规则，必须返回为 Ture 时才能进行分段，如果匹配到这些规则，则会直接返回 False
        :param match_start: 匹配开头的列表
        :param match_end: 匹配结尾的列表
        :param match_any: 匹配任意的列表
        :param line: 待匹配的日记内容
        :return: 布尔值
        """
        for rule in match_start:
            if Match.match_start(rule, line):
                return False
        for rule in match_end:
            if Match.match_end(rule, line.strip(), isInclsEnter=False):
                return False
        for rule in match_any:
            if Match.match_any(rule, line):
                return False
        return True

    @staticmethod
    def get_multiprocess_counts():
        """获取可以同时进行的进程数"""
        if cfg.get('system', 'multiprocess_counts') in ['Auto', 'auto']:
            # 获取 Windows 的 CPU 核数
            try:
                return int(os.environ['NUMBER_OF_PROCESSORS'])
            except:
                return 4
        else:
            return cfg.getint('system', 'multiprocess_counts')

    @staticmethod
    def get_display_segments():
        return cfg.getint('display', 'display_segments')

    @staticmethod
    def check_files(filepath, InputRules_NeedFiles, basepath):
        '''
        如果是压缩包，则检查压缩包中是否包含需要分析的文件
        如果是单文件，则直接返回该文件的绝对路径(仅支持 .log / .txt 文件)
        :param filepath: 待分析的原始文件路径
        :param InputRules: Input 规则列表
        :param basepath: os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..'))
        :return:list:[file_abspath_dict, unarchive_path]
        '''
        if Match.match_any('\.log', filepath) or Match.match_any('\.txt', filepath):
            if Match.match_end('.zip', filepath, isInclsEnter=False) or Match.match_end('tar.gz', filepath, isInclsEnter=False):
                # 针对压缩包进行处理，与最下方的 else 处理方式一致
                file_path_dict = ArchiveCheck.check_archive(filepath, InputRules_NeedFiles)
                unarchive_path = ArchiveCheck.unarchive(filepath, basepath)
                file_abspath_dict = ArchiveCheck.get_abspath_dict(unarchive_path, file_path_dict)
                return [file_abspath_dict, unarchive_path]

            else:
                # 针对单文件进行处理
                file_abspath_dict = {'logs':[filepath,], 'other':''}
                unarchive_path = filepath
                return [file_abspath_dict, unarchive_path]

        else:
            # 过滤压缩包中的内容
            file_path_dict = ArchiveCheck.check_archive(filepath, InputRules_NeedFiles)
            # 解压压缩包，获取解压路径
            unarchive_path = ArchiveCheck.unarchive(filepath, basepath)
            # 获取需要分析文件列表的绝对路径
            file_abspath_dict = ArchiveCheck.get_abspath_dict(unarchive_path, file_path_dict)

            return [file_abspath_dict, unarchive_path]

    @staticmethod
    def get_mongodb_connect_url():
        return cfg.get('MongoDB', 'mongodb_connect_url')

class ArchiveCheck(Check):
    """检查类，主要针对的是压缩包文件（多文件）"""
    @staticmethod
    @Debug.get_time_cost('[debug] 主进程 - 检查压缩包：')
    def check_archive(archive_filename, rules_dict):
        """
        检查压缩包中是否包含需要分析的日志文件
        :param archive_filename: 压缩包文件名
        :param rule_list: 需要匹配的规则
        :return: dict{logs:list, other:list} 或 输出提示信息，并直接退出
        """
        from mod.tools.message import Message
        msg = Message()

        # 初始化参数
        archive_type = None
        logs = []
        other = []

        # 判断压缩包的类型
        if zipfile.is_zipfile(archive_filename):
            zip_file = zipfile.ZipFile(archive_filename)
            archive_type = 'zip'
        elif tarfile.is_tarfile(archive_filename):
            tar_file = tarfile.open(archive_filename, "r:gz")
            archive_type = 'tar'
        else:
            msg.archive_type_error()

        if archive_type == 'zip':
            for file in zip_file.filelist:
                # 判断文件大小
                if file.file_size != 0:
                    # 将对应的日记文件加入到列表中
                    for rule in list(set(rules_dict.get('other'))):
                        if Match.match_any(rule, file.filename):
                            other.append(file.filename)
                    for rule in list(set(rules_dict.get('logs'))):
                        if Match.match_any(rule, file.filename):
                            logs.append(file.filename)
        else:
            for file in tar_file.getnames():
                # 将对应的日记文件加入到列表中
                for rule in list(set(rules_dict.get('other'))):
                    if Match.match_any(rule, file):
                        other.append(file)
                for rule in list(set(rules_dict.get('logs'))):
                    if Match.match_any(rule, file):
                        logs.append(file)
            tar_file.close()

        file_path_list = {'logs':logs, 'other':other}
        if file_path_list == {'logs': [], 'other': []}:
            msg.general_no_need_file()
        else:
            return file_path_list

    @staticmethod
    @Debug.get_time_cost('[debug] 主进程 - 解压缩：')
    def unarchive(filepath, basepath):
        """
        解压压缩包，并返回压缩包的路径
        :param filepath: 待解压的压缩包所在路径
        :param basepath: 待解压的基础路径
        :return: string:解压后的路径
        """
        archive_type = None
        from mod.tools.message import Message
        msg = Message()

        # 如果是压缩包是 zip
        if zipfile.is_zipfile(filepath):
            zip_file = zipfile.ZipFile(filepath)
            archive_type = 'zip'
        # 如果是压缩包是 tar.gz
        elif tarfile.is_tarfile(filepath):
            tar_file = tarfile.open(filepath, "r:gz")
            archive_type = 'tar'

        msg.archive_decompressing_info()
        # 解压压缩包, 并返回解压后文件所在的路径
        if archive_type == 'zip':
            zip_file = zipfile.ZipFile(filepath)
            unarchive_path = os.path.join(basepath, Check.get_temp_path())
            zip_file.extractall(os.path.join(basepath, Check.get_temp_path()))

        else:
            tar_file = tarfile.open(filepath, "r:gz")
            unarchive_path = os.path.join(basepath, Check.get_temp_path())
            try:
                tar_file.extractall(os.path.join(basepath, Check.get_temp_path()))
            except PermissionError as e:
                if Check.get_debug_level() in ['warn','debug']:
                    msg.archive_decompressing_error(e)
            tar_file.close()

        msg.archive_decompression_finish_info()
        return unarchive_path

    @staticmethod
    @Debug.get_time_cost('[debug] 主进程 - 获取解压后的绝对路径：')
    def get_abspath_dict(unzip_path, file_path_dict):
        """
        获取文件列表的绝对路径
        :param unzip_path: 解压文件夹的路径
        :param file_path_dict: {logs:list, other:list}
        :return: 包含待分析的文件列表路径
        """
        abspath_logs = []
        abspath_other = []

        for path in file_path_dict.get('logs'):
            abspath_logs.append(os.path.join(unzip_path, path))

        for path in file_path_dict.get('other'):
            abspath_other.append(os.path.join(unzip_path, path))

        # list(set(数组)) 为了去重，防止后续会出现重复的结果
        return {'logs':list(set(abspath_logs)), 'other':abspath_other}