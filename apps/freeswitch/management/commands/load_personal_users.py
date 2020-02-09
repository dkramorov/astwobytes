# -*- coding: utf-8 -*-
import logging
import time
import requests

from django.db import transaction
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.fortasks import search_process
from apps.freeswitch.models import PersonalUsers

logger = logging.getLogger(__name__)

CRM_HOST = 'https://223-223.ru'

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
        is_running = search_process(q = ('load_personal_users', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()
        r = requests.get('%s/media/personal_users.json' % (CRM_HOST, ), timeout=5)
        rows = r.json()
        logger.info('file received')
        bulk_save(rows)

@transaction.atomic
def bulk_save(rows):
    z = 0
    if rows:
        for row in rows:
            z += 1
            analog = PersonalUsers.objects.filter(userid=row[0]).first()
            if not analog:
                analog = PersonalUsers(userid=row[0])
            if not analog.username == row[1]:
                analog.username = row[1]
                analog.save()

            if z % 5000 == 0:
                logger.info('processed %s of %s' % (z, len(rows)))
                #break
