# -*- coding:utf-8 -*-
import re, time

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
            print(logline[-len(rule) - 1:-1])
            return logline[-len(rule) - 1:-1] == rule
        else:
            print(logline[-len(rule):])
            return logline[-len(rule):] == rule

    @staticmethod
    def match_time_ge(rule, logline):
        """
        比较日志中的时间与指定时间，如果日志中的时间大于等于指定的时间，则返回 True
        :param rule: 数据格式：[rule_time:指定时间的时间戳, re_format:抓取时间字符串的正则表达式, time_format:需要进行时间转换的字符串格式]
        :param logline: 待分析的日志内容
        :return:
        """
        try:
            try:
                log_time = re.findall("[a-z|A-Z]{3} [a-z|A-Z]{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4}", logline)[0]
                log_time = time.strptime(log_time, '%a %b %d %H:%M:%S %Y')
                log_time = time.mktime(log_time)
                return log_time >= rule[0]
            except:
                log_time = re.findall(rule[1], logline)[0]
                try:
                    print(log_time, rule[1], rule[2][0], rule[2][1])
                    log_time = time.strptime(log_time, rule[2][0])
                except:
                    log_time = time.strptime(log_time, rule[2][1])
                log_time = time.mktime(log_time)
                return log_time >= rule[0]
        except:
            return False

    @staticmethod
    def match_time_le(rule, logline):
        """
        比较日志中的时间与指定时间，如果日志中的时间小于等于指定的时间，则返回 True
        :param rule: 数据格式：[rule_time:指定时间的时间戳, re_format:抓取时间字符串的正则表达式, time_format:需要进行时间转换的字符串格式]
        :param logline: 待分析的日志内容
        :return:
        """
        try:
            try:
                log_time = re.findall("[a-z|A-Z]{3} [a-z|A-Z]{3} \d{1,2} \d{2}:\d{2}:\d{2} \d{4}", logline)[0]
                log_time = time.strptime(log_time, '%a %b %d %H:%M:%S %Y')
                log_time = time.mktime(log_time)
                return log_time <= rule[0]
            except:
                log_time = re.findall(rule[1], logline)[0]
                try:
                    log_time = time.strptime(log_time, rule[2][0])
                except:
                    log_time = time.strptime(log_time, rule[2][1])
                log_time = time.mktime(log_time)
                return log_time <= rule[0]
        except:
            return False