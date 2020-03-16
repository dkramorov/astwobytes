# -*- coding: utf-8 -*-
import logging
import json
import time
import datetime
import requests

from django.db.models import Count
from django.db import transaction
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.fortasks import search_process
from apps.main_functions.date_time import date_plus_days
from apps.main_functions.files import open_file, check_path
from apps.freeswitch.models import CdrCsv

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
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
        by = 500
        result = []
        fields = ('dest',
                  'cid',
                  'uuid',
                  'ip', # 192.168.1
                  'account',
                  'state',
                  'created',
                  'client_id',
                  'duration', )
        now = datetime.datetime.now()
        long_ago = date_plus_days(now, days=-days)
        query = CdrCsv.objects.filter(created__gte=long_ago)
        total_records = query.aggregate(Count('id'))['id__count']
        logger.info('total_records %s, days: %s' % (total_records, days))
        total_pages = int(total_records / by) + 1
        # Просто все запишем в файл
        for i in range(total_pages):
            rows = query[i*by:i*by+by]
            for row in rows:
                record = {}
                for field in fields:
                    record[field] = getattr(row, field)
                    if field == 'created':
                        record[field] = record[field].strftime('%Y-%m-%d %H:%M:%S')
                record['record'] = row.get_record_path()
                if check_path(record['record'].replace('/media/', '')):
                    record['record'] = ''
                    #if record['duration']:
                    #    logger.info('record not found %s, %s' % (record['uuid'], record['ip']))
                result.append(record)
        with open_file('json_calls_db.txt', 'w+') as f:
            f.write(json.dumps(result))


