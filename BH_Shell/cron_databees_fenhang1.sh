#!/bin/bash

####################################
# 此脚本用于定期重启fenhang1分区采集器
####################################

# 定义环境变量
if [ -z "$DATABEES_HOME" ];then
    DATABEES_HOME=/opt/TDS/iSmartOne/databees
fi

# 定义采集器停止函数
cron_stop(){
    /usr/bin/expect <<EOF
    set timeout 120
    spawn ssh ismartone@$1
    expect "DBS" { send "cd $2 || exit\n" }
    expect "DBS" { send "./databees.sh stop\n" }
    expect "DBS" { send "sleep 1s\n" }
    expect "DBS" { send "ps -ef | grep databees\n" }
    expect "DBS" { send "exit\n" }
    expect eof
EOF
}

# 定义采集器启动函数
cron_start(){
    /usr/bin/expect <<EOF
    set timeout 120
    spawn ssh ismartone@$1
    expect "DBS" { send "cd $2 || exit\n" }
    expect "DBS" { send "./databees.sh start\n" }
    expect "DBS" { send "sleep 1s\n" }
    expect "DBS" { send "ps -ef | grep databees\n" }
    expect "DBS" { send "exit\n" }
    expect eof
EOF
}

# 定义ip地址存放文件、远程用户
cron_databees_dir=/opt/TDS/cron_shell/cron_databees
fenhang1="$cron_databees_dir"/fenhang1.txt

# 读取ip地址文件登录服务器,停止采集器进程
cd "$cron_databees_dir" || exit
echo '' > ./cron_databees.log
{
    echo ''
    echo ''
    echo ''
    echo ========================================"$(date)  fenhang1分区采集器重启开始"======================================
} >> ./cron_databees.log
while read -r line
do
    cron_stop "$line" "$DATABEES_HOME" | tee -a ./cron_databees.log
done < "$fenhang1"

echo "--------------------------------------------------------------------------------------------------------------------" >> ./cron_databees.log

sleep 10s

# 启动采集器进程
while read -r line
do
    sleep 20s
    cron_start "$line" "$DATABEES_HOME" | tee -a ./cron_databees.log
    sleep 10s
done < "$fenhang1"