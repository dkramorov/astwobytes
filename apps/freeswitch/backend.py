# -*- coding:utf-8 -*-
import json
import datetime
import logging

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
       USAGE:
       uri = "http://monitor:cnfylfhnysq@10.1.250.6:8080"
       fs = FreeswitchBackend(uri)"""

    def __init__(self, uri):
        self.uri = uri
        self.server = xmlrpc.client.ServerProxy(uri)

    def _parse_callcenter(self, apiresult):
        """Parse output of mod_callcenter's api output"""
        data = []
        lines = apiresult.splitlines()
        if lines:
          keys = lines[0].strip().split('|')
          for line in lines[1:]:
            fields = line.split('|')
            if len(fields) != len(keys):
              continue
            entry = {}
            for i in range(0, len(keys)):
              entry[keys[i]] = fields[i]
            data.append(entry)
        return data

    def _parse_xml(self, apiresult):
        data = []
        for row in XML(apiresult):
          data.append(dict([(e.tag, e.text) for e in row]))
          return data

    def _get_user_data(self, extension, data):
        presence_id = self.server.freeswitch.api('user_data', '%s@%s %s' % (extension, self.domain, data))
        if presence_id:
          return presence_id
        return None

    def get_agents(self):
        # Get list of all defined agents
        output = self.server.freeswitch.api('callcenter_config', 'agent list')
        agents = dict([(agent['name'], agent) for agent in self._parse_callcenter(output)])
        # Get tiers and update agent info
        output = self.server.freeswitch.api('callcenter_config', 'tier list')
        tiers = self._parse_callcenter(output)
        for tier in tiers:
          agent = agents.get(tier['agent'])
          if not agent:
            continue
          if not agent.get('queues'):
            agent['queues'] = []
          agent['queues'].append({'queue': tier['queue'], 'level': tier['level'], 'position': tier['position']})

        presence_table = {}
        # Get extension, real name and presence ID of logged in agents
        for agtid, agent in agents.iteritems():
          if agent['contact']:
            contact = agent['contact'].split('/')
            if contact[0].endswith('loopback'):
              agent['extension'] = contact[1]
              if contact[1] and contact[1][0] not in ('0', '9'):
                realname = self._get_user_data(contact[1], 'var effective_caller_id_name')
                if realname:
                  agent['realname'] = realname
                presence_id = self._get_user_data(contact[1], 'var presence_id')
                if presence_id:
                  agent['presence_id'] = presence_id
                  presence_table[presence_id] = agent

        # Get currently active channels
        output = self.server.freeswitch.api('show', 'channels as xml')
        channels = self._parse_xml(output) or []
        # Update presence state from active channels
        for channel in channels:
          if channel['presence_id'] in presence_table:
            presence_table[channel['presence_id']]['callstate'] = channel['callstate']
            presence_table[channel['presence_id']]['direction'] = 'caller' if channel['direction'] == 'inbound' else 'callee'
        return agents

    def get_queues(self):
        output = self.server.freeswitch.api('callcenter_config', 'queue list')
        queues = dict([(queue['name'], queue) for queue in self._parse_callcenter(output)])
        for queue in queues:
          output = self._parse_callcenter(self.server.freeswitch.api('callcenter_config', 'queue list members %s' % queue))
          output.sort(key=lambda m: m['system_epoch'])
          queues[queue]['members'] = output
          queues[queue]['waiting_count'] = len([x for x in output if x['state'] == 'Waiting'])
        return queues

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
