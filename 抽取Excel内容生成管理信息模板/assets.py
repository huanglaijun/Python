import pandas as pd

# 步骤1: 读取网管导出的管理信息、2022/2023未录入资产
print("======================1========================")
df = pd.read_excel("C:/Users/1/Desktop/资产处理/网络资产管理信息_合并后.xlsx",
                   converters={"资产编号": str, "序列号": str})
df_2022 = pd.read_excel("C:/Users/1/Desktop/资产处理/待录入/资产结构树明细查询2023-10-26 -资产编号2022-未录入.xls",
                        converters={"资产标签号": str, "序列号": str})

# 步骤2: 对比2022未录入资产与网管导出资产,若为已有资产则更新<<2_管理信息导入模板.xlsx>>,若为未有资产则打印资产编号手动录入
print()
print("======================2========================")
# 用"资产结构树明细查询2023-10-26 -资产编号2022-未录入.xls"序列号去管理信息表中寻找
serial_list_df = df["序列号"].to_list()
serial_list_2022 = df_2022["序列号"].to_list()

# 序列号已存在的进入serial_inDataFrame_2022,最终进入2_管理信息导入模板.xlsx
# 序列号不存在进入serial_notInDataFrame_2022，最终进入1_未录入资产模板.xlsx
serial_inDataFrame_2022 = []
serial_notInDataFrame_2022 = []
for i in serial_list_2022:
    if i in serial_list_df:
        serial_inDataFrame_2022.append(i)
    else:
        serial_notInDataFrame_2022.append(i)

# 先处理未存在的资产，需手动录入，此处仅打印序列号
print(serial_notInDataFrame_2022)

# 处理需要更新管理信息的资产
mgn_data = {"序列号": "", "资产编号": "", "设备名称": "", "设备IP": "", "用途": "", "启用日期": "", "责任人": "", "购置时间": "", "购置合同": "", "设备提供商": "",
            "目前服务商": "", "维保开始时间": "", "维保结束时间": "", "所属数据中心": "", "区域位置": "", "机柜编号": "", "采购金额": "", "起始U位": "", "结束U位": "", "设备提供商": ""}

# 针对不同类型，都使用mgn_data模板生成DataFrame
# 上网代理服务器暂时选择为服务器
mgn_server_DataFrame=pd.DataFrame(mgn_data,index=[0])
# 路由器
mgn_router_DataFrame=pd.DataFrame(mgn_data,index=[0])
# 交换机
mgn_switch_DataFrame=pd.DataFrame(mgn_data,index=[0])
# 防火墙
mgn_fireWall_DataFrame=pd.DataFrame(mgn_data,index=[0])

for i in serial_inDataFrame_2022:
    # 根据序列号找出待录入资产表中数据，并找出网管已录入的资产数据
    item_2022_list = []
    item_list = []
    for item in df_2022.values:
        if item[11] == i:
            item_2022_list = item
    for item in df.values:
        if item[0] == i:
            item_list = item

    # 对比两个表数据，对管理信息导入模板字典赋值，并将数据插入到"2_管理信息导入模板.xlsx"
    # 序列号、资产编号、设备名称、设备IP、用途 以网管信息为准
    mgn_data["序列号"] = item_list[0]
    mgn_data["资产编号"] = item_list[1]
    mgn_data["设备名称"] = item_list[2]
    mgn_data["设备IP"] = item_list[3]
    mgn_data["用途"] = item_list[4]
    # 启用日期、责任人、购置时间、购置合同、设备提供商、目前服务商、维保开始时间、维保结束时间 以新表为准
    mgn_data["启用日期"] = item_2022_list[4]
    mgn_data["责任人"] = item_2022_list[5]
    mgn_data["购置时间"] = item_2022_list[3]
    mgn_data["购置合同"] = item_2022_list[20]
    mgn_data["设备提供商"] = item_2022_list[18]
    mgn_data["目前服务商"] = item_2022_list[18]
    mgn_data["维保开始时间"] = item_2022_list[16]
    mgn_data["维保结束时间"] = item_2022_list[17]
    mgn_data["所属数据中心"] = "总部数据中心"
    # 区域位置、机柜编号 以网管信息为准
    mgn_data["区域位置"] = item_list[14]
    mgn_data["机柜编号"] = item_list[15]
    # 采购金额 以新表为准
    mgn_data["采购金额"] = item_2022_list[10]
    # 起始U位、结束U位 以网管信息为准
    mgn_data["起始U位"] = item_list[17]
    mgn_data["结束U位"] = item_list[18]
    # 设备提供商 以新表为准
    mgn_data["设备提供商"] = item_2022_list[18]

    # 根据类型，将每条新记录插入至DataFrame
    if item_2022_list[2]=="上网代理设备":
        mgn_server_DataFrame=pd.concat([mgn_server_DataFrame,pd.DataFrame(mgn_data,index=[0])],ignore_index=True)
    elif item_2022_list[2]=="路由器":
        mgn_router_DataFrame=pd.concat([mgn_router_DataFrame,pd.DataFrame(mgn_data,index=[0])],ignore_index=True)
    elif item_2022_list[2]=="交换机":
        mgn_switch_DataFrame=pd.concat([mgn_switch_DataFrame,pd.DataFrame(mgn_data,index=[0])],ignore_index=True)
    elif item_2022_list[2]=="防火墙":
        mgn_fireWall_DataFrame=pd.concat([mgn_fireWall_DataFrame,pd.DataFrame(mgn_data,index=[0])],ignore_index=True)

# 将最终数据生成管理信息导入模板
with pd.ExcelWriter("C:/Users/1/Desktop/资产处理/2_管理信息导入模板.xlsx") as writer:
    mgn_fireWall_DataFrame.to_excel(writer,sheet_name="防火墙在线",encoding='gbk')
    mgn_router_DataFrame.to_excel(writer,sheet_name="路由器在线",encoding='gbk')
    mgn_server_DataFrame.to_excel(writer,sheet_name="服务器在线",encoding='gbk')
    mgn_switch_DataFrame.to_excel(writer,sheet_name="交换机在线",encoding='gbk')
