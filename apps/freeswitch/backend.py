# -*- coding:utf-8 -*-
import json
import datetime
import logging
import MySQLdb

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

import xmlrpc.client
# ------------
# Документация
# ------------
# https://github.com/gonicus/fsqueuemon

class FreeswitchBackend(object):
    """Работа со свичом через xmlrpc
       https://freeswitch.org/confluence/display/FREESWITCH/FreeSWITCH+XML-RPC
       https://freeswitch.org/confluence/display/FREESWITCH/mod_python

       Скрипт питона можно вызвать прямо с консоли
       freeswitch> python foo.bar
       либо через диалплан
       <action application="python" data="foo.bar"/>

       USAGE:
       uri = "http://monitor:cnfylfhnysq@10.1.250.6:8080"
       fs = FreeswitchBackend(uri)
    """

    def __init__(self, uri):
        self.uri = uri
        self.server = xmlrpc.client.ServerProxy(uri)

    def call_script(self, script: str, args: list):
        """Вызов скрипта с аргументами
           :param script: вызываемый python script
           :param args: аргументы для скрипта
        """
        cmd = '%s %s' % (script, ' '.join(args))
        self.server.freeswitch.api('python', cmd)

    def agent_set_status(self, agent: str, status: int):
        """Задать статус агенту в коллцентре"""
        statuses = {
            1:"'Logged Out'",
            2:"'Available'",
            3:"'Available (On Demand)'",
            4:"'On Break'",
        }
        if not status in statuses:
            logger.info('[BAD STATUS]: %s, choose one of %s' % (status, statuses))
            return
        cmd = 'agent set status %s %s' % (agent, statuses[status])
        return self.server.freeswitch.api('callcenter_config', cmd)

    def agent_set_state(self, agent: str, state: int):
        """Задать состояние агенту в коллцентре"""
        states = {
            1:"'Idle'",
            2:"'Waiting'",
            3:"'Receiving'",
            4:"'In a queue call'",
        }
        if not state in states:
            logger.info('[BAD STATE]: %s, choose one of %s' % (status, states))
            return
        cmd = 'agent set state %s %s' % (agent, states[state])
        return self.server.freeswitch.api('callcenter_config', cmd)

    def get_agent_list(self):
        """Вернуть всех агентов колцентра
           "response": [{
               "busy_delay_time": "0",
               "calls_answered": "0",
               "contact": "[leg_timeout=5, rtp_secure_media=true]sofia/local/jocker%${domain_name}",
               "external_calls_count": "0",
               "instance_id": "single_box",
               "last_bridge_end": "1579842354",
               "last_bridge_start": "1579842237",
               "last_offered_call": "1579842233",
               "last_status_change": "1579848446",
               "max_no_answer": "3",
               "name": "jocker",
               "no_answer_count": "0",
               "no_answer_delay_time": "0",
               "ready_time": "1579837621",
               "reject_delay_time": "0",
               "state": "Idle",
               "status": "Logged Out",
               "talk_time": "0",
               "type": "callback",
               "uuid": "",
               "wrap_up_time": "5"
           }, ...]
        """
        agent_list = self.json_api({
            'command': 'callcenter_config',
            'format': 'pretty',
            'data': {
                'arguments': 'agent list'
            }
        })
        return {agent['name']: agent for agent in agent_list['response']}

    def get_tier_list(self):
        """Вернуть всех tiers (ярусы) колцентра
           "response": [{
               "agent": "jocker",
               "level": "1",
               "position": "1",
               "queue": "cifrus",
               "state": "Ready"
           }, ...]
        """
        tier_list = self.json_api({
            'command': 'callcenter_config',
            'format': 'pretty',
            'data': {
                'arguments': 'tier list'
            }
        })
        return {tier['agent']: tier for tier in tier_list['response']}

    def get_queues(self):
        """Получить список очередей колцентра"""
        queue_list = self.json_api({
            'command': 'callcenter_config',
            'format': 'pretty',
            'data': {
                'arguments': 'queue list'
            }
        })
        return {queue['name']: queue for queue in queue_list['response']}

    def json_api(self, json_obj):
        """Апи json для freeswitch
           https://freeswitch.org/confluence/display/FREESWITCH/mod_callcenter
           :param json_obj: объект json, например,
           {
               "command": "callcenter_config",
               "format": "pretty",
               "data": {"arguments":"agent list"}
           }
        """
        result = self.server.freeswitch.api('json', json.dumps(json_obj))
        return json.loads(result)

    def do_json_request(self, cmd: str, show: str = 'show'):
        """Выполнить JSON запрос к свичу, предположительно по команде show
           :param cmd: команда для выполнения
           :param show: команда вместо show
           USAGE:
           do_request('registrations as json') = show registration as json
           do_request('tier list', 'callcenter_config') = callcenter_config tier list
        """
        result = []
        output = self.server.freeswitch.api(show, cmd)
        try:
            result = json.loads(output).get("rows", [])
        except Exception as e:
            logger.error(e)
        return result

    def kill_channel(self, uuid):
        """Убить канал"""
        return self.server.freeswitch.api('uuid_kill', uuid)

    def reloadxml(self):
        """Перезагрузить конфигрурацию диалплана"""
        return self.server.freeswitch.api('reloadxml', '')

    def cdr_csv_rotate(self):
        """Перезагрузить логи по звонкам"""
        return self.server.freeswitch.api('cdr_csv', 'rotate')

    def get_registrations(self):
        """Получить регистрации на свиче"""
        result = {}
        output = self.do_json_request('registrations as json')
        for reg in output:
            result[reg['reg_user']] = reg['network_ip']
        return result

    def get_channels(self):
        """Получить каналы"""
        return self.do_json_request('channels as json')

    def get_bridged_calls(self):
        """Получить активные звонки (бриджи)"""
        return self.do_json_request('bridged_calls as json')

