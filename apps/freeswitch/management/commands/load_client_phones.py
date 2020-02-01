# -*- coding: utf-8 -*-
import logging
import time
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.fortasks import search_process
from apps.freeswitch.models import PhonesWhiteList

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
        """Загрузка белого списка телефонов в базу (для динамического диалплана)"""
        is_running = search_process(q = ('load_client_phones', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()
        r = requests.get('https://223-223.ru/media/phone_numbers.json')
        rows = r.json()
        if rows:
            for row in rows:
                analog = PhonesWhiteList.objects.filter(phone=row[0]).first()
                if not analog:
                    analog = PhonesWhiteList(phone=row[0])
                analog.tag = row[1]
                analog.desc = 'Получено из базы 223-223.ru'
                analog.name = row[2]
                analog.save()
