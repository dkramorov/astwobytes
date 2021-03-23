#-*- coding:utf-8 -*-
import os
import logging
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.addresses.models import Address

from apps.site.dealers.models import Dealer

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
        Address.objects.all().delete()
        Dealer.objects.all().delete()

        path = '/home/jocker/Downloads/dealers.txt'
        cities = {choice[1]: choice[0] for choice in Dealer.city_choices}
        fields = {
            'Адрес:': 'address',
            'Время работы:': 'worktime',
            'Сайт:': 'site',
            'Телефон:': 'phone',
        }
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        cur_field = None
        obj = {}
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue

            # Обнуление
            if cur_field == 'phone' and not (line.startswith('+') or line.startswith('8 (')):
                cur_field = None
                Dealer.objects.create(**obj)
                obj = {}

            if line in cities:
                cur_city = cities[line]
            elif not cur_field:
                cur_field = 'name'
                obj['name'] = line
            elif line in fields:
                cur_field = fields[line]
                cur_value = ''
                obj[cur_field] = ''
            else:
                if cur_field == 'address':
                    obj[cur_field] = Address.objects.create(addressLines=line, place=obj['name'])
                else:
                    obj[cur_field] += line + '<br>'

            obj['city'] = cur_city
        Dealer.objects.create(**obj)




