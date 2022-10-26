# -*- coding: utf-8 -*-
import json
from msilib.schema import PatchPackage
import pymysql
import time
from elasticsearch import Elasticsearch
from flask import Flask, render_template, request, redirect


# 引用flask框架
app = Flask(__name__)


def read_mysql_md(name, phone):
    # 定义查询mysql短信记录的方法
    # mysql连接参数
    dbconn = pymysql.connect(
        # host='192.168.72.129',
        host='10.8.6.93',
        user='root',
        database='iso_db_core',
        # password='1',
        password='iso-Root_AUS^2019',
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


def read_mysql_assets(assetsno, serial):
    # 定义查询mysql读取资产的方法
    # assetsno：资产编号, serial：序列号
    dbconn = pymysql.connect(
        host='10.8.6.93',
        user='root',
        database='iso_db_core',
        password='iso-Root_AUS^2019',
        port=3306
    )
    cur = dbconn.cursor()
    sql = "select * from t_assets_offline WHERE ASSETSNO LIKE " + '"' +\
        assetsno + '"' + " AND SERIAL LIKE " + '"' + \
        serial+'"' + " AND NODEPATH LIKE '%/2/1095846/%';"
    print(sql)
    cur.execute(sql)
    asset = cur.fetchall()
    dbconn.close()

    # 对MySQL取回的原始数据样式为(('思科','{"orgName": "10837"}','{"f001CA043BFACBA6A": "",此段为管理信息json}'),(每一个元组为一条资产记录),())
    # 需将(('a1', 'b1', '{"k1": "v1","k2": "v2","k3":"","k4":""}', 'd1'), ('a2', 'b2', '{"k5": "v5","k6": "v6","k7":"","k8":""}', 'd2'))
    # 转化为：(('a1', 'b1', 'd1', 'v1', 'v2', '', ''),('a2', 'b2', 'v5', 'v6', '', ''))
    # 其中MGNTINFO字段存储的信息为管理信息，将管理信息提取出来展开至新数据队列，原MGNTINFO字段删除
    # 最终将t_assets_offline数据表中内容全部展开，数据中无json格式信息，达到基本信息和管理信息都在表columns中
    # -------------
    # 先将sql查询结果
    # 由(('a1', 'b1', '{"k1": "v1","k2": "v2","k3":"","k4":""}', 'd1'), ('a2', 'b2', '{"k5": "v5","k6": "v6","k7":"","k8":""}', 'd2'))
    # ->[('a1', 'b1', '{"k1": "v1","k2": "v2","k3":"","k4":""}', 'd1'), ('a2', 'b2', '{"k5": "v5","k6": "v6","k7":"","k8":""}', 'd2')]
    src_list = list(asset)
    # 定义最终assets结果列表
    assets_list = []
    # 由[('a1', 'b1', '{"k1": "v1","k2": "v2","k3":"","k4":""}', 'd1'), ('a2', 'b2', '{"k5": "v5","k6": "v6","k7":"","k8":""}', 'd2')]
    # ->[['a1', 'b1', '{"k1": "v1","k2": "v2","k3":"","k4":""}],['a2', 'b2', '{"k5": "v5","k6": "v6","k7":"","k8":""}', 'd2']]
    for i in range(0, len(src_list)):
        # 对列表的每一个元素遍历，并把管理信息value值取出,删除原MGNTINFO、ASSETSINFO字段
        # 由[['a1', 'b1', '{"k1": "v1","k2": "v2","k3":"","k4":""}],['a2', 'b2', '{"k5": "v5","k6": "v6","k7":"","k8":""}', 'd2']]
        # ->[['a1', 'b1', 'v1', 'v2', '', ''],['a2', 'b2', 'v5', 'v6', '', '']]
        # 最终样式为(('a1', 'b1', 'd1', 'v1', 'v2', '', ''),('a2', 'b2', 'v5', 'v6', '', ''))
        # 将list中每个元组转换为list
        src_item_list = list(src_list[i])
        # 管理信息虽为json格式，但却是str类型，需转为dict
        dict_mgntinfo = json.loads(src_item_list[14])
        # 取管理信息value值添加至src_mgntinfo_list
        src_mgntinfo_list = []
        for k, v in dict_mgntinfo.items():
            src_mgntinfo_list.append(v)
        # 删除原MGNTINFO
        src_item_list.pop(14)
        # 删除原ASSETSINFO
        src_item_list.pop(20)
        #
        # 基本信息和管理信息拼接
        src_to_list = src_item_list+src_mgntinfo_list
        # 基本信息和管理信息list转为tuple
        src_to_tuple = tuple(src_to_list)
        # 每个结果放进定义最终assets结果列表
        assets_list.append(src_to_tuple)
    # 最终assets需由list转为tuple
    assets = tuple(assets_list)
    return assets


def read_es(index):
    # 定义查询ES数据库方法，此函数仅限于读取ausdata_iso_eventdata历史归档事件索引
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

    # ES取回来的原始数据格式为[{'a':1,'b':2},{'a':3,'b':4},{'a':5,'b':6}]
    # 字典索引相同，只需要value值，即转化为：((1,2),(3,4),(5,6))
    # data_tmp为处理后的元组嵌套
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
    data_tmp = tuple(value_list)

    # data_tmp完成了数据抽取及类型转换，但是ES数据的时间格式为13位时间戳，需格式化输出
    # 由(('A', 'Y', '1664611790301'), ('B', 'N','1664525300000'))
    # 转化为(('A', 'Y', '2022-10-01 16:09:50'), ('B', 'N', '2022-09-30 16:08:20'))
    tmp = []
    for elem in data_tmp:
        elem_list = list(elem)
        # STATECHANGE格式转换
        int_elem_list_STATECHANGE = int(elem_list[13])/1000
        elem_list[13] = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(int_elem_list_STATECHANGE))
        # LASTOCCURRENCE格式转换
        int_elem_list_LASTOCCURRENCE = int(elem_list[19])/1000
        elem_list[19] = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(int_elem_list_LASTOCCURRENCE))
        # FIRSTOCCURRENCE
        int_elem_list_FIRSTOCCURRENCE = int(elem_list[37])/1000
        elem_list[37] = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(int_elem_list_FIRSTOCCURRENCE))
        # ARCHIVETIME
        int_elem_list_ARCHIVETIME = int(elem_list[53])/1000
        elem_list[53] = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(int_elem_list_ARCHIVETIME))
        # ACKTIME
        int_elem_list_ACKTIME = int(elem_list[25])/1000
        elem_list[25] = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(int_elem_list_ACKTIME))
        # DOWNTIME
        int_elem_list_DOWNTIME = int(elem_list[29])/1000
        elem_list[29] = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(int_elem_list_DOWNTIME))
        # 将[(),()]转化为((),())
        elem_tuple = tuple(elem_list)
        tmp.append(elem_tuple)
    data = tuple(tmp)

    return data


