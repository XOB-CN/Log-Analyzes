# Log-Analyzes

## 功能描述
提取或整理日记中的信息，并输出到指定位置，方便对日记做进一步的分析或调查

## 流程解释
* 该脚本启动时，会创建三类进程来进行各自的处理：
    * 输入端：分割或重新排序日记内容
    * 分析端：接收输入端的日记内容，并进行分析处理
    * 输出端：合并分析端的数据，并将结果发送到指定位置

## 安装方法
1. 安装 Python 3
2. 安装 第三方库 chardet, pymysql, sqlalchemy, sqlalchemy-utils
3. 如果想要在任意目录下执行该脚本，请将 bin 目录添加到系统的环境变量中
```
Windows
   变量：Path   值：bin 目录的绝对路径
   例如：C:\Log-Analyzes\bin
```

## 使用方法
* 分析日记内容并生成分析结果
```bash
LogAnalyzes.py -f logfile -out report [-detail on]
```
* 如果不添加任何参数，则会列出所有的参数列表
```
To Report:
-f       必须：指定要读取的文件名
-out     必须：指定要输出的类型, 此处应该设置为 report
-detail  可选：可以输出更详细的内容, 默认不启用，当该值为 on、On、True 时生效

To CSV:
-f       必须：指定要读取的文件名
-out     必须：指定要输出的类型, 此处应该设置为 csv

To MySQL:
-f       必须：指定要读取的文件名
-out     必须：指定要输出的类型, 此处应该设置为 mysql
```

## 配置参数
请参考 config.cfg 文件, 每部分都有注释说明

## 支持情况
* Microsoft
    * Microsoft SQL Server
        * 输出到 Report
        ```bash
        MSSQL-Server.py -f logfile -out report [-detail on]
        ```
* Microfocus
    * Connected Backup
        * 输出到 Report
        ```bash
        CBK-ZipAgent.py -f zipfile -out report [-detail on]
        ```
        * 输出到 CSV
        ```bash
        CBK-ZipAgent.py -f zipfile -out csv
        ```
        * 输出到 MySQL
        ```bash
        CBK-ZipAgent.py -f zipfile -out mysql
        ```
    * Fortify SSC
        * 输出到 Report
        ```bash
        Fortify-SSC.py -f archivefile -out report [-detail on]
        ```
    * ITOM OA
        * 输出到 Report
        ```bash
        ITOM-OA.py -f archivefile -out report [-detail on]
        ```
    
* 通用模板
    * LogAnalyzes
        * 输出到 Report
        ```bash
        LogAnalyzes.py -f logfile -out report [-detail on]
        ```

## 授权模式
GNU General Public License v3.0