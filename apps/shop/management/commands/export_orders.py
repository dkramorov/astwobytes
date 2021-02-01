#-*- coding:utf-8 -*-
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.shop.exchange import create_orders_xml

logger = logging.getLogger('main')

class Command(BaseCommand):
    """Проверка формирования файла с заказами"""
    def add_arguments(self, parser):
        parser.add_argument('--dest',
            action = 'store',
            dest = 'dest',
            type = str,
            default = False,
            help = 'Set dest file (absolute path)')
    def handle(self, *args, **options):
        dest = 'orders.xml'
        if options.get('dest'):
            dest = options['dest']
        create_orders_xml(dest=dest)




