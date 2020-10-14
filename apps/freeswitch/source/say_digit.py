# -*- coding: utf-8 -*-
import freeswitch

# Обязательно нужно __init__.py иначе ошибка иморта будет
# https://github.com/signalwire/freeswitch/blob/master/src/mod/languages/mod_python/freeswitch.py

def log(msg, t='info'):
    freeswitch.consoleLog(t, msg)

def handler(session, args):
    log('Bridge user and switch from python\n')
    log('Arguments %s\n' % args)

# what => hangup or transfer
def hangup_hook(session, what, args=""):
    freeswitch.consoleLog('info', 'hangup hook for %s\n' % what)

# what => dtmf or event
# obj => dtmf object or event object
def input_callback(session, what, obj, args=''):
    if(what == 'dtmf'):
        freeswitch.consoleLog('info', what + ' ' + obj.digit + '\n')
    else:
        freeswitch.consoleLog('info', what + ' ' + obj.serialize() + '\n')
    return 'pause'

def fsapi(session, stream, env, args):
    """Вызывается, когда вызываем через консоль/скрипт"""
    log('--- script from console, args %s ---' % (args, ))
    stream.write('session=>%s\n' % session)

    phone = '83952959223'
    code = '12345'
    if args:
        if isinstance(args, str):
            args = args.split()
        if not len(args) == 2:
            log('[ERROR]: len args %s not equal 2 ---' % (args, ), t='error')
            return
        phone, code = args

    diversion_cid = '73952223223'
    diversion_phone = '73952546114'
    diversion_domain = 'irk.voice.dsi.ru'

    ignore_early_media = 'ignore_early_media=true'
    gw = 'sofia/gateway/dsi_gw/'
    effective_caller_id_number = 'effective_caller_id_number=%s' % diversion_cid
    effective_caller_id_name = 'effective_caller_id_name=%s' % diversion_cid
    origination_caller_id_name = 'origination_caller_id_name=%s' % diversion_cid
    origination_caller_id_number = 'origination_caller_id_number=%s' % diversion_cid
    sip_h_diversion = 'sip_h_Diversion=&quot;%s&quot; <sip: %s@%s>;reason=unconditional;' % (diversion_phone, diversion_phone, diversion_domain)

    bridge_vars = "{%s,%s,%s,%s,%s}" % (
        effective_caller_id_number,
        effective_caller_id_name,
        origination_caller_id_name,
        origination_caller_id_number,
        sip_h_diversion,
    )

    session = freeswitch.Session('%s%s%s' % (bridge_vars, gw, phone))
    session.answer()
    if session.ready():
        #<action application="say" data="ru number pronounced 12345"/>
        session.execute('wait_for_answer', '60')
        for i in range(5):
            session.say(code, 'ru', 'number', 'pronounced')
            session.execute('sleep', '1500')
        session.hangup()
    else:
        log('[ERROR]: session not ready', t='error')

    stream.write(env.serialize())

def runtime(args):
    print args + '\n'

def xml_fetch(params):
    xml = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<document type="freeswitch/xml">
  <section name="dialplan" description="RE Dial Plan For FreeSWITCH">
    <context name="rtmp">
      <extension name="generated">
        <condition>
          <action application="answer"/>
          <action application="playback" data="${hold_music}"/>
        </condition>
      </extension>
    </context>
  </section>
</document>"""
    return xml