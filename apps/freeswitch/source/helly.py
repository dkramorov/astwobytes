# -*- coding: utf-8 -*-
import freeswitch

import MySQLdb
import os

dialplan_path = "/usr/local/freeswitch/conf/dialplan/pcheline"

login = "jocker";
passwd = "reabhxbr";
host = "127.0.0.1";
dbname = "freeswitch"
db = MySQLdb.connect(host=host, user=login, passwd=passwd, db=dbname)
cursor = db.cursor()
query = "select gw, dest from dialplan_transfer"
cursor.execute(query)
rowcount = cursor.rowcount

# Drop everything starts from transfer_from_
content = os.listdir(dialplan_path)
for item in content:
  current_item = os.path.join(dialplan_path, item)
  if os.path.isfile(current_item):
    if item.startswith("transfert_from_"):
      os.unlink(current_item)

for i in range(rowcount):
  row = cursor.fetchone()
  gw, dest = row[0], row[1]
  if gw and dest:

    # ---------------------------
    # Pass all, except 7395243...
    # ---------------------------
    if not gw.startswith("7395243"):
      continue

    gw = gw.strip()
    gw_len = len(gw)
    if gw_len < 6 or gw_len > 11:
      continue
    if gw_len == 7 and gw.startswith("2"):
      gw = gw[1:]

    result = ""

    dest = dest.strip()
    dest_len = len(dest)
    dest_array = dest.replace(",", " ").replace(".", " ").split(" ")
    for item in dest_array:
      try:
        item = int(item)
        item = str(item)
      except ValueError:
        continue
      item_len = len(item)
      if item_len < 11:
        continue

      if item.startswith("7"):
        item = "8%s" % item[1:]
      #result += "sofia/gateway/pcheline_gw/008153685%s:_:" % item
      result += "sofia/gateway/rostelecom_gw/%s:_:" % item

    if not result:
      continue
    result = result[:-3]

    gw_name = "transfer_from_%s.xml" % gw
    gw_path = os.path.join(dialplan_path, gw_name)
    f = open(gw_path, "wb+")

    transfer_line = """<extension name="pcheline_incoming_GW">
  <condition field="destination_number" expression="^(GW)$">
    <!--
    <condition field="${caller_id_number}" expression="^(demo1000|1000)$">
      <action application="set" data="effective_caller_id_number=3952782536"/>
      <action application="set" data="effective_caller_id_name=3952782536"/>
      <anti-action application="set" data="effective_caller_id_number=${caller_id_number}"/>
      <anti-action application="set" data="effective_caller_id_name=${caller_id_number}"/>
    </condition>
    -->
    <action application="set" data="ringback=${us-ring}"/>
    <action application="export" data="hold_music=$${hold_music}"/>
    <action application="set" data="ignore_early_media=true" />
    <action application="set" data="record_file_name=$${base_dir}/RTMP/${strftime(%Y-%m-%d)}/${destination_number}_${caller_id_number}_${uuid}.wav"/>
    <action application="set" data="media_bug_answer_req=true"/>
    <action application="export" data="execute_on_answer=record_session ${record_file_name}"/>
    <action application="bridge" data="RESULT"/>
  </condition>
</extension>"""
    transfer_line = transfer_line.replace("GW", gw)
    transfer_line = transfer_line.replace("RESULT", result)
    f.write(transfer_line)

    f.close()

#os.system("fs_cli -x \"reloadxml\"")

# CALL RUN
def handler(session, args):
  freeswitch.consoleLog("info", "helly")

# CONSOLE RUN fs_cli
def fsapi(session, stream, env, args):
  stream.write("helly")
