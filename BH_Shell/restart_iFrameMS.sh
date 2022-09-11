#!/bin/bash

if [ -z "$TDS_HOME" ];then
    TDS_HOME=/opt/TDS
fi

if [ -z "$IFRAMEMS_HOME" ];then
    IFRAMEMS_HOME=/opt/TDS/iSmartOne/iSmartOne-iFrameMS
fi

shell_dir="$TDS_HOME"/cron_shell/restart_iFrameMS

restart_iFrameMS(){
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh ismartone@XX.XX.XX.XX
    expect "IF1" { send "cd $1\n" }
    expect "IF1" { send "ps -ef|grep iFrameMS\n" }
    expect "IF1" { send "./iSmartOne.sh restart\n" }
    expect "IF1" { send "ps -ef|grep iFrameMS\n" }
    expect "IF1" { send "exit\n" }
    expect eof
EOF
}

cd "$shell_dir" || exit
{
    echo ''
    echo ''
    echo "===============$(date)  重启iFrameMS==============="
} > ./restart_iFrameMS.log

restart_iFrameMS "$IFRAMEMS_HOME" | tee -a ./restart_iFrameMS.log
