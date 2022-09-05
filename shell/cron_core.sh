#!/bin/bash

if [ -z "$CORE_HOME" ];then
    CORE_HOME=/opt/TDS/iSmartOne/iSmartOne-core
fi

shell_home=/opt/TDS/cron_shell/cron_core

cd $CORE_HOME || exit
echo '' > $shell_home/cron_core.log
echo "------------------$(date)  核心模块重启------------------------" >> $shell_home/cron_core.log
./iSmartOne.sh restart | tee -a $shell_home/cron_core.log
sleep 2s
{
    echo ''
    echo ''
} >> $shell_home/cron_core.log
ps -ef | grep core | tee -a $shell_home/cron_core.log
