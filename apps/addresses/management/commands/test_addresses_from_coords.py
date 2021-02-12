#-*- coding:utf-8 -*-
import os
import logging
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.addresses.utils import ask_yandex_address_by_point, parse_yandex_address, ask_yandex_address_by_str
from apps.addresses.models import Address

logger = logging.getLogger('main')


class Command(BaseCommand):
    """Проверка функций работы с хранилищем"""
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--fake',
            action = 'store_true',
            dest = 'fake',
            default = False,
            help = 'Fake')
        parser.add_argument('--fake1',
            action = 'store',
            dest = 'fake1',
            type = str,
            default = False,
            help = 'Fake1')

    def handle(self, *args, **options):
        addresses = Address.objects.all()
        for address in addresses:
            #if not address.latitude or not address.longitude:
                resp = ask_yandex_address_by_str(address.addressLines)
                print(json_pretty_print(resp))
                adr = parse_yandex_address(resp)
                print(json_pretty_print(adr))
                if not adr:
                    continue
                kwargs = {k: v for k, v in adr.items() if not k in ('addressLines', )}
                Address.objects.filter(pk=address.id).update(**kwargs)



