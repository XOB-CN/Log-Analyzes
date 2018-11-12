# -*- coding:utf-8 -*-

# 设置系统环境变量
def set_path():
    import os, sys
    base_path = os.path.abspath('..')
    sys.path.append(base_path)
    sys.path.append(os.path.split(os.path.realpath(__file__))[0][:-3])


def main():
    # 主程序逻辑
    Q1 = Queue()
    Q2 = Queue()

    # 获取输入的信息,用来决定后续的处理流程
    arg_dict = input.read_args()

    p1 = Process(target=input.log_send, args=(arg_dict['filename'], Q1))
    p2 = Process(target=ConnectedBackup.CBK_ZipAgent_Summary, args=(Q1, Q2))

    # 此处用来决定输出端具体的位置
    if arg_dict['output'] == 'csv':
        p3 = Process(target=output.to_csv, args=(arg_dict,Q2, tools.TemplateCSV.cbk_summary()))
    else:
        p3 = Process(target=output.to_mysql, args=(arg_dict,Q2, tools.TemplateMySQL.cbk_summary))

    p1.start()
    p2.start()
    p3.start()

if __name__ == "__main__":
    # 将当前路径添加到系统环境变量中
    set_path()

    # 加载所需的模块
    from mod import input, output, tools
    from mod.analysis import ConnectedBackup
    from multiprocessing import Process,Queue

    # 主程序逻辑
    main()