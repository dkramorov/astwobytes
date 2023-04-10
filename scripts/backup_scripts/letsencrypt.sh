#!/usr/bin/expect -f
set timeout 57600
set CHAR "#"
set PASSWD "passwd\r"
set IP "192.168.1.3"

spawn rsync -a -e "ssh -p 9022" root@$IP:/etc/letsencrypt/ /etc/letsencrypt/
expect "root@192.168.1.3's password:"
send $PASSWD
expect eof

# CRON:
#SHELL=/bin/sh
#PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
#*/5 * * * * root /home/jocker/cron/letsencrypt.sh >/dev/null 2>&1
