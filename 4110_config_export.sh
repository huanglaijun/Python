#!/bin/bash

#################################################
# 此脚本用于将4110防火墙配置以ftp方式传输至第三方平台
#################################################

# 定义配置备份导出任务默认路径及4110任务自定义保存路径
source /home/ismartone/.bash_profile

if [ -z "$AUTH_HOME" ];then
    AUTH_HOME=/opt/TDS/iSmartOne/iSmartOne-authentication
fi

dev_path=${AUTH_HOME}/dev_cfg/
customer_dir=4110_Firewall

# 解压4110配置导出文件仅保留conf结尾文件
cd ${dev_path}${customer_dir} || exit
# 检测4110配置导出任务是否生成了正确的目录，若任务没有生成对应目录则程序退出，不执行后续命令
unzip ./*.zip && rm -rf ./*.zip

# 解压后10秒开始传输至第三方平台
sleep 2s

# 定义ftp方式传输至第三方平台的信息
ftp -v -n 10.5.4.101 <<EOF
user network 1qazXSW@
binary
lcd ${dev_path}${customer_dir}
prompt
mput *.conf
bye
EOF

# 传输后间隔10秒再进行清空操作
sleep 2s

# 传输后2秒清空4110目录本身，此命令用于将4110配置从每月1日全行配置备份中删除
cd ${dev_path} || exit
rm -rf ${customer_dir}

