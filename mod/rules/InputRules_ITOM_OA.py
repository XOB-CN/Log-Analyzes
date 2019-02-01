# -*- coding:utf-8 -*-

"""
如果匹配到下列列表中的规则，则本行不能被分段
match_start: 从行首开始匹配
match_end: 从行尾开始匹配
match_any: 利用正则表达式，全行任意位置匹配
"""
match_start=[]
match_end=[]
match_any=[]

# 需要分析的文件列表
Zip_File_list = [
    # 搜集信息
    'agent\.log',

    # OA 的所有动作描述，包含错误信息
    'System\.txt',
]

# 如果匹配到，直接跳过后续匹配内容
black_rule_list = [
]