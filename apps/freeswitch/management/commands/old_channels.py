# -*- coding: utf-8 -*-
import logging
import time
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.fortasks import search_process
from apps.freeswitch.backend import FreeswitchBackend

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    #def add_arguments(self, parser):
        # Named (optional) arguments
        #parser.add_argument('--multiple',
        #    action = 'store_true',
        #    dest = 'multiple',
        #    default = False,
        #    help = 'Send to multiple accounts')
        #parser.add_argument('--single',
        #    action = 'store_true',
        #    dest = 'single',
        #    default = False,
        #    help = 'Send to single account')
    def handle(self, *args, **options):
        """Загрузка cdr_csv информации о звонках в базу"""
        is_running = search_process(q = ('old_channels', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()

        fs = FreeswitchBackend(settings.FREESWITCH_URI)
        regs = fs.get_registrations()
        print(regs)
        agents = fs.get_agent_list()
        for agent_name, agent in agents.items():
            print(agent_name, agent['state'], agent['status'])
            if not agent_name in regs:
                if not agent['state'] == 'Idle':
                    fs.agent_set_state(agent_name, 1)

        #print(fs.agent_set_status('jocker', 1))
        #print(fs.agent_set_state('jocker', 2))
        #print(json_pretty_print(fs.get_queues()))
        return
        #print(json_pretty_print(fs.get_tier_list()))
        #print(json_pretty_print(fs.get_agent_list()))
        #return

        #fs.server.freeswitch.api("callcenter_config", "agent set status %s %s" % (key, state_vars[1]))


        channels = fs.get_channels()
        for channel in channels:
            if '%' in channel.get('callee_num'):
                login, domain = channel['callee_num'].split('%')
                if not login in regs:
                    fs.kill_channel(channel.get('uuid'))
