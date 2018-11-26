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
    Error_Q = Queue()

    # 获取输入的信息,用来决定后续的处理流程
    arg_dict = input.read_args()

    p1 = Process(target=input.log_send, args=(arg_dict['filename'], Q1, Error_Q))

    # 此处用来决定输出端具体的位置
    if arg_dict['output'] == 'report':
        p2 = Process(target=General.General_Report_LogAnalyze, args=(Q1, Q2, Rules_Fortify_SSC.RulesList))
        p3 = Process(target=output.to_report, args=(arg_dict, Q2))
    else:
        tools.Messages.pop_error('没有这个输出方法！')

    p1.start()
    if Error_Q.get() == False:
        exit(1)
    p2.start()
    p3.start()

if __name__ == "__main__":
    # 将当前路径添加到系统环境变量中
    set_path()

    # 加载所需的模块
    from mod import input, output, tools
    from mod.analysis import General
    from mod.rules import Rules_Fortify_SSC
    from multiprocessing import Process,Queue

    # 主程序逻辑
    main()