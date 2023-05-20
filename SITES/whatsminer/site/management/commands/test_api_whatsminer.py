# -*- coding:utf-8 -*-
import os
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count
from django.db import connections

from apps.main_functions.catcher import json_pretty_print
from apps.site.miners.whatsminer import WhatsMinerApi

logger = logging.getLogger('main')

class Command(BaseCommand):
    """
       vpn connect then
       sudo route add 10.10.11.0/24 10.10.6.1
       sudo route add 10.10.10.0/24 10.10.6.1
       sudo route add 10.10.5.0/24 10.10.6.1
    """
    def add_arguments(self, parser):
        parser.add_argument('--folder',
            action = 'store',
            dest = 'folder',
            type = str,
            default = False,
            help = 'Set folder with spinner files')
        parser.add_argument('--catalogue',
            action = 'store_true',
            dest = 'catalogue',
            default = False,
            help = 'Load catalogue')

    def handle(self, *args, **options):
        # отключено апи
        #api = WhatsMinerApi(ip='10.10.10.94', passwd='admin')
        #api.authorization()
        #print(api.manage_led())
        #print(api.exec('summary'))
        #print(api.exec('get_version'))
        #print(api.exec('get_miner_info'))

        # включено апи
        #print('----------')
        api = WhatsMinerApi(ip='10.10.5.195', passwd='admin')
        api.authorization()
        #print(api.reboot())
        print(api.manage_led())
        #print(api.exec('summary'))
        #print(api.exec('get_version'))
        #print(api.exec('get_miner_info'))
        #print(api.exec('get_psu'))
        #print(api.exec('devdetails'))
        #print(json_pretty_print(api.exec('edevs')))
        #print(api.exec('edevs'))
        #print(api.exec('devs'))
        #print(json_pretty_print(api.exec('pools')))

        #api.gen_credentials(time='0793', salt='BQ5hoXV9', new_salt='ZulutshE', passwd = 'admin')
        #api.authorization()
        #print(api.token, api.cipher)
        #print(api.manage_led())
        #print(api.download_logs())
        #print(api.change_passwd())
        #print(api.get_status())
