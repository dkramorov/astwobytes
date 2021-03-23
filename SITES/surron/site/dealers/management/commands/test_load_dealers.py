#-*- coding:utf-8 -*-
import os
import json
import logging
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.addresses.utils import ask_yandex_address_by_coords, parse_yandex_address
from apps.addresses.models import Address

from apps.site.dealers.models import Dealer

logger = logging.getLogger('main')

DEALERS_FILE = '/home/jocker/Downloads/dealers.json'
# https://api.sur-ron.com/web/store/en/list?country=China&page=1&size=200
COUNTRIES = (
    'China',
    'United States',
    'Germany',
    'United Kingdom',
    'Sweden',
    'Norway',
    'Czech',
    'Ukraine',
    'Chile',
    'Australia',
    'Mongolia',
    'Poland',
    'Singapore',
    'United Arab Emirates',
    'Bulgaria',
    'Russia',
    'Denmark',
    'Iceland',
    'Netherlands',
    'Belarus',
    'Kazakhstan',
    'Romania',
    'Dominican',
    'Indonesia',
    'France',
    'Japan',
    'Malaysia'
    'Philippines',
    'Belgium',
    'Georgia',
    'Morocco',
)

def load_dealers(country):
    """Загрузка дилеров
       :param country: страна
    """
    result = []
    domain = 'https://api.sur-ron.com/web/store/en/list'
    params = {
        'country': country,
        'page': 1,
        'size': 200,
    }
    r = requests.get(domain, params=params)
    resp = r.json()
    items = resp.get('data', {}).get('list', [])
    while items:
        print(json_pretty_print(params))
        params['page'] += 1
        result += [{
            'phone': item['contactPhone'],
            'place': item.get('storeName') or item.get('contactName'),
            'addressLines': item['address'],
            'latitude': item['latitude'],
            'longitude': item['longitude'],
        } for item in items]
        r = requests.get(domain, params=params)
        resp = r.json()
        items = resp.get('data', {}).get('list', [])
    return result

def load_dealers2file():
    """Записать дилеров в файл"""
    addresses = []
    for country in COUNTRIES:
        addresses += load_dealers(country)
    with open(DEALERS_FILE, 'w+', encoding='utf-8') as f:
        f.write(json.dumps(addresses))

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

        #load_dealers2file()

        with open(DEALERS_FILE, 'r', encoding='utf-8') as f:
            addresses = json.loads(f.read())
        for adr in addresses:

            adr_info = ask_yandex_address_by_coords(adr['latitude'], adr['longitude'])
            details = parse_yandex_address(adr_info)
            print(json_pretty_print(details))
            adr.update({
                'country': details.get('country'),
                'city': details.get('city'),
                'state': details.get('state'),
                'county': details.get('county'),
                'street': details.get('street'),
                'subdistrict': details.get('subdistrict'),
                'houseNumber': details.get('houseNumber'),
                'postalCode': details.get('postalCode'),
            })

            address = Address.objects.create(**{
                k: v for k, v in adr.items() if not k in ('phone', )
            })

            dealer = Dealer.objects.create(**{
                'name': adr['addressLines'],
                'phone': adr['phone'],
                'address': address,
            })


