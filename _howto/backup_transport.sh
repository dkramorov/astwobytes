#!/usr/bin/expect -f
set timeout 57600

# expect uses TCL language

set ARGS_COUNT [llength $argv]
if {$ARGS_COUNT == 1} {
    puts "--- start ---"
} else {
    puts "not enough argument for path"
    exit
}

# Обязательный аргумент
set DEST [lrange $argv 0 0]

set YANDEX_DISK "https://webdav.yandex.ru:443"
set LOGIN "kimadav\r"
set PASSWD "rbvflfd\r"

spawn mount_webdav -i $YANDEX_DISK $DEST
expect "Username:"
send $LOGIN
expect "Password:"
send $PASSWD
expect eof

