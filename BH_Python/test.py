import time
import json


# ES时间戳13位，单位毫秒，需除以1000做转换
# 时间戳类型为<class 'int'>,转化后的类型为<class 'str'>
# time_stamp = 1664611790301
# time_local = time.strftime(
#     '%Y-%m-%d %H:%M:%S', time.localtime(time_stamp/1000))
# print("时间戳类型为{},转化后的类型为{}\n".format(type(time_stamp), type(time_local)))

# FGL2101110Q

# 定义一个结果样例
# ((),(),())遍历后将时间格式修改生成一个格式相同的元组

# src = (('A', 'Y', '1664611790301'), ('B', 'N',
#        '1664525300000'), ('C', 'N', '1664511835000'))

# dest = []
# for elem in src:
#     elem_list = list(elem)
#     int_elem_list2 = int(elem_list[2])/1000
#     elem_list[2] = time.strftime(
#         '%Y-%m-%d %H:%M:%S', time.localtime(int_elem_list2))
#     elem_tuple = tuple(elem_list)
#     dest.append(elem_tuple)
# data = tuple(dest)
# print("原始数据为：{}".format(src))
# print("最终数据为：{}".format(data))


# -------------------------------------------------------------------------------
# 管理信息对应关系
# {"f14E58D4C7A6FE909": "hlj-管理信息测试-可删除此处填写",
# "fF6879B6EF3A00FE7": "总部数据中心"}   设备别名 数据中心
src = (
    'a', 'b', '{"f14E58D4C7A6FE909": "管理信息测试","fF6879B6EF3A00FE7": "总部数据中心"}', 'd')
src_list = list(src)
# print("原始数据转化为list的结果为{}".format(src_list))
# print("json数据段提取的结果为:{},数据格式为:{}".format(src_list[2], type(src_list[2])))

json_dict = json.loads(src_list[2])
print("json转化为字典的结果为:{},数据格式为{}".format(json_dict, type(json_dict)))
json_list = []
for k, v in json_dict.items():
    json_list.append(v)
print("将json中的value值提取到list中的结果为:{}".format(json_list))

# pop语句需要写在最后面,先把json数据段删除掉，再将剩余数据拼接
src_list.pop(2)
print("删除json数据段的list为:{}".format(src_list))

dest_list = []
dest_list = src_list+json_list
dest_tuple = tuple(dest_list)
print(dest_tuple)
