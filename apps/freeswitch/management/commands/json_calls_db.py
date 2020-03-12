# -*- coding: utf-8 -*-
import logging
import time
import datetime
import requests

from django.db.models import Count
from django.db import transaction
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.fortasks import search_process
from apps.freeswitch.models import CdrCsv

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    #def add_arguments(self, parser):
        # Named (optional) arguments
        #parser.add_argument('--multiple',
        #    action = 'store_true',
        #    dest = 'multiple',
        #    default = False,
        #    help = 'Send to multiple accounts')
        parser.add_argument('--days',
            action = 'store',
            dest = 'days',
            type = str,
            default = False,
            help = 'Set count days for recalc stata')
    def handle(self, *args, **options):
        """Создаем json файлы, чтобы не напрягать базень запросами
           при формировании статистики, пусть сервер статистики
           забирает нужные данные сам"""
        is_running = search_process(q = ('json_calls_db', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()

        days = 2
        if options.get('days'):
            try:
                days = int(options['days'])
            except ValueError:
                logger.error('You try set days param non int type')
                return
        now = datetime.datetime.now()
        long_ago = date_plus_days(now, days=-days)
        query = CdrCsv.objects.filter(created__gte=long_ago)
        total_records = query.aggregate(Count('id'))['id__count']
        logger.info('total_records %s, days: %s' % (total_records, days))





