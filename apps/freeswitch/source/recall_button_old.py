# -*- coding: utf-8 -*-
# Обязательно нужно __init__.py иначе ошибка иморта будет
import freeswitch
import MySQLdb
import re

rega_phone = re.compile("[^0-9]")

login = "jocker";
passwd = "reabhxbr";
host = "127.0.0.1";
dbname = "freeswitch"
db = MySQLdb.connect(host=host, user=login, passwd=passwd, db=dbname)

def log(msg, t="info"):
  freeswitch.consoleLog(t, msg)

def handler(session, args):
  log("Bridge user and company from python\n")
  log("Arguments %s\n" % args)

# what => hangup or transfer
def hangup_hook(session, what, args=""):
  freeswitch.consoleLog("info", "hangup hook for '%s'\n" % what)

# what => dtmf or event
# obj => dtmf object or event object
def input_callback(session, what, obj, args=""):
  if(what == "dtmf"):
    freeswitch.consoleLog("info", what + " " + obj.digit + "\n")
  else:
    freeswitch.consoleLog("info", what + " " + obj.serialize() + "\n")
  return "pause"

def fsapi(session, stream, env, args):
  stream.write("session=>%s\n" % session)
  if args:
    stream.write("fsapi called with theese arguments: %s\n" % args)
  else:
    # ---------
    # Константы
    # ---------
    ignore_early_media = "ignore_early_media=true"
    originator = "origination_caller_id_name=3952782536,origination_caller_id_number=3952782536"
    bridge_vars = "{%s,%s}" % (ignore_early_media, originator)
    gw = "sofia/gateway/pcheline_gw/"
    #phone1 = "83952959223"
    #phone2 = "89642233223"
    # ----------------------------------
    # Сценарий без сессии,
    # тащим с базы задачки по коммутации
    # ----------------------------------
    cursor = db.cursor()
    query = """select from_phone, to_phone, id from recall_recall where state is NULL limit 1"""
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.execute(query)

    for row in rows:
      cursor = db.cursor()
      query = "update recall_recall set state=99 where id=%s" % (row[2], )
      cursor.execute(query)
      cursor.execute("commit")
      cursor.close()

      phone1 = rega_phone.sub("", row[0])
      phone2 = rega_phone.sub("", row[1])
      new_state = 1
      asession = freeswitch.Session("%s%s%s" % (bridge_vars, gw, phone1))
      if asession.ready():
        bsession = freeswitch.Session("%s%s%s" % (bridge_vars, gw, phone2))
        if bsession.ready():
          freeswitch.bridge(asession, bsession)
        else:
          new_state = 3
      else:
        new_state = 2

      cursor = db.cursor()
      query = "update recall_recall set state=%s where id=%s" % (new_state, row[2])
      cursor.execute(query)
      cursor.execute("commit")
    cursor.close()
  stream.write(env.serialize())

def runtime(args):
  print args + "\n"

def xml_fetch(params):
  xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?> <document type="freeswitch/xml"> <section name="dialplan" description="RE Dial Plan For FreeSWITCH"> <context name="rtmp"> <extension name="generated"> <condition> <action application="answer"/> <action application="playback" data="${hold_music}"/> </condition> </extension> </context> </section> </document>"""
  return xml