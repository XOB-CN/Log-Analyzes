# -*- coding:utf-8 -*-

general_help = '''\
Please input '-h' or '-help' to see how to use this command.'''

general_help_command = '''\
Report / MongoDB mode:
-f          must, Specify the filename.
-out        must, Specify the form in which you want to output the result. The value can be 'report' or 'csv' or 'mysql'.
-detail     optional, Generates details when the value is on, default it's disable.
-ge         optional, The analysis function is enabled only when the time in the log is greater than the specified value.
-le         optional, The analysis function is enabled only when the time in the log is less than the specified value. you need to specify the '-ge' parameter at the same time.

Summary_by_*** mode:
-out        must, Specify the out mode, now can use "summary_by_date" or "summary_by_count"
-db_name    must, Specify the MongoDB Database name.
-col_name   optional, Specify the MongoDB Collection name，default name it's "default"
-ge         optional, Count only data greater than or equal to the specified date
-le         optional, Count only data less than or equal to the specified date
-freq       optional, only use by "summary_by_date" mode，set pandas Resampling frequency，default it's H，representing hourly
            for example: T - per minute, H - hourly, D - every day, M - per month

summary_by_count_lv** mode
-out        must, Specify the out mode，now can use "summary_by_count_lv1 / lv2 / lv3"
-db_name    must, Specify the MongoDB Database name.
-col_name   optional, Specify the MongoDB Collection name，default name it's "default"
-ge         optional, Count only data greater than or equal to the specified date
-le         optional, Count only data less than or equal to the specified date
-top        optional, show top rows of data，default it's lv1 - 5; lv2 - 10; lv3 - 15
-gui        optional, display a histogram, when the value is on will enable (not recommended)'''

general_input_error = '''\
Input parameters are incorrect, Please check and re-enter.'''

general_file_error ='''\
The specified file does not exist, Please check and re-enter.'''

general_output_error ='''\
This command does not have this output method yet.'''

general_no_need_file ='''\
No files found to be analyzed.'''

archive_type_error ='''\
Archive format is not supported, only '.zip' or '.tar.gz' or '.txt' or '.log' formats are supported.'''

archive_decompressing_info = '''\
[info] Main: Decompressing...'''

archive_decompressing_error = '''\
[error] Main: Can't process this file: '''

archive_decompression_finish_info = '''\
[info] Main: Decompression completed.'''

input_info = '''\
[info] Input: Has been read {num} segments. '''

input_warn = '''\
[warn] Input: Can't process this file: '''

analysis_info = '''\
[info] Analysis: Has been process {num} segments.'''

analysis_content_warn = '''\
[warn] Analysis: Can't process this line, please check your rule. Exception info: '''

output_get_finish_info = '''\
[info] Output: Has been getting all data.'''

output_integrate_info = '''\
[info] Output: Now is integrating data'''

output_integrate_finish_info = '''\
[info] Output: Integration finish!'''

output_write_html_info = '''\
[info] Output: Generating result file, please wait...'''

output_write_html_finish_info = '''\
[info] Output: Result file has been generated.'''

output_delete_info = '''\
[info] Output: Deleting temp directory.'''

output_delete_finish_info = '''\
[info] Output: Temp directory has been deleted, analysis it's completed.'''

output_delete_warn = '''\
[warn] Output: Can't delete temp directory, please delete by manually.'''

output_mongo_insert_info = '''\
[info] Output：Has been insert {num} segments.'''

output_graph_dbname_error = '''\
[error] Output: No input -db_name, please check it again.'''