#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

mount_point = "/home/jocker/tmp"
command = "curlftpfs irkpic5:irkutsk223223@9soi.biz " + mount_point
try:
  os.system(command)
except:
  print "[ERROR]: could not moutn 9soi.biz"
  exit()
is_mount = os.path.ismount(mount_point)
if is_mount:
  new = os.path.join(mount_point, "new2")
  if not os.path.exists(new):
    os.mkdir(new)
  print os.listdir(mount_point)
  os.system("umount "+mount_point)
  is_mount = os.path.ismount(mount_point)
  #print is_mount


#<Limit ALL>
#Allow from 87.229.238.214
#Allow from 188.166.17.32
#Deny from all
#</Limit>