@app.route('/', methods=['GET', 'POST'])
# 引导页面
def index():
    return render_template('index.html')


@app.route('/assets', methods=['GET', 'POST'])
# 查询网络资产
def show_assets():
    if request.method == 'POST':
        assetsno = request.form.get("assetsno")
        serial = request.form.get("serial")
        # 判断assetsno和serial是否有输入，无输入则置为%
        if assetsno.strip() == "":
            assetsno = "%"
        else:
            assetsno = assetsno
        if serial.strip() == "":
            serial = "%"
        else:
            serial = serial
        return render_template('assets.html', assets=read_mysql_assets(assetsno, serial))
    else:
        return render_template('assets.html', assets=read_mysql_assets("%", "%"))


@app.route('/es', methods=['GET', 'POST'])
# 查询历史归档事件-ausdata_iso_eventdata
def show_es():
    if request.method == 'POST':
        index = request.form.get("index")
        if index.strip() == "":
            index = "ausdata_iso_eventdata_202209"
        return render_template('es.html', data=read_es(index))
    else:
        return render_template('es.html', data=read_es("ausdata_iso_eventdata_202209"))


@app.route('/md', methods=['GET', 'POST'])
# 查询所有短信发送记录
def show_md():
    if request.method == 'POST':
        name = request.form.get("username")
        phone = request.form.get("phone")
        # # 判断name和Phone是否有输入，无输入则置为%
        # if name.strip() == "":
        #     name = "%"
        # else:
        #     name = name
        # if phone.strip() == "":
        #     phone = "%"
        # else:
        #     phone = phone
        # return render_template('md.html', md=read_mysql_md(name, phone))

        # 只输入姓名时
        if name.strip() != "" and phone.strip() == "":
            name = name
            phone = "%"
            return render_template('md.html', md=read_mysql_md(name, phone))
        # 只输入手机号时
        elif name.strip() == "" and phone.strip() != "":
            name = "%"
            phone = phone
            return render_template('md.html', md=read_mysql_md(name, phone))
        # 手机号和姓名均输入时
        else:
            name = name
            phone = phone
            return render_template('md.html', md=read_mysql_md(name, phone))
    else:
        return render_template('md.html', md=read_mysql_md("#", "#"))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
