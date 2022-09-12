# -*- coding: utf-8 -*- 
import pandas as pd
import pymysql
from flask import Flask, render_template, request, redirect


# 引用flask框架
app = Flask(__name__)


# 定义查询数据库方法
def search_mysql(name, phone):
    # mysql连接参数
    dbconn = pymysql.connect(
        host='192.168.72.129',
        user='root',
        database='iso_db_core',
        password='1',
        port=3306
    )
    cur = dbconn.cursor()
    sql = "select * from t_evt_sent_sms WHERE NAME LIKE " + '"' +\
        name + '"' + " AND PHONE LIKE " + '"' + \
        phone+'"' + " order by LASTSENDTIME desc;"
    print(sql)
    cur.execute(sql)
    md = cur.fetchall()
    dbconn.close()
    return md

# 查询网络资产


@app.route('/assets', methods=['GET', 'POST'])
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


# 查询短信发送记录


@app.route('/md', methods=['GET', 'POST'])
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