class RemoteDB:
    """Класс для подключения к удаленной БД"""
    conn = None

    def connect(self):
        login = 'jocker'
        passwd = 'reabhxbr'
        host = '10.10.10.1'
        dbname = 'a223'
        self.conn = MySQLdb.connect(host=host, user=login, passwd=passwd, db=dbname)
        self.conn.set_character_set('utf8')

    def query(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
        except (AttributeError, MySQLdb.OperationalError):
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute('SET NAMES utf8;')
            cursor.execute('SET CHARACTER SET utf8;')
            cursor.execute('SET character_set_connection=utf8;')
            cursor.execute(sql)
        return cursor

    def get_company_by_phone(self, phone: str):
        """Определяем нахер че за фирма по номеру телефона,
           делая запрос в рабочую базу по компаниям (удаленно)
           :param phone: телефон по которому ищем фирму"""
        try:
            dest = str(int(phone))
        except ValueError:
            logger.error('wrong phone number %s' % (phone, ))
            return
        # -----------------------------
        # Номер содержит 6/10/11 знаков
        # -----------------------------
        dest_len = len(dest)
        if dest_len == 6:
            dest = "83952%s" % dest
        elif dest_len == 10:
            dest = "8%s" % dest
        else:
            if "oper_" in dest:
                dest = dest.replace("oper_", "")

        if not len(dest) == 11:
            logger.error('phone len is not 11 digit line %s' % (dest, ))
            return
        cond = "("
        cond += " digits=%s OR" % dest # весь номер
        cond += " digits=%s OR" % dest[1:] # без 8
        cond += " digits=%s OR" % dest[4:] # без 8914
        cond += " digits=%s   " % dest[5:] # без 83952
        cond += ") "
        query = "select client_id, client_orgs.name, client_phones.digits, client_phones.prefix from client_phones inner join client_orgs on client_orgs.id=client_phones.client_id where %s" % (cond, )
        cursor = self.query(query)
        if cursor.rowcount >= 1:
            rows = cursor.fetchall()
            for row in rows:
                result_phone_number = ''
                if row[2]:
                    result_phone_number += '%s' % row[3]
                if row[3]:
                    result_phone_number += '%s' % row[2]
                if dest.endswith(result_phone_number):
                    return {'id': row[0], 'name': row[1]}

if __name__ == '__main__':
    FREESWITCH_URI='http://monitor:cnfylfhnysq@192.168.1.3:8080'
    logger.info(FREESWITCH_URI)
    fs = FreeswitchBackend(FREESWITCH_URI)
    bridged_calls = fs.get_bridged_calls()
    logger.info('[BRIDGED CALLS]: %s' % bridged_calls)
    channels = fs.get_channels()
    logger.info('[CHANNELS]: %s' % channels)
    registrations = fs.get_registrations()
    logger.info('[REGISTRATIONS]: %s' % registrations)
    fs.reloadxml()
