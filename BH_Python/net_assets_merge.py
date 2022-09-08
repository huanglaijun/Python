import pandas as pd

########################################################################################################################
# -------------将网络资产管理信息各sheet页合并至一个sheet、并与基本信息合并(唯一性标识为'资产编号+序列号')------------------
# 定义基本信息、管理信息文件存放路径
mgn_data_path = "C:/Users/1/Desktop/网络资产/网络资产管理信息.xlsx"
base_data_path = "C:/Users/1/Desktop/网络资产/网络资产基本信息.xlsx"

# 将管理信息各sheet页合并为一页 *****方法一*****
mgn_df = pd.read_excel(mgn_data_path, sheet_name=None,
                       converters={"资产编号": str, "序列号": str})   # 设置资产编号、序列号str类型，避免科学计数法
mgn_data = pd.concat(mgn_df).set_index("序列号")

# 将合并后的管理信息导出为“网络资产管理信息_合并后.xlsx”
mgn_data["启用日期"] = pd.to_datetime(mgn_data["启用日期"], format="%Y-%m-%d")
mgn_data.to_excel("C:/Users/1/Desktop/网络资产/网络资产管理信息_合并后.xlsx", encoding='gbk')

# 读取基本信息文件，注意：因基本信息只有一页，此处不能添加sheet_name=None选项，否则merge会出现报错。如基本信息有多页，先合并至一页再merge
base_data = pd.read_excel(base_data_path,  converters={
                          "资产编号": str, "序列号": str})

# 合并基本信息、管理信息，并导出至“网络资产信息_合并.xlsx”
# how='outer'表示结果取并集。即：资产编号+序列号如果基本信息和管理信息表不同，也保留此行数据至合并后的表
# indicator=True表示在导出的表中说明合并后数据来源于管理信息还是基本信息
data = pd.merge(mgn_data, base_data, on=[
                "资产编号", "序列号"], how="outer", indicator=True).set_index("序列号")
data.to_excel("C:/Users/1/Desktop/网络资产/网络资产信息_合并后.xlsx",
              encoding='gbk', sheet_name="A-S列管理信息_T列后基本信息")

# 将管理信息各sheet页合并为一页 *****方法二*****
# df = pd.read_excel("C:/Users/1/Desktop/网络资产/网络资产管理信息.xlsx", sheet_name=None)
# # 获取各sheet名，添加至列表
# sheet_list = []
# for sheet in df:
#     sheet_list.append(sheet)
# data = [pd.read_excel("C:/Users/1/Desktop/网络资产/网络资产管理信息.xlsx",
#                       sheet_name=index) for index in range(len(sheet_list))]
# pd.concat(data).set_index("序列号").to_excel(
#     "C:/Users/1/Desktop/网络资产/网络资产管理信息_合并后.xlsx",encoding='gbk')

##########################################################################################################################
# ---------------根据设备IP+设备名称合并两个sheet页，将运维分组从管理信息添加至基本信息中。并将合并的结果保存至xlsx文件------------
# sheet_name=None返回的是excel文件中所有的sheet
# df = pd.read_excel("C:/Users/1/Desktop/设备资产信息.xlsx", sheet_name=None)

# # 打印sheet页名称
# for sheet in df:
#     print(sheet)

# # 根据设备IP+设备名称合并两个sheet页，并保存结果至新excel文件
# data = pd.merge(df['Sheet1'], df['Sheet2'], on=[
#                 "设备IP", "设备名称"]).set_index("设备IP")
# print(data.columns)
# data.to_excel("C:/Users/1/Desktop/设备资产信息_合并后.xlsx", encoding='gbk')  # 中文使用gbk
