#-*- coding:utf-8 -*-
import time
import logging

from django.core.management.base import BaseCommand

from apps.products.models import Products

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
        parser.add_argument('--test',
            action = 'store_true',
            dest = 'test',
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
        polis_report()


