#-*- coding:utf-8 -*-
import json
import logging
import datetime
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--start',
            action = 'store',
            dest = 'start',
            type = str,
            default = False,
            help = 'Set start date')
        parser.add_argument('--end',
            action = 'store',
            dest = 'end',
            type = str,
            default = False,
            help = 'Set end date')

    def handle(self, *args, **options):
        """Парсер авито
           Информацию по айди рубрик и регионов можно найти
           на https://rest-app.net/api#ads
           но все это приходит внутри json итак
        """
        host = 'https://www.avito.ru'
        endpoint = '/web/1/main/items'
        params = {
            'forceLocation': True, # забить на геолокацию автоматом
            'locationId': 629210,
            'categoryId': '21', # 21 бытовая техника, 0 - все категории
            #'lastStamp': 1589612412, # непонятно нахер нужен
        }
        s = requests.Session()
        r = s.get('%s%s' % (host, endpoint), params=params)
        resp = r.json()
        print(resp['context'], len(resp['items']), resp['items'][0]['id'])
        #print(json_pretty_print(resp['items'][0]))


        r = s.get('%s%s' % (host, endpoint), params=params)
        resp = r.json()
        print(resp['context'], len(resp['items']), resp['items'][0]['id'])
        #print(json_pretty_print(resp['items'][0]))


