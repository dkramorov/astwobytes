#!/usr/bin/expect -f
set timeout 7200
set MNT [lrange $argv 0 0]

spawn ssh -p 9022 root@10.10.10.253
expect "password:"
send "engeiCoh0aiY\r"
expect "#"
send "python /home/jocker/get_pics.py\r"
expect "#"
send "exit\r"
expect "#"
spawn scp -P 9022 root@10.10.10.253:/home/jocker/\{lpics.tar.gz,apics.tar.gz,pics.tar.gz} $MNT
expect "password:"
send "engeiCoh0aiY\r"
expect eof
