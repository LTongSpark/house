# /usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
import pymysql
import numpy as np

mysql_cn = pymysql.connect(host='10.212.4.34', port=3306, user='root', passwd='Admin@123', db='security_info')
data = pd.read_sql('select *  from ti_ua_new_user_innet_info_d ;', con=mysql_cn)
data["c_cust_cert_code"] = data["c_cust_cert_code"].str.replace('[a-zA-Z]', '10')
data.replace(to_replace="", value=np.nan, inplace=True)
data.replace(to_replace="NULL", value=np.nan, inplace=True)
data.fillna(value=0, inplace=True)

# 设置省份
data["province"] = data["c_cust_cert_code"].str[0:2]
data["prefecture"] = data["c_cust_cert_code"].str[0:2]
data["country"] = data["c_cust_cert_code"].str[0:2]

# 把入网时间拆分成不同的时间
time = pd.to_datetime(data['innet_date'])
time_value = pd.DatetimeIndex(time)
data["day"] = time_value.day
data["week"] = time_value.week
data["hour"] = time_value.hour
data["second"] = time_value.second
data["month"] = time_value.month

# 把关联号码的时间拆分成不同的时间
else_time = pd.to_datetime(data['else_innet_date'])
else_time_value = pd.DatetimeIndex(else_time)
data["else_day"] = else_time_value.day
data["else_week"] = else_time_value.week
data["else_hour"] = else_time_value.hour
data["else_second"] = else_time_value.second
data["else_month"] = else_time_value.month

x_test = data[['phone_no', 'cust_id', 'user_id', 'c_cust_cert_code',
               'age', 'c_real_name_flag', 'create_org_id', 'sts',
               'else_phone_no', 'else_cust_id', 'else_create_org_id',
               'else_sts', 'else_1_money', 'else_2_money',
               'else_3_money', "province", "day", "week", "hour",
               "second", "month", "else_day", "else_week", "else_second",
               'country', 'prefecture', "else_month"]]

print(x_test)

base_dir = "/home/xinanzhongxin/data"

with open(base_dir + '/static_phoneNum.txt', 'w+') as f:
    for i in x_test["phone_no"].values:
        f.write(str(i) + "\r")

std = StandardScaler()
x_test1 = std.fit_transform(x_test)
# 加载模型
model = joblib.load("/home/xinanzhongxin/modle/static_mode.pkl")
y_predict = model.predict(x_test1)

with open(base_dir + '/static_if_black.txt', 'w+') as f:
    for i in y_predict:
        f.write(str(i) + "\r")
# print("准确率：", lg.score(x_test1, y_test))
with open(base_dir + '/static_phoneNum.txt', 'r') as f:
    json_list = f.read().replace('\r', '').replace('\n', ',').split(',')

with open(base_dir + '/static_if_black.txt', 'r') as f:
    scores_list = f.read().replace('\r', '').replace('\n', ',').split(',')

with open(base_dir + '/static_result.txt', 'w+') as f:
    for index in zip(scores_list, json_list):
        f.write(index[0] + "\t\t" + index[1])