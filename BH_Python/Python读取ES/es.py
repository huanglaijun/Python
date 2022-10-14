from base64 import encode
from datetime import date, datetime
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
# print(all_data)

# 将数据读取为DataFrame保存至本地Excel中
data = pd.DataFrame(all_data)
print(data)
data.to_csv("C:/Users/1/Desktop/归档事件.csv", encoding='gbk')
