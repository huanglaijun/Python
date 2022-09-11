#!/bin/bash

########################################
# 此脚本用于清理kafka短信缓存及重启md程序
########################################

# 停止md程序
stop_md(){
    cd /opt/TDS/iSmartOne/iSmartOne-md || exit
    ./iSmartOne.sh stop
    sleep 3s
    ps -ef|grep iSmartOne-md
}

# 启动md程序
start_md(){
    cd /opt/TDS/iSmartOne/iSmartOne-md || exit
    ./iSmartOne.sh start
    sleep 3s
    ps -ef|grep iSmartOne-md
}

# 清除kafka短信topic
del_kafka_topic(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@XX.XX.XX.XX
    expect "HQ-KS3-155" { send "cd /opt/TDS/kafka || exit\n" }
    expect "HQ-KS3-155" { send "bin/kafka-topics.sh --list --zookeeper HQ-ZR1-89:2181,HQ-ZR2-90:2181,HQ-ZR3-91:2181,HQ-ZR4-92:2181,HQ-ZR5-93:2181/kafka-other\n" }
    expect "HQ-KS3-155" { send "sleep 5s\n" }
    expect "HQ-KS3-155" { send "bin/kafka-topics.sh -delete --zookeeper HQ-ZR1-89:2181,HQ-ZR2-90:2181,HQ-ZR3-91:2181,HQ-ZR4-92:2181,HQ-ZR5-93:2181/kafka-other --topic ausware-message\n" }
    expect "HQ-KS3-155" { send "sleep 5s\n" }
    expect "HQ-KS3-155" { send "bin/kafka-topics.sh --list --zookeeper HQ-ZR1-89:2181,HQ-ZR2-90:2181,HQ-ZR3-91:2181,HQ-ZR4-92:2181,HQ-ZR5-93:2181/kafka-other\n" }
    expect "HQ-KS3-155" { send "sleep 5s\n" }
    expect "HQ-KS3-155" { send "exit\n" }
    expect eof
EOF
}

# 调用函数，清理kafka缓存并重启md
cd /opt/TDS/cron_shell/cron_md || exit
{
    echo "##################################################################################################################"
    echo ---------------------------------"$(date)  清理kafka缓存及重启md开始----------------------------"
    echo ''
    echo ''
} > ./cron_md.log

stop_md | tee -a ./cron_md.log
sleep 5s
del_kafka_topic | tee -a ./cron_md.log
sleep 5s
start_md | tee -a ./cron_md.log
