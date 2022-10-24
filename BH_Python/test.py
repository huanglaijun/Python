import time


# ES时间戳13位，单位毫秒，需除以1000做转换
# 时间戳类型为<class 'int'>,转化后的类型为<class 'str'>
# time_stamp = 1664611790301
# time_local = time.strftime(
#     '%Y-%m-%d %H:%M:%S', time.localtime(time_stamp/1000))
# print("时间戳类型为{},转化后的类型为{}\n".format(type(time_stamp), type(time_local)))

# FGL2101110Q

# 定义一个结果样例
# ((),(),())遍历后将时间格式修改生成一个格式相同的元组

src = (('A', 'Y', '1664611790301'), ('B', 'N',
       '1664525300000'), ('C', 'N', '1664511835000'))

dest = []
for elem in src:
    elem_list = list(elem)
    int_elem_list2 = int(elem_list[2])/1000
    elem_list[2] = time.strftime(
        '%Y-%m-%d %H:%M:%S', time.localtime(int_elem_list2))
    elem_tuple = tuple(elem_list)
    dest.append(elem_tuple)
data = tuple(dest)
print("原始数据为：{}".format(src))
print("最终数据为：{}".format(data))
