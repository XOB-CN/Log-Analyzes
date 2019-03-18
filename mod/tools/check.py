# -*- coding:utf-8 -*-

import os, sys
import zipfile, tarfile

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read(os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..\..','config.cfg')), encoding='utf-8')

from mod.tools.match import Match

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
        check_list = ['-f', '-out', '-detail', '-t', '-filter']

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

        try:
            have_f = '-f' in sys.argv
            have_f_data = sys.argv[sys.argv.index('-f') + 1]
            have_out = '-out' in sys.argv
            have_out_data = sys.argv[sys.argv.index('-out') + 1]
        except:
            msg.general_input_error()

        if have_f and have_f_data and have_out and have_out_data:
            return input_dict
        else:
            msg.general_input_error()

    @staticmethod
    def get_display_language():
        return cfg.get('system','display_language')

    @staticmethod
    def get_temp_path():
        return cfg.get('system','temp_path')

    @staticmethod
    def get_debug_level():
        return cfg.get('system','debug_level')

    @staticmethod
    def get_encoding(filename):
        import chardet
        """获取文件编码"""
        if cfg.getboolean('system','auto_detect_encoding'):
            _varchar = b''
            with open(filename, 'rb') as f:
                for i in range(cfg.getint('system','detect_encoding_line')):
                    _varchar = _varchar + f.readline()
            return chardet.detect(_varchar)['encoding']
        else:
            return 'utf-8'

    @staticmethod
    def get_def_encoding():
        cfg.read('base', 'default_encoding')

class ArchiveCheck(Check):
    """检查类，主要针对的是压缩包文件（多文件）"""
    @staticmethod
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
                    for rule in rules_dict.get('other'):
                        if Match.match_any(rule, file.filename):
                            other.append(file.filename)
                    for rule in rules_dict.get('logs'):
                        if Match.match_any(rule, file.filename):
                            logs.append(file.filename)
        else:
            for file in tar_file.getnames():
                # 将对应的日记文件加入到列表中
                for rule in rules_dict.get('other'):
                    if Match.match_any(rule, file):
                        other.append(file)
                for rule in rules_dict.get('logs'):
                    if Match.match_any(rule, file):
                        logs.append(file)
            tar_file.close()

        file_path_list = {'logs':logs, 'other':other}
        if file_path_list == {'logs': [], 'other': []}:
            msg.general_no_need_file()
        else:
            return file_path_list

    @staticmethod
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

        return {'logs':abspath_logs, 'other':abspath_other}