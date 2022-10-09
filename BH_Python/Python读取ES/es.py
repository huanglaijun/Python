from base64 import encode
from datetime import date, datetime
from sqlite3 import converters
from elasticsearch import Elasticsearch
import pandas as pd


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
# print(data)
data.to_csv("C:/Users/1/Desktop/归档事件.csv", encoding='gbk')

# pandas读取ES数据
# Create a DataFrame object
# from pandasticsearch import DataFrame
# df = DataFrame.from_es(url='http://10.8.1.30:9200/',
#                        index='ausdata_iso_eventdata_202210')

# # Print the schema(mapping) of the index
# df.print_schema()
# company
# |-- employee
#   |-- name: {'index': 'not_analyzed', 'type': 'string'}
#   |-- age: {'type': 'integer'}
#   |-- gender: {'index': 'not_analyzed', 'type': 'string'}

# Inspect the columns
# df.columns
# #['name', 'age', 'gender']

# # Denote a column
# df.name
# # Column('name')
# df['age']
# # Column('age')

# # Projection
# df.filter(df.age < 25).select('name', 'age').collect()
# # [Row(age=12,name='Alice'), Row(age=11,name='Bob'), Row(age=13,name='Leo')]

# # Print the rows into console
# df.filter(df.age < 25).select('name').show(3)
# # +------+
# # | name |
# # +------+
# # | Alice|
# # | Bob  |
# # | Leo  |
# # +------+

# # Convert to Pandas object for subsequent analysis
# df[df.gender == 'male'].agg(df.age.avg).to_pandas()
# #    avg(age)
# # 0        12

# # Translate the DataFrame to an ES query (dictionary)
# df[df.gender == 'male'].agg(df.age.avg).to_dict()
# # {'query': {'filtered': {'filter': {'term': {'gender': 'male'}}}}, 'aggregations': {'avg(birthYear)':
# # {'avg': {'field': 'birthYear'}}}, 'size': 0}
