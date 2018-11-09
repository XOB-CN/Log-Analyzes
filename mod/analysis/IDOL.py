# -*- coding:utf-8 -*-
import re
from mod.tools import LogAnalyze

# IDOL Query 日记的处理模块
def IDOL_Query(queue1, queue2):

    n = True
    Is_Start = False
    index_id = 1
    event_dict = {} # key:index_id / value:日记的具体内容
    index_dict = {} # 维护目前正在处理的事件 key:thr_id / value:index_id
    src_log_line = 0  # 源文件日记的行数
    no_deal_with = [] # 未处理的日记内容

    while n:
        line = queue1.get()

        if line == False:
            n = False

        else:
            # 准备好需记录的日记分段
            src_log_line += 1
            log_time_tmp = line.split(' ', 4)[0]
            MM,DD,YY = log_time_tmp.split('/')
            log_time = YY+'/'+ MM + '/' + DD + ' ' + line.split(' ', 4)[1]
            log_thid = line.split(' ', 4)[2]
            log_level = line.split(' ', 4)[3][3:-1]
            log_content = line.split(' ', 4)[-1]

            ################-开头结束-###################################################################################

            # 事件的开头：Request from 开头
            if LogAnalyze('Request from', log_content).log_start():
                if Is_Start == False:
                    Is_Start = True

                # 将此行加入正在处理的事件中
                # index_dict key(log_thid) ---> value:index_id = event_dict key <--- event_dict value(log_content)
                index_dict[log_thid] = index_id
                event_dict[index_id] = {'log_line':src_log_line,'log_time':log_time,'log_thid':log_thid,'host':log_content[len('Request from'):-1],'status':'No Status Info'}
                index_id += 1

            # 事件的结束：Request completed 开头
            elif LogAnalyze('Request completed', log_content).log_start():
                if Is_Start == True:
                    tmp_index_id = index_dict[log_thid]
                    event_dict[tmp_index_id]['finsh_time'] = log_content[len("Request completed in "):-2]

                    # 将完成的数据放入到 Queue 中，由下一个进程来处理
                    log_data = event_dict.pop(tmp_index_id)
                    del index_dict[log_thid]
                    queue2.put(log_data)
                else:
                    no_deal_with.append(line)

            ################-Action/ActionID-###########################################################################

            elif LogAnalyze('action=', log_content).log_start() or LogAnalyze('ACTION=', log_content).log_start():
                if Is_Start == True:
                    # 查看当前线程属于那个事件(与 index_id 对应)，并将对应的数据写入到相应的事件中去
                    tmp_index_id = index_dict[log_thid]
                    event_dict[tmp_index_id]['action'] = log_content[:-1]

                    # 如果开头包含 actionid=.{40}，代表内容中有 ActionID 信息
                    if LogAnalyze('actionid=.{40}', log_content).log_regex():
                        tmp_index_id = index_dict[log_thid]
                        actionid = str(re.findall('actionid=.{40}', log_content))[len("['actionid="):-2]
                        event_dict[tmp_index_id]['action_id'] = actionid
                else:
                    # 如果 Is_Start 不是 True,代表此事件没有开头，事件不完整，所以不进行处理
                    no_deal_with.append(line)

            elif LogAnalyze('Generated ActionId', log_content).log_start():
                if Is_Start == True:
                    tmp_index_id = index_dict[log_thid]
                    event_dict[tmp_index_id]['action_id'] = log_content[len('Generated ActionId '):-1]
                else:
                    no_deal_with.append(line)

            ################-命令结束-###################################################################################

            # 如果日记以 complete 结尾，代表该命令结束
            elif LogAnalyze(' complete', log_content).log_end():
                if Is_Start == True:
                    tmp_index_id = index_dict[log_thid]
                    event_dict[tmp_index_id]['status'] = log_content[:-1]
                else:
                    no_deal_with.append(line)

    queue2.put(False)