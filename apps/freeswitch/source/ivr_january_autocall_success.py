# -*- coding: utf-8 -*-
import freeswitch

import MySQLdb
import os

login = "jocker";
passwd = "reabhxbr";
host = "127.0.0.1";
dbname = "freeswitch"
db = MySQLdb.connect(host=host, user=login, passwd=passwd, db=dbname)
cursor = db.cursor()
#query = "select gw, dest from dialplan_transfer"
#cursor.execute(query)
#rowcount = cursor.rowcount

# CALL RUN
def handler(session, args):
  session.answer()
  session.execute("playback", "$${base_dir}/sounds/IVR/ivr_january_autocall_success.wav")
  freeswitch.consoleLog("info", "ivr_january_autocall_success")

# CONSOLE RUN fs_cli
def fsapi(session, stream, env, args):
  stream.write("ivr_january_autocall")

