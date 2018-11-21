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

    # 获取输入的信息
    arg_dict = input.read_args()

    p1 = Process(target=input.log_send, args=(arg_dict['filename'], Q1))
    p2 = Process(target=IDOL.IDOL_Query, args=(Q1, Q2))

    # 此处用来决定输出端具体的位置
    if arg_dict['output'] == 'csv':
        # 这里有括号的原因是因为 tools.TemplateCSV.idol_query() 有返回值，类型是列表，如果没有括号后续无法处理
        p3 = Process(target=output.to_csv, args=(arg_dict,Q2, tools.TemplateCSV.idol_query()))
    elif arg_dict['output'] == 'report':
        tools.Messages.pop_error('没有这个输出方法！')
    else:
        p3 = Process(target=output.to_mysql, args=(arg_dict,Q2, tools.TemplateMySQL.idol_query))

    p1.start()
    p2.start()
    p3.start()


if __name__ == "__main__":
    # 将当前路径添加到系统环境变量中
    set_path()

    # 加载所需的模块
    from mod import input, output, tools
    from mod.analysis import IDOL
    from multiprocessing import Process,Queue

    # 主程序逻辑
    main()