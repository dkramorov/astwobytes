#-*- coding:utf-8 -*-
import time
import datetime
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage

from apps.products.models import Products
from apps.main_functions.files import open_file
from apps.main_functions.date_time import str_to_date

from apps.site.polis.models import Polis
from apps.site.polis.report import polis_report
from apps.site.main.order_forms import get_markup_product

logger = logging.getLogger(__name__)

"""Формирование отчета по заказам
"""

def check_markup():
    prices = list(Products.objects.all().values_list('price', flat=True))
    for price in prices:
        if not price:
            continue
        markup = get_markup_product(price)
        price_with_markup = float(price) + markup.price
        diff = price_with_markup * 2.3 / 100
        print(price, markup.price, diff, price_with_markup - diff)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--flush',
            action = 'store_true',
            dest = 'flush',
            default = False,
            help = 'Reset state=2 for polises')
        parser.add_argument('--start_date',
            action = 'store',
            dest = 'start_date',
            type = str,
            default = False,
            help = 'Start date for report')

    def handle(self, *args, **options):
        started = time.time()
        emails = ('ap@223-223.ru', 'dk@223-223.ru')
        #emails = ('dk@223-223.ru', )
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=4)
        from_date = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
        if options.get('start_date'):
            start_date = str_to_date(options['start_date'])
            if start_date:
                from_date = start_date
        to_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        #to_date = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
        if options.get('flush'):
            Polis.objects.all().update(state=1)

        fname = polis_report(from_date, to_date, payed_status='payed')
        title = 'Отчет %s - %s' % (from_date.strftime('%d-%m-%Y'), to_date.strftime('%d-%m-%Y'))
        body = '<h6>%s</h6>' % title
        mail = EmailMessage(title, body, settings.EMAIL_HOST_USER, emails)
        mail.content_subtype = 'html'

        with open_file(fname, 'rb') as f:
            mail.attach(fname, f.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        mail.send()

