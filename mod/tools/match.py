# -*- coding:utf-8 -*-
import re, time
from datetime import datetime

class Match(object):
    """内容匹配类"""
    @staticmethod
    def match_any(rule, logline):
        """利用正则表达式来进行全局匹配，如果符合则返回 True, 其中 re.I 代表大小写不敏感"""
        if rule == None:
            return False
        else:
            return re.findall(rule, logline, re.I) != []

    @staticmethod
    def match_start(rule, logline):
        """从日记开头开始匹配，如果符合则返回 True"""
        if rule == None:
            return False
        else:
            return logline[0:len(rule)] == rule

    @staticmethod
    def match_end(rule, logline, isInclsEnter=True):
        """从日记结尾开始匹配，如果符合则返回 True，默认匹配带换行符的"""
        if rule == None:
            return False

        elif isInclsEnter:
            #print(logline[-len(rule) - 1:-1])
            return logline[-len(rule) - 1:-1] == rule
        else:
            #print(logline[-len(rule):])
            return logline[-len(rule):] == rule

    @staticmethod
    def match_log_time(logline):
        """
        获取日志中的时间，并返回时间戳
        :param logline: 待匹配的日志
        :return: 时间戳 / False
        """
        time_format = {
            "[a-z|A-Z]{3} [a-z|A-Z]{3} \s*\d{1,2} \d{2}:\d{2}:\d{2} \d{4}": "%a %b %d %H:%M:%S %Y",
            "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}": "%Y-%m-%d %H:%M:%S",
            "\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}": "%Y/%m/%d %H:%M:%S",
            "\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}": "%y/%m/%d %H:%M:%S",
            "\d{4} [a-z|A-Z]{3} \d{2} \d{2}:\d{2}:\d{2}": "%Y %b %d %H:%M:%S",
            "\d{2}-[a-z|A-Z]{3}-\d{4} \d{2}:\d{2}:\d{2}": "%d-%b-%Y %H:%M:%S",
        }
        for re_rule, time_rule in time_format.items():
            try:
                log_time = re.findall(re_rule, logline)[0]
                log_time = time.strptime(log_time, time_rule)
                log_time = time.mktime(log_time)
                return log_time
            except:
                pass
        return False

    @staticmethod
    def match_time_ge(input_time, logline):
        """
        比较日志中的时间与指定时间，如果日志中的时间大于等于指定的时间，则返回 True
        :param input_time: 指定时间的时间戳
        :param logline: 待分析的日志内容
        :return:
        """
        try:
            log_time = Match.match_log_time(logline)
            return log_time >= input_time
        except:
            return False

    @staticmethod
    def match_time_le(input_time, logline):
        """
        比较日志中的时间与指定时间，如果日志中的时间小于等于指定的时间，则返回 True
        :param input_time: 指定时间的时间戳
        :param logline: 待分析的日志内容
        :return:
        """
        try:
            log_time = Match.match_log_time(logline)
            return log_time <= input_time
        except:
            return False

    @staticmethod
    def convert_time(log_time):
        """
        将字符串形式保存的时间转换成时间对象
        :param log_time: 字符串形式的时间
        :return: python 的 datetime 格式
        """
        time_format = [
            "%a %b %d %H:%M:%S %Y",
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%y/%m/%d %H:%M:%S",
            "%Y %b %d %H:%M:%S",
            "%d-%b-%Y %H:%M:%S",
        ]

        for time_fmt in time_format:
            try:
                log_date = datetime.strptime(log_time, time_fmt)
                return log_date
            except:
                pass
        return False
