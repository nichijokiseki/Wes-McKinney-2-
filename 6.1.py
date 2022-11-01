import pandas as pd
import numpy as np
# 简单地读取一个以逗号分隔的csv文件
print(pd.read_csv('examples:ex1.csv'))
# 如果希望将message列做成DataFrame的索引，可以通过index_col参数指定'message'
names = ['a', 'b', 'c', 'd', 'message']
print(pd.read_csv('examples:ex2.csv', names=names, index_col='message'))
# 如果希望将多个列做成一个层次化索引，可以传入由列编号或列名组成的列表
print(pd.read_csv('examples:csv_mindex.csv', index_col=['key1', 'key2']))
# 某些情况下，有些表格可能不是用固定的分隔符去分隔字段的（比如空白符或其他形式）
# 这种情况可以传递一个正则表达式作为read_table的分隔符
print(pd.read_table('examples:ex3.txt', sep='\s+'))
# 缺失值处理是文件解析任务的一个重要组成部分，缺失数据有两种情况（没有或用某个标记值表示）
# 默认情况下，pandas会使用一组经常出现的标记值进行识别（比如NA及NULL）
print(pd.read_csv('examples:ex4.csv'))
print(pd.isnull(pd.read_csv('examples:ex4.csv')))
# na_values可以通过一个列表或集合的字符串表示缺失值
# 字典的各列可以使用不同的NA标记值
print(pd.read_csv('examples:ex4.csv', na_values=['NULL']))
sentinels = {'message': ['foo', 'NA'], 'something': ['two']}
print(pd.read_csv('examples:ex4.csv', na_values=sentinels))

# 在处理很大的文件时，或找出大文件中的参数集以便于后续处理，可能只想要读取文件的一小部分或逐块对文件进行迭代
# 如果只想读取几行（避免读取整个文件），可以指定参数nrows
print(pd.read_csv('examples:ex5.csv', nrows=10))

import sys
# 数据也可以被输出为分隔符格式的文本
# 利用DataFrame的to_csv方法，可以将数据写到一个文件中（默认以逗号分隔）
data = pd.read_csv('examples:ex4.csv')
data.to_csv('examples:out.csv')
# 也可以使用其他分隔符，只需要指定参数sep的值
print(data.to_csv(sys.stdout, sep='|'))
# 缺失值在输出结果中会被表示为空字符串，也可以将其表示为别的标记值
print(data.to_csv(sys.stdout, na_rep='NULL'))
# 如果不设置其他选项，那么就会写出行和列的标签，它们都可以被禁用
print(data.to_csv(sys.stdout, index=False, header=False))
# 可以只写出一部分，并按照指定的顺序排列
print(data.to_csv(sys.stdout, index=False, columns=['a', 'c', 'd']))
# Series也有其to_csv方法
dates = pd.date_range('1/1/1999', periods=7)
ts = pd.Series(np.arange(7), index=dates)
ts.to_csv('examples:tseries.csv', header=False)
print(pd.read_csv('examples:tseries.csv'))

# 大部分表格型数据都能用pandas.read_table来进行加载
# 但是由于接收到含有畸形行的文件而使得read_table出毛病的情况并不少见
print(pd.read_csv('examples:ex6.csv'))
# 对于任何的单字符分隔符文件，可以使用csv模块，将任意打开的文件传给csv.reader
import csv
f = open('examples:ex6.csv', encoding='UTF-8-sig')
reader = csv.reader(f)
# 对这个reader进行迭代会为每行产生一个元组（并且移除所有的引号）
for line in reader:
    print(line)
# 现在为了让数据合乎要求，需要对其进行一些整理工作
# 首先读取文件到一个多行的列表中
with open('examples:ex6.csv', encoding='UTF-8-sig') as f:
    lines = list(csv.reader(f))
# 然后将这些行分为标题行和数据行
header, values = lines[0], lines[1:]
# 使用字典构造式
data_dict = {h: v for h, v in zip(header, zip(*values))}
print(data_dict)
# csv文件的形式有很多，只需要定义csv.Dialect的一个子类就能够定义出一个新格式（比如特定的分隔符、引用约定、行结束符等）
f = open('examples:ex6.csv', encoding='UTF-8-sig')
class my_dilect(csv.Dialect):
    lineterminator = '\n'
    delimiter = ';'
    quotechar = '"'
    quoting = csv.QUOTE_MINIMAL
reader_1 = csv.reader(f, dialect=my_dilect)
# 各个CSV语支的参数也可以使用关键字的形式提供给csv.reader，而无需定义子类
reader_2 = csv.reader(f, delimiter='|')

# JSON（JavaScript Object Notation）已成为通过HTTP请求在Web浏览器和其他应用程序之间发送数据的标准格式之一
# 一个JSON的例子
obj = """
{"name": "Wes", 
 "places_lived": ["United States", "Spain", "Germany"], 
 "pet": null, 
 "siblings": [{"name": "Scott", "age": 30, "pets": ["Zeus", "Zuko"]},
              {"name": "Katie", "age": 38, "pets": ["Sixes", "Stache", "Cisco"]}]
}
"""
# JSON非常接近于有效的Python代码，基本类型有对象（字典）、数组（列表）、字符串、数值、布尔值以及null
# 通过json.loads可以将JSON字符串转换成Python形式
# 通过json.dumps可以将Python对象转换成JSON形式
import json
result = json.loads(obj)
print(result)
# 将（一个或一组）JSON对象转换为便于分析的数据结构
# 一个简单的做法：向DataFrame构造器传入一个字典的列表，并选取数据字段的子集
siblings = pd.DataFrame(result["siblings"], columns=["name", "age"])
print(siblings)
# pandas.read_json可以自动将特别格式的JSON数据集转换为Series或DataFrame
# pandas.read_json的默认选项假设JSON数组中的每个对象是表格中的一行
# 如果需要将数据从pandas输出到JSON，可以使用方法to_json
data = pd.read_json("example.json")
print(data)

# Python有许多可以读写常见HTML和XML格式数据的库，包括lxml、Beautiful Soup、html5lib等
# lxml的速度比较快，但其他的库处理有误的HTML或XML文件更好
# 打开一个记录了银行倒闭情况的HTML文件
# 默认条件下，pd.read_html会搜索、尝试解析标签内的表格数据，结果是一个列表的DataFrame对象
tables = pd.read_html("examples:fdic_failed_bank_list.html")
failures = tables[0]
pd.set_option("display.max_columns", None)
print(failures.head())
# 这里可以进行一些数据的处理
# 比如按照年份计算倒闭的银行数量
close_timestamps = pd.to_datetime(failures["Closing Date"])
print(close_timestamps.dt.year.value_counts())

# XML是另一种常见的支持分层、嵌套数据以及元数据的结构化数据格式
# XML和HTML的结构很相似，但XML更为通用
