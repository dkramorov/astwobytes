#!/usr/bin/expect -f
#set timeout 28800
set timeout 57600
#set MNT [lrange $argv 0 0]

# --------------------------------
# полный путь до локального файла,
# который отрпвляем
# --------------------------------
set fname [lindex $argv 0] 
# ------------------------------
# Папка куда отправляем файл
# относительно /home/jocker/www/
# то есть без начального слеша
# ------------------------------
set folder [lindex $argv 1] 

# MNT - файл откуда берем, соответственно для сохранения структуры
# необходимо в MNT копировать на новом сервере - это должен быть 
# относительный путь типа media/...

#jocker@jockbook:~/django/archive/myscripts$ ssh -i RSA_irkutskpictures_com irkutskpictures.com
#Enter passphrase for key 'RSA_irkutskpictures_com': 

#jocker@jockbook:~/django/archive/myscripts$ scp -i RSA_irkutskpictures_com 1.txt irkutskpictures.com:/home/jocker/www/
#Enter passphrase for key 'RSA_irkutskpictures_com': 

#spawn ssh -p 9022 jocker@10.10.10.253
#expect "password:"
#send "PASSWD\r"
#expect "#"
#send "python /home/jocker/get_backup.py\r"
#expect "#"
#send "exit\r"
#expect "#"

spawn ssh jocker@irkutskpictures.com "mkdir -p /home/jocker/www/$folder"
expect "password:"
send "PASSWD\r"
expect "#"

#spawn scp 1.txt jocker@irkutskpictures.com:/home/jocker/www/1.txt
#spawn scp $MNT jocker@irkutskpictures.com:/home/jocker/www/$MNT

spawn scp $fname jocker@irkutskpictures.com:/home/jocker/www/$folder
# ДЕЙСТВИЕ : ./expect_remote.sh /home/jocker/django/archive/myscripts/1.txt media/123/
# РЕЗУЛЬТАТ : spawn scp /home/jocker/django/archive/myscripts/1.txt jocker@irkutskpictures.com:/home/jocker/www/media/123/
expect "password:"
send "PASSWD\r"

#expect "#"
expect eof


#spawn scp -P 9022 $MNT/bis_223.tar.gz root@10.10.10.253:/home/jocker/
#expect "password:"
#send "PASSWD\r"
#expect "#"
#spawn scp -P 9022 $MNT/sites.tar.gz root@10.10.10.253:/home/jocker/
#expect "password:"
#send "PASSWD\r"
#expect "#"
#spawn ssh root@10.10.10.253 -p 9022
#expect "password:"
#send "PASSWD\r"
#expect "#"
#send "python /home/jocker/work.py\r"
#expect "#"
#send "exit\r"
