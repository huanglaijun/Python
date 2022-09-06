#!/bin/bash

#######################################################################################
# 此脚本用于将全行配置备份导出文件按预定格式以ftp方式传输至201服务器
########################################################################################
# 脚本分为两部分，第一部分处理压缩文件以及生成所需格式目录
# 第二部分将处理后的dev_cfg目录重命名为XXXX年XX月XX日格式并将压缩包传输至201

# 第一部分
# 声明配置备份导出默认保存路径
source /home/ismartone/.bash_profile

if [ -z "$AUTH_HOME" ];then
    AUTH_HOME=/opt/TDS/iSmartOne/iSmartOne-authentication
fi

default_path=${AUTH_HOME}/dev_cfg/

# org_path_file定义org_path_list.txt文件存放位置。
# org_path_list.txt为配置导出各任务设置的保存路径，若网管里修改的保存路径，则需同步修改org_path_list.txt文件，此脚本无须修改。
org_zonghang=/opt/TDS/cron_shell/config_export_to_201/org_zonghang.txt
org_fenhang=/opt/TDS/cron_shell/config_export_to_201/org_fenhang.txt

# zhwl及dir_name是单独对总行设置的变量，分行无须关注
zhwl="总行网络"
dir_name="配置备份"

# 分行配置路径
fenhang_dir="网管配置备份"
fenhang_month="/$(date +%Y年%m月)网管配置备份"

# 遍历org_path_list.txt中各路径，将各路径下文件解压为.conf模式，并删除zip文件，遍历后保持在default_path目录下
while read -r line
do
    cd "${default_path}""${line}"
    mkdir -p ${fenhang_dir}${fenhang_month}
    unzip configbackup_"$(date +%Y%m)*.zip"
    rm -rf ./*.zip
    mv ./*.conf ${fenhang_dir}${fenhang_month}
done < "${org_fenhang}"

# 在总行网络中创建“2022年配置备份/2022年$月配置备份”格式目录
dest_dir_year=$(date +%Y年)${dir_name}
dest_dir_month=/$(date +%Y年%m月)${dir_name}/
dest_dir=${dest_dir_year}${dest_dir_month}
# 总行网络中创建目标格式目录
cd ${default_path}${zhwl}
mkdir -p "${dest_dir}"

while read -r line
do
    cd "${default_path}""${line}"
    unzip configbackup_"$(date +%Y%m)*.zip"
    rm -rf ./*.zip
done < "${org_zonghang}"

# 将原总行网络下所有内容移至“2022年配置备份/2022年$月配置备份”目录
cd ${default_path}${zhwl}
mv $(ls | grep -v ${dest_dir_year}) "${dest_dir}"


#----------------------------------------------------------------
# 第二部分
# tmp_dir为将dev_cfg拷贝打包的中转目录，程序运行完毕后删除
tmp_dir=$(date +%Y-%m-%d)_configBackup
# dest_file为最终ftp发送到201的配置压缩包文件
dest_file=${tmp_dir}.tar.gz
# 定义系统默认输出的配置保存目录
default_dir=dev_cfg
shell_dir=/opt/TDS/cron_shell

# 进入默认用户模块所在目录
cd $AUTH_HOME || exit

# 将系统默认保存目录dev_cfg复制并改名为XXXX年XX月XX日格式目录
cp -rp "$default_dir" "$tmp_dir"

# 将新建的目录打包，并删除复制的多余目录
tar zcvf "$dest_file" "$tmp_dir"
rm -rf "$tmp_dir"
mv "$dest_file" "$shell_dir"

sleep 2s

# ftp方式将压缩包传输至201服务器
#ftp -v -n XX.XX.XX.XX <<EOF
#user USER PASSWORD
#binary
#lcd $shell_dir
#prompt
#mput $dest_file
#bye
#EOF

sleep 2s

# ftp传输后将压缩包删除
# 执行删除命令前，先确认工作路径，以免误删
cd $shell_dir || exit
# 安装tftp后下方一句取消注释
# rm -rf "$dest_file"
