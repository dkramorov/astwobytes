# -*- coding: utf-8 -*-
import logging
import time

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.fortasks import search_process
from apps.freeswitch.services import analyze_logs

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
        is_running = search_process(q = ('load_cdr_csv', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()
        analyze_logs()

        # ----------------------------
        # Определяем нахер че за фирма
        # ----------------------------
        #company = db.get_company_by_phone(new_cdr.dest)
        #if company:
            #new_cdr.client_id = company['id']
            #new_cdr.client_name = company['name']
