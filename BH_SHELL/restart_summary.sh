#!/bin/bash

if [ -z "$TDS_HOME" ];then
    TDS_HOME=/opt/TDS
fi

if [ -z "$ISMARTONE_HOME" ];then
    ISMARTONE_HOME=/opt/TDS/iSmartOne
fi

shell_dir="$TDS_HOME"/cron_shell/restart_summary

restart_summary(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@10.6.10.153
    expect "KS1" { send "cd $1/iSmartOne-summary\n" }
    expect "KS1" { send "ps -ef|grep summary\n" }
    expect "KS1" { send "./summary.sh restart\n" }
    expect "KS1" { send "ps -ef|grep summary\n" }
    expect "KS1" { send "exit\n" }
    expect eof
EOF
}

cd "$shell_dir" || exit
{
    echo ''
    echo ''
    echo "===============$(date)  重启summary==============="
} > ./restart_summary.log

restart_summary "$ISMARTONE_HOME" | tee -a ./restart_summary.log
