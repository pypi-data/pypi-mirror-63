# xtalpi-pandas v0.0.6#

xtalpi-pandas是对pandas进行封装的命令行工具，用于处理csv

## 安装 ##
安装前建议升级pip，并将pip更换为国内源（清华）
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
通过pip进行安装
```
pip install xtalpi-pandas
```

## 更新 ##
通过pip进行更新
```
pip install xtalpi-pandas -U
```

## 使用方式 ##
打开终端，输入
```
xpandas xxx.csv
```
其中xxx.csv为待处理的csv路径。之后按照程序提示选择功能，执行操作。

## 功能列表  ##
|command|description|
|-----|-----|
|c|将csv均分为N个csv|
|s|每N行切分为一个csv|
|t|按csv中某列的值Top N行|

