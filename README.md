# Log-Analyzes

## 功能描述
用来读取软件中的日记信息，用来整理和提取日记中的信息，并输出到指定位置，方便对日记进行分析

## 流程解释
进程1：输入端，用来读取日记<br>
进程2：处理端，用来解析日记<br>
进程3：输出端，输出到指定位置

## 使用方法
+ 将日记内容输出到 MySQL 数据库
    + IDOL-Query.py -f logfile -t tablename
    
+ 将日记内容输出到 csv 文件
    + CBK-Agent-Summary.py -f logfile -out csv

+ 如果不添加任何参数，则会列出所有的参数列表

## 支持情况

#### MicroFocus
+ ConnectedBackup
    + Agent 生成的汇总信息，文件格式：Agent_*****-*****_mm-dd-YYYY_HH-MM.txt

+ IDOL
    + query 类日记，例如 content/query.log, agentstore/query.log, qms/query.log 等