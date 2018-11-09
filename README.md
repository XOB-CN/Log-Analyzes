# Log-Analyzes

## 功能描述
用来读取软件中的日记信息，用来整理和提取日记中的信息，并输出到指定位置，方便对日记进行分析

## 流程解释
* 该脚本启动时，会依次创建3个子进程来进行处理各自的任务
* 进程1：输入端，用来判断输入的参数是否正确以及读取日记内容
* 进程2：处理端，用来处理日记内容
* 进程3：输出端，将处理完成的内容输出到指定位置

## 使用方法
* 将日记内容输出到 MySQL 数据库
```
IDOL-Query.py -f logfile -t tablename [-d dbname | -P 3306 | …… ]
```  
* 将日记内容输出到 csv 文件
```
CBK-Agent-Summary.py -f logfile -out csv
```
* 如果不添加任何参数，则会列出所有的参数列表
```
To MySQL:
-f   必须：指定要读取的文件名
-t   必须：指定要保存的数据表的名字
-u   可选：连接数据库的用户名
-h   可选：连接数据库的主机
-d   可选：需要创建的数据库名，默认为当前时间
-p   可选：连接数据库的密码
-P   可选：连接数据库的端口，默认为 3306
-out 可选：指定要输出的地点，默认为 mysql

To CSV:
-f   必须：指定要读取的文件名
-out 必须：指定要输出的地点，默认为 mysql，此处应该设定为 csv
```
## 支持情况

#### MicroFocus
* ConnectedBackup
    * Agent客户端生成的汇总信息，文件格式：Agent_*****-*****_mm-dd-YYYY_HH-MM.txt（仅支持英文）

* IDOL
    * query类型的日记，例如 content/query.log, agentstore/query.log, qms/query.log 等