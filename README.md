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
2. 安装 第三方库 chardet
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
-f      必须，指定需要分析的文件名
-out    必须，指定需要输出结果的形式，值可以是 report / csv / mysql
-detail 可选，是否生成详细信息，值为 on 时开启，默认不开启
-ge     可选，只有当日志中的时间大于指定值时才会开启分析功能
-le     可选，只有当日志中的时间小于指定值时才会开启分析功能，注意，需要同时指定 -ge 参数
```

## 配置参数
请参考 config.cfg 文件, 每部分都有注释说明

## 支持情况
* Apache
    * Tomcat
        * 输出到 Report
        ```bash
        Apache-Tomcat.py -f archivefile -out report [-detail on] [-ge 日期 [-le 日期]]
        ```
* Microfocus
    * Connected Backup
        * 输出到 Report
        ```bash
        CBK-ZipAgent.py -f zipfile -out report [-detail on] [-ge 日期 [-le 日期]]
        ```
    * Fortify SSC/SCA/WI/WIE
        * 输出到 Report
        ```bash
        Fortify-[SSC|SCA|WI|WIE].py -f archivefile -out report [-detail on] [-ge 日期 [-le 日期]]
        ```
    * ITOM OA / OBM
        * 输出到 Report
        ```bash
        ITOM-OA.py -f archivefile -out report [-detail on] [-ge 日期 [-le 日期]]
        ```

## 授权模式
GNU General Public License v3.0