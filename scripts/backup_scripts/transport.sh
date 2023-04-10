#!/usr/bin/expect -f
set timeout 57600
set MNT [lrange $argv 0 0]
set CLEANER "python /home/jocker/archive/backup_scripts/cleaner.py\r"
set DEST "/home/jocker/backup/"
set IP "188.225.73.29"
set PORT "9022"
set LOGIN "root"
set PASSWD "passwd\r"
set CHAR "#"

#################################################
# DEBUG
#################################################
#set IP "192.168.1.4"

#################################################
# Аргументом:
#################################################
# MNT архив, который будем переправлять
#################################################
# DEST папку КУДА будем копировать бекапы
# CHAR - ожидаем приглашения # или $
# CLEANER - скрипт по завершению всех работ
#################################################
# КУДА подключаемся:
#################################################
# IP адрес сервера
# PORT порт сервера
# LOGIN имя пользователя
# PASSWD пароль
#################################################
# EXAMPLE :
#################################################
#set MNT "/home/jocker/django/archive/backup_scripts/test.txt"
#################################################

spawn scp -P $PORT $MNT $LOGIN@$IP:$DEST
expect "password:"
send $PASSWD
expect $CHAR
#spawn ssh $LOGIN@$IP -p $PORT
#expect "password:"
#send $PASSWD
#expect $CHAR
#send $CLEANER
#expect "#"
send "exit\r"
expect eof

