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
    #gw = "sofia/gateway/pcheline_gw/"
    gw = "sofia/default/test"

    phone1 = "83952959223"
    phone2 = "89642233223"
    #originator = "origination_caller_id_name=%s,origination_caller_id_number=%s" % (
      #phone2[1:], phone2[1:]
    #)
    #bridge_vars = "{%s,%s}" % (ignore_early_media, originator)
    bridge_vars = "{%s}" % (ignore_early_media, )

    #asession = freeswitch.Session("%s%s%s" % (bridge_vars, gw, phone1))
    session = freeswitch.Session(gw)

    #if asession.ready():
      #asession.transfer("recall_button_%s_%s" % (phone1, phone2), "XML", "pcheline_context")
      #asession.execute("execute_extension", 
        #"recall_button_%s_%s XML pcheline_context" % (phone1, phone2))

      #asession.execute("playback", "/usr/local/freeswitch/sounds/recall.wav")

      #bsession = freeswitch.Session("%s%s%s" % (bridge_vars, gw, phone2))
      #if bsession.ready():
        #freeswitch.bridge(asession, bsession)

  stream.write(env.serialize())

def runtime(args):
  print args + "\n"

def xml_fetch(params):
  xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?> <document type="freeswitch/xml"> <section name="dialplan" description="RE Dial Plan For FreeSWITCH"> <context name="rtmp"> <extension name="generated"> <condition> <action application="answer"/> <action application="playback" data="${hold_music}"/> </condition> </extension> </context> </section> </document>"""
  return xml