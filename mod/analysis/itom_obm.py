# -*- coding:utf-8 -*-

import re, os
from datetime import datetime
from mod.tools.match import Match

# test mode
from mod.tools.io_tools import delete_directory

def analysis_to_mongodb(Queue_Input, Queue_Output, black_list, dir_path):
    # 初始化参数
    n = True
    IsMuline = False
    tmp_list = []
    fin_list = []
    fin_data = []

    # 初始化数据变量
    file_type = None

    # 从 Queue 中获取数据
    while n:
        queue_data = Queue_Input.get()
        if queue_data == False:
            n = False
        else:
            # 如果获取的数据类型是 logs, 则进行进一步的处理
            # queue_data: {'section_id': id, 'type': 'log', 'filepath': filepath, 'log_content': [行数, 日志内容]}
            if queue_data.get('type') == 'logs':
                file_type = os.path.basename(queue_data.get('filepath')).split('.')[0]
                file_path = queue_data.get('filepath')

                # 对日志的事件进行整合和预处理, 生成预处理数据
                for line, log_content in queue_data.get('log_content'):
                    black_rule = True

                    # 黑名单规则
                    for blk_rule in black_list:
                        if Match.match_any(blk_rule, log_content):
                            black_rule = False

                    if black_rule == True and file_type not in ['UserActions',
                                                                'OvSvcDiscServer',
                                                                'opr-backend_boot',
                                                                'opr-backend_shutdown',
                                                                'login',
                                                                'opr-event-ws',
                                                                'opr-ws-response',
                                                                'kes',
                                                                'opr-ue',
                                                                'odb_boot',
                                                                'license',]:
                        # 先将每行数据放入临时列表中
                        tmp_list.append({'log_line': line, 'log_content': log_content.strip()})
                        # 判断本行是否是事件的开头, 如果是, 则将本行内容从临时列表中弹出, 并放入到最终的列表中, 否则开启多行匹配
                        if re.findall('INF:|INFO|WRN:|WARN|ERR|DEBUG| - ', log_content):
                            fin_list.append(tmp_list.pop())
                            # 如果本行已经是事件的开始, 那么意味着上一个事件已经结束, 需要将数据进行合并
                            while IsMuline:
                                if len(tmp_list) > 0:
                                    try:
                                        dict = {'log_line': '', 'log_content': ''}
                                        for tmp_dict in tmp_list:
                                            dict['log_line'] = dict.get('log_line') + tmp_dict.get('log_line')
                                            dict['log_content'] = dict.get('log_content') + '\n' + tmp_dict.get('log_content')
                                        fin_list[-2]['log_line'] = fin_list[-2].get('log_line') + dict.get('log_line')
                                        fin_list[-2]['log_content'] = fin_list[-2].get('log_content') + dict.get('log_content')
                                        tmp_list.clear()
                                    except:
                                        IsMuline = False
                                else:
                                    IsMuline = False
                        else:
                            IsMuline = True

                # 对每行数据进行进一步的处理：fin_list, 并且生成最终数据
                for dict in fin_list:
                    log_line = dict.get('log_line')
                    log_content = dict.get('log_content')
                    log_time = Match.match_log_time(log_content)

                    # 事件等级
                    if Match.match_any('INF:|INFO', log_content):
                        log_level = 'INFO'
                    elif Match.match_any('WRN:|WARN', log_content):
                        log_level = 'WARN'
                    elif Match.match_any('ERR', log_content):
                        log_level = 'ERR'
                    elif Match.match_any('DEBUG', log_content):
                        log_level = 'DEBUG'
                    else:
                        log_level = None

                    # 事件组件
                    # OBM 中的 OA 组件
                    if file_type in ['System','system']:
                        try:
                            log_component = re.findall(': [o|c]\w+', log_content)[0][2:]
                            log_component = 'OA' + '.' + log_component
                        except:
                            print(file_type)
                            print(log_content)

                    elif file_type in ['root']:
                        try:
                            log_component_1 = re.findall('\[.*?\]', log_content)[0][1:-1]
                            log_component_2 = re.findall(' :.*?->|G:.*?->', log_content)[0][2:-2]
                            log_component = file_type + '.' + log_component_1 + '.' + log_component_2
                            print(log_component)
                        except:
                            print(file_type)
                            print(log_content)

                    # 针对其余部分
                    elif file_type in ['opr-heartbeat',
                                       'opr-gateway',
                                       'opr-backend',
                                       'opr-ciresolver',
                                       'opr-webapp',
                                       'opr-configserver',
                                       'opr-svcdiscserver',
                                       'content-manager',
                                       'setting',]:
                        try:
                            log_component_1 = re.findall('\[.*?\]', log_content)[0][1:-1]
                            if Match.match_any('  .*?-',log_content):
                                log_component_2 = re.findall('  .*?-', log_content)[0][2:-2]
                            elif Match.match_any('\].*?-',log_content):
                                log_component_2 = re.findall('\].*?-', log_content)[0].split(' ')[2]
                            log_component = file_type + '.' + log_component_1 + '.' + log_component_2
                            print(log_component)
                        except:
                            print(file_type)
                            print(log_content)

                    # 针对 downtime.log 的处理
                    elif file_type in ['downtime',]:
                        try:
                            # 针对 log_componet_1 的处理
                            if Match.match_any('MSC service thread', log_content):
                                log_component_1 = 'MSC service thread'
                            elif Match.match_any('ServerService Thread Pool', log_content):
                                log_component_1 = 'ServerService Thread Pool'
                            else:
                                log_component_1 = re.findall('\[.*?\]', log_content)[0][1:-1]
                            # 针对 log_component_2 的处理
                            if Match.match_any('\(.*?\.',log_content):
                                log_component_2 = re.findall('\(.*?\.', log_content)[0][1:-2]
                            else:
                                log_component_2 = 'Unknow'
                            # 整合 log_component
                            log_component = file_type + '.' + log_component_1 + '.' + log_component_2
                            print(log_component)
                        except:
                            print(file_type)
                            print(log_content)

                    # 针对 opr-scripting-host.log 的处理
                    elif file_type in ['opr-scripting-host', ]:
                        try:
                            # 针对 log_component_1 的处理
                            if Match.match_any('ActiveMQ.*client.*global.*threads', log_content):
                                log_component_1 = 'ActiveMQ-client-global-threads'
                            else:
                                log_component_1 = re.findall('\[.*?\]', log_content)[0][1:-1]
                            # 针对 log_component_2 的处理
                            if Match.match_any('lambda.*logStatus',log_content):
                                log_component_2 = 'lambda:logStatus'
                            else:
                                log_component_2 = re.findall('  .*?\(', log_content)[0][1:-2].strip()
                            log_component = file_type + '.' + log_component_1 + '.' + log_component_2
                            print(log_component)
                        except:
                            print(file_type)
                            print(log_content)

                    # 针对 bsm_sdk_ucmdb_service.log 的处理
                    elif file_type in ['bsm_sdk_ucmdb_service',]:
                        try:
                            # 针对 log_component_1 的处理
                            if Match.match_any('CiResolverIndexManager', log_content):
                                log_component_1 = 'CiResolverIndexManager'
                            elif Match.match_any('RMI TCP Connection', log_content):
                                log_component_1 = 'RMI TCP Connection'
                            else:
                                log_component_1 = re.findall('\[.*?\]', log_content)[0][1:-1]
                            # 针对 log_component_2 的处理
                            if Match.match_any('\(.*?\)', log_content):
                                log_component_2 = re.findall('\(.*?\)', log_content)[0][2:-4]
                                if len(log_component_2) == 0:
                                    log_component_2 = re.findall('\(.*?\)', log_content)[-1][2:-4]
                            else:
                                log_component_2 = re.findall('\].*?-', log_content)[0].split(' ')[2]
                            log_component = file_type + '.' + log_component_1 + '.' + log_component_2
                            print(log_component)
                        except:
                            print(file_type)
                            print(log_content)

                    elif file_type in ['scripts',]:
                        try:
                            log_component_1 = re.findall('\[.*?\]', log_content)[0][1:-1]
                            log_component_2 = re.findall('ERROR.*?-|WARN.*?-|INFO.*?-', log_content)[0][4:-2]
                            log_component = file_type + '.' + log_component_1 + '.' + log_component_2
                            print(log_component)
                        except:
                            print(file_type)
                            print(log_content)

                    elif file_type in ['jboss7_boot','opr-clis','upgrade']:
                        # 暂时还没想好要怎么处理
                        pass

                # 注意, 在完成处理的操作后需要将清空 fin_list
                fin_list.clear()

    # test mode
    delete_directory(dir_path)