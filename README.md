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
    + To MySQL:<br>
      -f   必须：指定要读取的文件名<br>
      -t   必须：指定要保存的数据表的名字<br>
      -u   可选：连接数据库的用户名<br>
      -h   可选：连接数据库的主机<br>
      -d   可选：需要创建的数据库名，默认为当前时间<br>
      -p   可选：连接数据库的密码<br>
      -P   可选：连接数据库的端口，默认为 3306<br>
      -out 可选：指定要输出的地点，默认为 mysql<br>

    + To CSV:<br>
      -f   必须：指定要读取的文件名<br>
      -out 必须：指定要输出的地点，默认为 mysql，此处应该设定为 csv

## 支持情况

#### MicroFocus
+ ConnectedBackup
    + Agent客户端生成的汇总信息，文件格式：Agent_*****-*****_mm-dd-YYYY_HH-MM.txt（仅支持英文）

+ IDOL
    + query类型的日记，例如 content/query.log, agentstore/query.log, qms/query.log 等