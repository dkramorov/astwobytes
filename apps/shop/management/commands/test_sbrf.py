#-*- coding:utf-8 -*-
import time
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.shop.sbrf import SberPaymentProovider

logger = logging.getLogger('main')

"""
https://securepayments.sberbank.ru/wiki/doku.php/integration:api:start
https://securepayments.sberbank.ru/wiki/doku.php/integration:simple
https://securepayments.sberbank.ru/wiki/doku.php/mportal3:auth

    Тестовый личный кабинет - https://3dsec.sberbank.ru/mportal3
    Боевой личный кабинет - https://securepayments.sberbank.ru/mportal3
"""

class Command(BaseCommand):
    """Проверка формирования файла с заказами"""
    def add_arguments(self, parser):
        parser.add_argument('--fake',
            action = 'store',
            dest = 'fake',
            type = str,
            default = False,
            help = 'Set fake string')
    def handle(self, *args, **options):

        params = {
            'amount': 100,
            'orderNumber': 'test_%s' % str(time.time()),
            'returnUrl': 'http://localhost:8000/payment/sbrf/success/',
            'failUrl': 'http://localhost:8000/payment/sbrf/fail/',
            'description': 'Тестовый заказ',
            'clientId': 'tester1',
            'email': 'tester@masterme.ru',
            'phone': '73952959223',
        }

        sber = SberPaymentProovider()
        register_order = sber.register_do(**params)
        print(json_pretty_print(register_order))
        print(register_order['errorCode'], type(register_order['errorCode']))



