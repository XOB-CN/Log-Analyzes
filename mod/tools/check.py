# -*- coding:utf-8 -*-

import os, sys

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
        # 输入的参数是奇数的情况，不包括一个，因为还要判断是否是 -h / -help
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

class ArchiveCheck(Check):
    """检查类，主要针对的是压缩包文件（多文件）"""

    @staticmethod
    def check_archive(archive_filename, rules_dict):
        """
        检查压缩包中是否包含需要分析的日志文件
        :param archive_filename: 压缩包文件名
        :param rule_list: 需要匹配的规则
        :return: dict{logs:list, other:list}
        """
        import zipfile, tarfile
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

        return {'logs':logs, 'other':other}