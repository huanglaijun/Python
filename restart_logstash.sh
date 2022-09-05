#!/bin/bash

# 此脚本用于重启syslog、acs

# 定义环境变量
if [ -z "$TDS_HOME" ];then
    TDS_HOME=/opt/TDS
fi

if [ -z "$LOGSTASH_HOME" ];then
    LOGSTASH_HOME=$TDS_HOME/logstash
fi

shell_dir=$TDS_HOME/cron_shell/restart_logstash/fenhang_syslog_acs
ip_file=$shell_dir/logstash_ip.txt

# 重启filebeat-acslog函数
restart_filebeat_acslog(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@$1
    expect "LOGSF" { send "cd $2/filebeat-acslog-5.6.5\n" }
    expect "LOGSF" { send "ps -ef|grep acslog\n" }
    expect "LOGSF" { send "./filebeat-acslog.sh restart\n" }
    expect "LOGSF" { send "ps -ef|grep acslog\n" }
    expect "LOGSF" { send "exit\n" }
    expect eof
EOF
}

# 重启filebeat-syslog函数
restart_filebeat_syslog(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@$1
    expect "LOGSF" { send "cd $2/filebeat-syslog\n" }
    expect "LOGSF" { send "ps -ef|grep filebeat-syslog\n" }
    expect "LOGSF" { send "./filebeat-syslog.sh restart\n" }
    expect "LOGSF" { send "ps -ef|grep filebeat-syslog\n" }
    expect "LOGSF" { send "exit\n" }
    expect eof
EOF
}

# 重启filebeat-syslogEvents函数
restart_filebeat_syslogEvents(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@$1
    expect "LOGSF" { send "cd $2/filebeat-syslogEvents\n" }
    expect "LOGSF" { send "ps -ef|grep filebeat-syslogEvents\n" }
    expect "LOGSF" { send "./filebeat-syslogEvents.sh restart\n" }
    expect "LOGSF" { send "ps -ef|grep filebeat-syslogEvents\n" }
    expect "LOGSF" { send "exit\n" }
    expect eof
EOF
}

# 重启logstash-acslog函数
restart_logstash_acslog(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@$1
    expect "LOGSF" { send "cd $2-5.6.5\n" }
    expect "LOGSF" { send "ps -ef|grep acslog\n" }
    expect "LOGSF" { send "./acslog.sh restart\n" }
    expect "LOGSF" { send "ps -ef|grep acslog\n" }
    expect "LOGSF" { send "exit\n" }
    expect eof
EOF
}

# 重启logstash-syslog函数
restart_logstash_syslog(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@$1
    expect "LOGSF" { send "cd $2\n" }
    expect "LOGSF" { send "ps -ef|grep syslog\n" }
    expect "LOGSF" { send "./syslog.sh restart\n" }
    expect "LOGSF" { send "ps -ef|grep syslog\n" }
    expect "LOGSF" { send "exit\n" }
    expect eof
EOF
}

# 重启logstash-syslog-to-kafka函数
restart_logstash_syslog_to_kafka(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@$1
    expect "LOGSF" { send "cd $2\n" }
    expect "LOGSF" { send "ps -ef|grep syslog-to-kafka\n" }
    expect "LOGSF" { send "./syslog-to-kafka.sh restart\n" }
    expect "LOGSF" { send "ps -ef|grep syslog-to-kafka\n" }
    expect "LOGSF" { send "exit\n" }
    expect eof
EOF
}

# 调用函数，重启分行logstash、acs
cd "$shell_dir" || exit
{
        echo ''
        echo ''
        echo "=================$(date)  重启logstash================"
} > restart_logstash.log
while read -r line
do
    restart_filebeat_syslog "$line" "$TDS_HOME" | tee -a ./restart_logstash.log
    sleep 5s
    restart_filebeat_syslogEvents "$line" "$TDS_HOME" | tee -a ./restart_logstash.log
    sleep 5s
    restart_logstash_syslog "$line" "$LOGSTASH_HOME" | tee -a ./restart_logstash.log
    sleep 5s
    restart_logstash_syslog_to_kafka "$line" "$LOGSTASH_HOME" | tee -a ./restart_logstash.log
    sleep 5s
done < "$ip_file"
