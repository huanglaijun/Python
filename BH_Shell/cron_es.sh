#!/bin/bash

#############################################
# 此脚本用于判断ES集群状态，重启进程不在的es节点
#############################################


# 登录ES的master节点，查询ES集群状态
check_es(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@10.6.10.83
    expect "HQ-ESM1-83" { send "cd /opt/TDS/cron_shell/cron_es\n" }
    expect "HQ-ESM1-83" { send "curl http://XX.XX.XX.XX:9200/_cat/nodes > es_ip_now.txt\n" }
    expect "HQ-ESM1-83" { send "sleep 2s\n" }
    expect "HQ-ESM1-83" { send "scp ./es_ip_now.txt ismartone@XX.XX.XX.XX:/opt/TDS/cron_shell/cron_es\n" }
    expect "HQ-ESM1-83" { send "sleep 2s\n" }
    expect "HQ-ESM1-83" { send "exit\n" }
    expect eof
EOF
}

# 将es查询结果与定义的es节点比对，判断是否有节点DOWN掉,生成异常节点IP地址txt
check_ip(){
    cd "$CRON_ES_HOME" || exit
    rm -rf diff*.txt
    awk '{print $1,$NF}' "$ip_now" > tmp.txt
    rm -rf "$ip_now" && mv tmp.txt "$ip_now"
    # 查询A文件有，但B文件没有,保存至C文件 cat A B B | sort | uniq -u > c.txt
    cat "$ip_all" "$ip_now" "$ip_now" | sort | uniq -u > "$ip_diff"
    sleep 1s
}

# 远程登录es服务器，重启该节点es进程
es_restart(){
    /usr/bin/expect <<EOF
    set timeout 120
    spawn ssh ismartone@$1
    expect "$3" { send "cd $2\n" }
    expect "$3" { send "./elasticsearch.sh restart\n" }
    expect "$3" { send "sleep 3s\n" }
    expect "$3" { send "ps -ef | grep elastic\n"}
    expect "$3" { send "exit\n" }
    expect eof
EOF
}

# 检查master节点是否正常
check_master(){
    /usr/bin/expect <<EOF
    spawn ssh ismartone@$1
    expect "HQ-ESM" { send "cd /opt/TDS/cron_shell/cron_es\n" }
    expect "HQ-ESM" { send "ps -ef | grep elasticsearch | grep -v grep | grep -v modules | wc -l > es_ip_now.txt\n" }
    expect "HQ-ESM" { send "sleep 2s\n" }
    expect "HQ-ESM" { send "scp ./es_ip_now.txt ismartone@XX.XX.XX.XX:/opt/TDS/cron_shell/cron_es\n" }
    expect "HQ-ESM" { send "sleep 2s\n" }
    expect "HQ-ESM" { send "exit\n" }
    expect eof
EOF
}

# 重启master节点
master_restart(){
    /usr/bin/expect <<EOF
    set timeout 120
    spawn ssh ismartone@$1
    expect "HQ-ESM" { send "cd /opt/TDS/elasticsearch\n" }
    expect "HQ-ESM" { send "./elasticsearch.sh restart\n" }
    expect "HQ-ESM" { send "sleep 3s\n" }
    expect "HQ-ESM" { send "ps -ef | grep elastic\n"}
    expect "HQ-ESM" { send "exit\n" }
    expect eof
EOF
}

# 判断MASTER节点是否正常
master_status(){
    count_master=$(cat "$ip_now")
    if [ "$count_master" -eq 1 ];then
        echo "----MASTER $1 节点正常-----" >> cron_es.log
    else
        echo "----MASTER $1 节点不正常，需重启-----" >> cron_es.log
        master_restart "$1" | tee -a cron_es.log
    fi
}

# 定义变量
if [ -z "$TDS_HOME" ];then
    TDS_HOME=/opt/TDS
fi

if [ -z "$ES_HOME" ];then
    ES_HOME=$TDS_HOME/elasticsearch
fi

if [ -z "$CRON_ES_HOME" ];then
    CRON_ES_HOME=$TDS_HOME/cron_shell/cron_es
fi

# 定义check_ip函数比较过程中产生的ip文件
ip_all=$CRON_ES_HOME/es_ip_all.txt
ip_now=$CRON_ES_HOME/es_ip_now.txt
ip_diff=$CRON_ES_HOME/diff_ip.txt
ip_master=$CRON_ES_HOME/master_ip.txt

############开始判断逻辑#########
cd $CRON_ES_HOME || exit
{
    echo ''
    echo ''
    echo "############################################$(date)  ES检查开始###########################################################################"
} > cron_es.log
# 判断MASTER节点是否异常的逻辑
while read -r line
do
    check_master "$line"
    sleep 1s
    master_status "$line"
    sleep 1s
done < "$ip_master"
echo "------其它节点检查开始------" >> cron_es.log
sleep 20s
check_es
sleep 10s
check_ip
sleep 10s
# 判断是否有非master节点异常，异常重启非master节点
if [ -s "$ip_diff" ];then
    while read -r line
    do
        problem_ip=$(echo "$line" | awk '{print $1}')
        problem_host=$(echo "$line" | awk '{print $2}')
        echo "$problem_ip"
 	    echo ---"有问题的服务器为：$problem_host IP为$problem_ip"--- >> cron_es.log
	    echo ======================================================= >> cron_es.log
  	    echo "$problem_host"
	    sleep 5s
        es_restart "$problem_ip" "$ES_HOME" "$problem_host" | tee -a cron_es.log
    done < "$ip_diff"
else
    echo ------------"$(date)---ES所有节点正常"-------------------- >> cron_es.log
    exit
fi
