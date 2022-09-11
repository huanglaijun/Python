#!/bin/bash

###########################################
# 此脚本用于设置网管服务器间的免密登录
###########################################

# 定义在本机自动生成密钥的函数
ssh_keygen(){
    # EOF用于追加多行内容
    /usr/bin/expect <<EOF
    set timeout 15
    spawn ssh-keygen -t rsa
    expect {
        ".ssh/id_rsa" { send "\r"; exp_continue }
        "empty for no passphrase" { send "\r"; exp_continue }
        "passphrase again:" { send "\r"; exp_continue }
    }
EOF
}

# 定义将密钥传输至目标系统的函数
# timeout参数需设置大一些，设置小容易匹配不到password发送语句
send_ssh_key(){
    cd /home/ismartone/.ssh || exit
    /usr/bin/expect <<EOF
    set timeout 60
    spawn ssh-copy-id -i id_rsa.pub $1@$2
    expect {
        "yes/no"  { send "yes\r"; exp_continue }
        "assword" { send "$3\r"; exp_continue }
    }
EOF
}

# 定义密钥文件
pub_key_file=/home/ismartone/.ssh/id_rsa.pub

# 判断密钥文件是否存在，不在则生成密钥
if [ ! -f "${pub_key_file}" ]; then
    ssh_keygen
fi

sleep 2s

# 定义远程用户、密码、IP
remote_user=ismartone
passwd=password
ip_file=/opt/TDS/cron_shell/ssh_askpass/ip_all.txt


# 调用传输密钥函数对各目标系统做免密登录
while read -r line
do
    send_ssh_key "$remote_user" "$line" "$passwd"
done < ${ip_file}






# ----------------------------------------------------------------
# [root@control .ssh]# ll
# total 4
# -rw-r--r--. 1 root root 171 Aug 19 08:59 known_hosts


# [root@control .ssh]# ssh-keygen -t rsa
# Generating public/private rsa key pair.
# Enter file in which to save the key (/root/.ssh/id_rsa): 
# Enter passphrase (empty for no passphrase): 
# Enter same passphrase again: 
# Your identification has been saved in /root/.ssh/id_rsa.
# Your public key has been saved in /root/.ssh/id_rsa.pub.
# The key fingerprint is:
# SHA256:TonYhs+bPyNIXZn4CkPbdRU1TS/CXz0sQ3vm6WyfXbs root@control
# The key's randomart image is:
# +---[RSA 2048]----+
# |            .+oo.|
# |           .o o.+|
# |       . o .o+.=+|
# |    .+..=..  o*oo|
# |   .o+++S.    .o |
# |    =+oo.     o  |
# |   . +o..      +.|
# |    . ooo     . *|
# |      oo.o     E+|
# +----[SHA256]-----+
# [root@control .ssh]# 
# [root@control .ssh]# 
# [root@control .ssh]# ssh-copy-id -i id_rsa.pub root@node1
# /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "id_rsa.pub"
# The authenticity of host 'node1 (192.168.72.130)' can't be established.
# ECDSA key fingerprint is SHA256:wHT694XrZzZyzbMbDn72ogDy+t5+TyyxLOmG0QSddAI.
# ECDSA key fingerprint is MD5:cd:81:b7:b4:5c:42:4f:ee:31:85:9c:ee:c6:fd:37:36.
# Are you sure you want to continue connecting (yes/no)? yes
# /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
# /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
# root@node1's password: 

# Number of key(s) added: 1

# Now try logging into the machine, with:   "ssh 'root@node1'"
# and check to make sure that only the key(s) you wanted were added.

# [root@control .ssh]# ssh root@node1
# Last login: Thu Aug 18 17:58:52 2022 from 192.168.72.129
# [root@node1 ~]# exit
# logout
# Connection to node1 closed.
# [root@control .ssh]
