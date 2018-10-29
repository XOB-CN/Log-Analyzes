# -*- coding:utf-8 -*-
import re

# ConnectedBackup 日记的处理模块
def CBK_ZipAgent_Summary(queue1, queue2):
    # 初始化
    Agent_type = ''
    Agent_version =''
    Is_read_ver = False
    Agent_account =''
    Is_read_acc = False
    Agent_events ={}
    index_id = 0

    # 从 queue1 中获取日记
    n = True
    while n:
        line = queue1.get()

        # 判断 Agent_type 是 Mac 还是 PC
        if Is_read_ver != True:
            try:
                if line.index('® Backup for Mac Agent Version'):
                    Agent_type = 'Mac'
                    Agent_version = line[line.index('Version') + 9:-1]
                    Is_read_ver = True
                    print('Agent Version:{}'.format(Agent_version))
                    print('Agent Type:{}'.format(Agent_type))
            except:
                pass

            try:
                if line.index('Backup/PC Agent Version'):
                    Agent_type = 'PC'
                    Agent_version = line[line.index('Version') + 9:line.index('(')]
                    Is_read_ver = True
                    print('Agent Version:{}'.format(Agent_version))
                    print('Agent Type:{}'.format(Agent_type))
            except:
                pass

        # 进入日记分析流程
        if Agent_type == 'Mac' and Is_read_ver:
            if line[0:len('Account Number:')] == 'Account Number:':
                Agent_account = line[16:-1]
                Agent_events[index_id] = {'Agent_version':Agent_version, 'Agent_Type':Agent_type, 'Agent_account':Agent_account}
            pass
        elif Agent_type == 'PC' and Is_read_ver:
            print('input PC Log Rule')
            print(Agent_version)
            pass
        else:
            print('指定的日记类型错误，请重新检查您指定的文件')
            exit()
