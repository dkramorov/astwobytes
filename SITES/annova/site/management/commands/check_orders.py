#-*- coding:utf-8 -*-
import time
import datetime
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage

from apps.products.models import Products
from apps.main_functions.files import open_file

from apps.site.polis.report import polis_report
from apps.site.main.order_forms import get_markup_product

logger = logging.getLogger(__name__)

"""Проверка оплат
"""

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--without_report',
            action = 'store_true',
            dest = 'without_report',
            default = False,
            help = 'test')
        parser.add_argument('--test2',
            action = 'store',
            dest = 'test2',
            type = str,
            default = False,
            help = 'test2')

    def handle(self, *args, **options):
        started = time.time()
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=4)
        from_date = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
        #from_date = datetime.datetime(2022, 1, 1)
        to_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        #to_date = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)

        polis_report(from_date, to_date, payed_status='not_payed')


