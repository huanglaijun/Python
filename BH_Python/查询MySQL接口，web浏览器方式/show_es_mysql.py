# -*- coding: utf-8 -*-
import pandas as pd
import pymysql
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request, redirect


# 引用flask框架
app = Flask(__name__)


def search_mysql(name, phone):
    # 定义查询mysql数据库方法
    # mysql连接参数
    dbconn = pymysql.connect(
        host='192.168.72.129',
        user='root',
        database='iso_db_core',
        password='1',
        port=3306
    )
    cur = dbconn.cursor()
    # sql语句查询1000条结果
    sql = "select * from t_evt_sent_sms WHERE NAME LIKE " + '"' +\
        name + '"' + " AND PHONE LIKE " + '"' + \
        phone+'"' + " order by LASTSENDTIME desc limit 1000;"
    print(sql)
    cur.execute(sql)
    md = cur.fetchall()
    dbconn.close()
    return md


def read_es(index):
    # 定义查询ES数据库方法
    # 读取ES数据
    es = Elasticsearch(["http://10.8.1.30:9200/"])
    body = {
        "query": {
            "match_all": {}
        }
    }
    # 设置读取的索引
    value = es.search(index=index, body=body)
    # 处理取回来的数据,只要['hits']['hits']['_source']中的数据
    all_data = []
    for hits in value['hits']['hits']:
        respose = hits['_source']
        all_data.append(respose)

    # all_data为[{第一条记录},{第二条记录}...]的列表，每条记录为一个dict字典
    # 每条记录key值相同，只将value值取出来
    # 需将[{'a':'1','b':'2'},{'c':'3','d':'4'}]转化为
    # (('1', '2'), ('3', '4'))

    # 定义一个列表，列表内容为[(),(),()]每个元素为一个元组，每个元组是all_data其中一个字典的value值
    # value_list预期格式为[('1', '2'), ('3', '4')]
    value_list = []
    for i in range(0, len(all_data)):
        # 每个tmp_list只存放all_data中一个字典的值
        # tmp_list预期格式为['1', '2'],['3', '4']
        tmp_list = []
        for k, v in all_data[i].items():
            # 取出一个字典的值组成列表['1', '2'],第二次遍历为['3', '4']
            tmp_list.append(v)
        # value_tuple将['1', '2']转化为('1', '2')
        value_tuple = tuple(tmp_list)
        # 将各元组添加至最终的list，格式为[('1', '2'), ('3', '4')]
        value_list.append(value_tuple)
    # 将list转化为tuple,[('1', '2'), ('3', '4')] -> (('1', '2'), ('3', '4'))
    data = tuple(value_list)

    return data


@app.route('/', methods=['GET', 'POST'])
# 引导页面
def index():
    return render_template('index.html')


@app.route('/assets', methods=['GET', 'POST'])
# 查询网络资产
def show_assets():
    # mysql连接参数
    dbconn = pymysql.connect(
        host='192.168.72.129',
        user='root',
        database='iso_db_core',
        password='1',
        port=3306
    )
    cur = dbconn.cursor()
    # mysql查询语句
    sql = 'select * from t_assets_offline;'
    cur.execute(sql)
    assets = cur.fetchall()
    dbconn.close()

    return render_template('assets.html', assets=assets)


@app.route('/es', methods=['GET', 'POST'])
# 查询历史归档事件-ausdata_iso_eventdata
def show_es():
    if request.method == 'POST':
        index = request.form.get("index")
        if index.strip() == "":
            index = "ausdata_iso_eventdata_202210"
        return render_template('es.html', data=read_es(index))
    else:
        return render_template('es.html', data=read_es("ausdata_iso_eventdata_202210"))


@app.route('/md', methods=['GET', 'POST'])
# 查询短信发送记录
def show_md():
    if request.method == 'POST':
        name = request.form.get("username")
        phone = request.form.get("phone")
        # 判断name和Phone是否有输入，无输入则置为%
        if name.strip() == "":
            name = "%"
        else:
            name = name
        if phone.strip() == "":
            phone = "%"
        else:
            phone = phone
        return render_template('md.html', md=search_mysql(name, phone))
    else:
        return render_template('md.html', md=search_mysql("%", "%"))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
