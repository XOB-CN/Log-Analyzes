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
2. 安装 第三方库 chardet, pymongo, pandas, matplotlib
```
    pip install chardet pymongo pandas matplotlib
```
3. 如果想要在任意目录下执行该脚本，请将 bin 目录添加到系统的环境变量中
```
Windows
   变量：Path   值：bin 目录的绝对路径
   例如：C:\Log-Analyzes\bin
```

## 使用方法
* 分析日记内容并生成分析结果
```bash
LogAnalyzes.py -f logfile -out report [-detail on] [-ge 日期 [-le 日期]]   # 日期格式:年-月-日, 例如 2019-10-10
```
* 如果添加 -h 或 -help 参数，则会显示提示信息
```
Report 模式 / MongoDB 模式
-f          必须，指定需要分析的文件名
-out        必须，指定需要输出结果的形式，值可以是 report / mongodb
-detail     可选，是否生成详细信息，值为 on 时开启，默认不开启
-ge         可选，只有当日志中的时间大于指定值时才会开启分析功能
-le         可选，只有当日志中的时间小于指定值时才会开启分析功能，注意，需要同时指定 -ge 参数

Summary_by_*** 模式
-out        必须，指定需要输出结果的形式，目前值可以是 summary_by_date / summary_by_count
-db_name    必须，指定 MongoDB 的数据库名字
-col_name   可选，指定 MongoDB 的集合的名字，默认值是 default
-ge         可选，只统计大于等于指定日期的数据
-le         可选，只统计小于等于指定日期的数据
-freq       可选，仅用于 summary_by_date 模式，设定 pandas 重采样的频率，默认为H，代表每小时

Summary_by_count_lv** 模式
-out        必须，指定需要输出结果的形式，目前值可以是 summary_by_count_lv1 / lv2 / lv3
-db_name    必须，指定 MongoDB 的数据库名字
-col_name   可选，指定 MongoDB 的集合的名字，默认值是 default
-ge         可选，只统计大于等于指定日期的数据
-le         可选，止痛剂小于等于指定日期的数据
-top        可选，显示数据的前多少行，默认值：lv1 - 5; lv2 - 10; lv3 - 15
-gui        可选，是否显示柱状图，当值为 on, enable 时显示柱状图（不推荐）
```

## 配置参数
请参考 config.cfg 文件, 每部分都有注释说明

## 支持情况
* Apache
    * Tomcat
        * 输出到 Report
        ```bash
        Apache-Tomcat.py -f logfile -out report [-detail on] [-ge 日期 [-le 日期]]
        ```
* Microfocus
    * Connected Backup
        * 输出到 Report
        ```bash
        CBK-ZipAgent.py -f logfile -out report [-detail on] [-ge 日期 [-le 日期]]
        ```
    * Fortify SSC/SCA/WI/WIE
        * 输出到 Report
        ```bash
        Fortify-[SSC|SCA|WI|WIE].py -f logfile -out report [-detail on] [-ge 日期 [-le 日期]]
        ```
    * ITOM OA / OBM
        * 输出到 Report
        ```bash
        ITOM-OA.py -f logfile -out report [-detail on] [-ge 日期 [-le 日期]]
        ```
        * 输出到 MongoDB
        ```bash
        ITOM-OA.py -f logfile -out mongodb [-db_name DBname] [-col_name ColName]
        ```
        * 显示统计信息
        ```bash
        ITOM-OA.py -out summary_by_date|summary_by_count -db_name DBName [-col_name ColName] [-ge 日期] [-le 日期] [-freq 频率单位,默认为1H]
        # -freq：是 pandas 的 resample 方法的频率单位，常见的有：T - 每分钟, H - 每小时, D - 每一天, M - 每个月    
        ```

## 授权模式
GNU General Public License v3.0