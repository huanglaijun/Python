from base64 import encode
from cgi import print_form
from datetime import date, datetime
import re
from sqlite3 import converters
from elasticsearch import Elasticsearch
import pandas as pd
from flask import Flask, render_template, request, redirect

# 此程序功能：读取ES制定索引，并将索引数据保存至本地Excel文件

# 依赖关系
# Installing collected packages: urllib3, certifi, elastic-transport, elasticsearch
# Successfully installed certifi-2022.9.24 elastic-transport-8.4.0 elasticsearch-8.4.3 urllib3-1.26.12
# ES版本"number": "7.6.2"

# 读取ES数据
es = Elasticsearch(["http://10.8.1.30:9200/"])
body = {
    "query": {
        "match_all": {}
    }
}
# 设置读取的索引
value = es.search(index="ausdata_iso_eventdata_202210", body=body)
# 处理取回来的数据,只要['hits']['hits']['_source']中的数据
all_data = []
for hits in value['hits']['hits']:
    respose = hits['_source']
    all_data.append(respose)

# ES取回的数据all_data为列表，每个元素为一个字典，print(type(all_data[0])) <class 'dict'>
#
# 打印[]中每一个dict
# for i in range(0, len(all_data)-1):
#     print(all_data[i])
#
# 打印dict键值对
# for key, value in all_data[0].items():
#     print(key, value)

# 打印all_data每一条数据的key和value
# for i in range(0, len(all_data)-1):
#     for key, value in all_data[i].items():
#         print(key, value)


# # 将数据读取为DataFrame保存至本地Excel中
data = pd.DataFrame(all_data)
print(data)
data.to_csv("C:/Users/1/Desktop/归档事件.csv", encoding='gbk')




#
def test():
    es = Elasticsearch(["http://10.8.1.30:9200/"])

    body = {
        "query": {
            "match_all": {}
        }
    }
    # 设置读取的索引
    value = es.search(index="ausdata_iso_eventdata_202210", body=body)
    # 处理取回来的数据,只要['hits']['hits']['_source']中的数据
    all_data = []
    for hits in value['hits']['hits']:
        respose = hits['_source']
        all_data.append(respose)

    # md
    # ((a,a,a),(c,c,c))
    # es
    # ({'a':'1','a':'2'},{'c':'1','c':'2'})
    # all_data格式
    # [{'a':'1','a':'2'},{'c':'1','c':'2'}]


# <class 'tuple'>
data = test()
print(data)
