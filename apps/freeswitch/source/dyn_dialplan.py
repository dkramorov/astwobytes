# -*- coding: utf-8 -*-
# Обязательно нужно __init__.py иначе ошибка иморта будет
# Скрипт должен лежать в папке scripts папки свича
# Делает звонок с подменой номера
import freeswitch
import requests

host = 'https://callcenter.1sprav.ru'

def log(msg, t="info"):
    freeswitch.consoleLog(t, msg)

def handler(session, args):
    log('call from Python, Arguments %s\n' % args)

    session.execute('set', 'call_timeout=60')
    session.execute('set', 'continue_on_fail=true')

    user_id = session.getVariable('sip_user_agent') # example: 134@223-223.ru
    if not user_id:
        user_id = ''

    # --------------------------
    # Phone number who make call
    # --------------------------
    caller_id = session.getVariable('caller_id_number')
    # --------------
    # Call direction
    # --------------
    dest_number = session.getVariable('destination_number')
    log("%s=>%s" % (caller_id, dest_number))

    if len(dest_number) == 11:
        try:
            dest_number = str(int(dest_number))
        except ValueError:
            dest_number = None
            log('phone number %s is incorrect' % dest_number)
    else:
        dest_number = None

    # Проверка направления, куда можно этому user_agent
    endpoint = '/freeswitch/is_phone_in_white_list/'
    params = {
        'phone': dest_number,
        'user_id': user_id.split('@')[0],
    }
    r = requests.get('%s%s' % (host, endpoint), params=params)
    resp = r.json()
    isError = 'success' not in resp
    #log('______________%s, %s, %s' % (resp, params, r.request.url))
    if isError:
        session.answer()
        session.execute('sleep', '1500')
        session.execute('playback', '/usr/local/freeswitch/sounds/ups.wav')
    else:
        if 'cid' in resp:
            session.execute('set', 'sip_h_X-PersonalUserCID={}'.format(resp['cid']))
        else:
            session.execute('set', 'sip_h_X-PersonalUserCID=Err')
        session.execute('bridge', 'sofia/gateway/niagara_gw/%s' % (dest_number, ))

# what => hangup or transfer
def hangup_hook(session, what, args=""):
    freeswitch.consoleLog('info', 'hangup hook for "%s"\n' % what)

# what => dtmf or event
# obj => dtmf object or event object
def input_callback(session, what, obj, args=''):
    if(what == 'dtmf'):
        freeswitch.consoleLog('info', what + ' ' + obj.digit + '\n')
    else:
        freeswitch.consoleLog('info', what + ' ' + obj.serialize() + '\n')
    return 'pause'

def fsapi(session, stream, env, args):
    if args:
        stream.write('fsapi called with theese arguments: %s\n' % args)
    else:
        stream.write('fsapi called with no arguments \n')
    stream.write(env.serialize())

def runtime(args):
    print args + "\n"

def xml_fetch(params):
    xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?> <document type="freeswitch/xml"> <section name="dialplan" description="RE Dial Plan For FreeSWITCH"> <context name="rtmp"> <extension name="generated"> <condition> <action application="answer"/> <action application="playback" data="${hold_music}"/> </condition> </extension> </context> </section> </document>"""
    return xml