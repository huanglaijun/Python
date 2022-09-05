#!/bin/bash

# 此脚本用于重启datatunnel
# 前三台停止用shutdown.sh，启动用./submit-perf.sh start
# 后两台只在第一台shutdown.sh startup.sh

# 定义环境变量
if [ -z "$TDS_HOME" ];then
    TDS_HOME=/opt/TDS
fi

if [ -z "$DATATUNNEL_HOME" ];then
    DATATUNNEL_HOME="$TDS_HOME"/iSmartOne/datatunnel
fi

shell_dir="$TDS_HOME"/cron_shell/restart_datatunnel
ip_one_to_three_file="$shell_dir"/ip_one_two_three.txt

# 前三台datatunnel停止函数
first_shutdown(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@$1
    expect "SD" { send "cd $2/bin\n" }
    expect "SD" { send "ps -ef|grep datatunnel\n" }
    expect "SD" { send "./shutdown.sh\n" }
    expect "SD" { send "ps -ef|grep datatunnel\n" }
    expect "SD" { send "exit\n" }
    expect eof
EOF
}

# 前三台datatunnel启动函数
first_start(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@$1
    expect "SD" { send "cd $2/bin\n" }
    expect "SD" { send "ps -ef|grep datatunnel\n" }
    expect "SD" { send "./submit-perf.sh start\n" }
    expect "SD" { send "ps -ef|grep datatunnel\n" }
    expect "SD" { send "exit\n" }
    expect eof
EOF
}

# 后两台datatunnel停止函数，只在131操作
second_shutdown(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@10.6.10.131
    expect "SD" { send "cd $1/bin\n" }
    expect "SD" { send "ps -ef|grep datatunnel\n" }
    expect "SD" { send "./shutdown.sh\n" }
    expect "SD" { send "ps -ef|grep datatunnel\n" }
    expect "SD" { send "exit\n" }
    expect eof
EOF
}

# 后两台datatunnel启动函数，只在131操作
second_start(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@10.6.10.131
    expect "SD" { send "cd $1/bin\n" }
    expect "SD" { send "ps -ef|grep datatunnel\n" }
    expect "SD" { send "./startup.sh\n" }
    expect "SD" { send "ps -ef|grep datatunnel\n" }
    expect "SD" { send "exit\n" }
    expect eof
EOF
}

# 调用函数，重启datatunnel集群
cd "$shell_dir" || exit
{
    echo ''
    echo ''
    echo ''
    echo "========================$(date) 重启datatunnel集群===================="
} > ./restart_datatunnel.log

# 停止前三台datatunnel
while read -r line
do
    first_shutdown "$line" "$DATATUNNEL_HOME" | tee -a ./restart_datatunnel.log
    sleep 5s
done < "$ip_one_to_three_file"

sleep 20s

# 启动前三台datatunnel
while read -r line
do
    first_start "$line" "$DATATUNNEL_HOME" | tee -a ./restart_datatunnel.log
    sleep 5s
done < "$ip_one_to_three_file"

# 重启第四台datatunnel
second_shutdown "$DATATUNNEL_HOME" | tee -a ./restart_datatunnel.log
sleep 20s
second_start "$DATATUNNEL_HOME" | tee -a ./restart_datatunnel.log
