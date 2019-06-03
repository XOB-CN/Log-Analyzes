# -*- coding:utf-8 -*-

general_help = '''\
请输入 -h 或 -help 来查看该命令的使用方法'''

general_help_command = '''\
-f      必须，指定需要分析的文件名
-out    必须，指定需要输出结果的形式，值可以是 report / csv / mysql
-detail 可选，是否生成详细信息，值为 on 时开启，默认不开启
-ge     可选，只有当日志中的时间大于指定值时才会开启分析功能
-le     可选，只有当日志中的时间小于指定值时才会开启分析功能，注意，需要同时指定 -ge 参数'''

general_input_error = '''\
输入的参数不正确，请检查后重新输入'''

general_file_error ='''\
不存在指定的文件，请检查后重新输入'''

general_output_error ='''\
该命令暂时还没有这个输出方法'''

general_no_need_file ='''\
没有需要分析的文件'''

archive_type_error ='''\
不支持此格式，仅支持'.zip'和'.tar.gz'格式的压缩包, 或者'.txt'和'.log'单文件'''

archive_decompressing_info = '''\
[info] 主进程：正在解压压缩包'''

archive_decompressing_error = '''\
[error] 主进程：无法处理该文件：'''

archive_decompression_finish_info = '''\
[info] 主进程：解压完成'''

input_info = '''\
[info] 输入端：已读取第 {num} 段'''

input_warn = '''\
[warn] 输入端：无法处理该文件 '''

analysis_info = '''\
[info] 分析端：已分析第 {num} 段'''

analysis_content_warn = '''\
[warn] 分析端：无法根据指定的规则来处理数据，请检查您指定的规则，错误信息：'''

output_get_finish_info = '''\
[info] 输出端：以获取所有数据'''

output_integrate_info = '''\
[info] 输出端：正在整理已分析的数据'''

output_integrate_finish_info = '''\
[info] 输出端：数据整理完成！'''

output_write_html_info = '''\
[info] 输出端：正在生成结果文件, 请稍后...'''

output_write_html_finish_info = '''\
[info] 输出端：结果文件已经生成'''

output_delete_info = '''\
[info] 输出端：正在删除临时目录'''

output_delete_finish_info = '''\
[info] 输出端：临时目录已经删除，分析完成'''

output_delete_warn = '''\
[warn] 输出端：无法删除临时文件，请手动删除'''