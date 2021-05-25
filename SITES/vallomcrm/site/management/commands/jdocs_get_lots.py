#-*- coding:utf-8 -*-
import datetime
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.date_time import date_plus_days
from apps.main_functions.catcher import json_pretty_print
from apps.site.main.api_jdocs import APIJDOCS

logger = logging.getLogger('main')


class Command(BaseCommand):
    """Проверка формирования файла с заказами"""
    def add_arguments(self, parser):
        parser.add_argument('--start_date',
            action = 'store',
            dest = 'start_date',
            type = str,
            default = False,
            help = 'Set start date')
        parser.add_argument('--end_date',
            action = 'store',
            dest = 'end_date',
            type = str,
            default = False,
            help = 'Set end date')
        parser.add_argument('--check_lot',
            action = 'store',
            dest = 'check_lot',
            type = str,
            default = False,
            help = 'Check lot')

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        seven_days_ago = date_plus_days(now, days=-7)
        start_date = seven_days_ago.strftime('%Y-%m-%d')
        end_date = now.strftime('%Y-%m-%d')
        if options.get('start_date'):
            date = str_to_date(options['start_date'])
            if date:
                start_date = date
        if options.get('end_date'):
            date = str_to_date(options['end_date'])
            if date:
                start_date = date

        api = APIJDOCS()
        #print(json_pretty_print(api.get_lots(start_date, end_date)))
        if options.get('check_lot'): # UP2618689 / m28195967844
            test_lot = api.load_exmple_from_old_format(options['check_lot'])
            api.prepare_data([test_lot])






