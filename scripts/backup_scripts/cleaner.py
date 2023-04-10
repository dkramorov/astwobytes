#!/usr/bin/env/python
#-*- coding:utf8 -*-
import datetime
import time
import os
import re

#################################################
# Старые папки можно удалить (дней назад)
# WITH MINUS
#################################################
long_ago = -5 
#################################################
# Папка, где нужна уборка АРХИВОВ
# %Y_%m_%d.tar.gz
#################################################
backup_path = "/home/jocker/backup/"
#################################################
# Названия папок бекапа
#################################################
rega_date = re.compile("^([0-9]{4}-[0-9]{1,2}-[0-9]{1,2}).tar.gz$")

started = time.time()
now = datetime.datetime.today()
print "we started at", now

# RESET system clock PROTECTION
dino = "01-01-2012"
test_date = datetime.datetime.strptime(dino, "%d-%m-%Y")
if now < test_date:
  print "[ERROR] System date lower than", dino
  print "[INFO] Trying to run ntpdate..."
  os.system("ntpdate ntp.ubuntu.com")
  now = datetime.datetime.today()
  if now < test_date:
    print "[ERROR] ntpdate could not get correct date"
    exit()

##################################################
# Garbage collector
##################################################
long_ago_delta = datetime.timedelta(days=long_ago)
long_ago_date = now + long_ago_delta
folders = os.listdir(backup_path)
for item in folders:
  search_date = rega_date.match(item)
  if search_date > -1:
    folder_date = datetime.datetime.strptime(search_date.group(1), '%Y-%m-%d')
    if folder_date < long_ago_date:
      old_file = os.path.join(backup_path, item)
      os.unlink(old_file)
      print "[WARNING]: Removing", old_file

print "Done", time.time()-started, "elapsed"

