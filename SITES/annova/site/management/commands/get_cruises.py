#-*- coding:utf-8 -*-
import re
import os
import time
import json
import logging
import requests

from lxml import html

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from apps.flatcontent.models import Containers, Blocks
from apps.main_functions.files import open_file, make_folder
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.date_time import str_to_date

logger = logging.getLogger(__name__)

"""Обновление круизов
   https://b2b.astoriagrande.com/cruises
"""

# CertificateError: hostname '...:443' doesn't match '...'
# You can avoid this error by monkey patching ssl:
import ssl
ssl.match_hostname = lambda cert, hostname: True

def get_cruises_page():
    """Получение странички https://b2b.astoriagrande.com/cruises"""
    r = requests.get('https://b2b.astoriagrande.com/cruises', verify=False)
    tree = html.fromstring(r.text)
    cruises = tree.xpath('//div[@id="dataRows"]')[0]
    return cruises

def parse_cruises(cruises):
    """Парсинг круизов
       :param cruises: элемент id=dataRows
    """
    result = []
    for child in cruises:
        class_name = child.attrib.get('class')
        if not class_name == 'accordion':
            continue

        inner, content = None, None
        for block in child:
            class_name = block.attrib.get('class')
            if class_name == 'accordion__inner':
                inner = block
            elif class_name == 'accordion__content':
                content = block
        if inner and content:
            date = inner.xpath('.//div[@class="cruise-list__row__dep-date"]')[0].text.strip()
            duration = inner.xpath('.//div[@class="cruise-list__row__duration"]')[0].text.strip()
            path = inner.xpath('.//div[@class="cruise-list__row__path"]')[0].text.strip()
            ship = inner.xpath('.//div[@class="cruise-list__row__ship"]')[0].text.strip()
            #price = inner.xpath('.//div[@class="cruise-list__row__best-price"]')[0].text.strip()
            #print(date, duration, path, ship)
            mapa = content.xpath('.//div[@class="cruise-list__row__map"]')[0]
            img = mapa.xpath('.//img')[0].attrib.get('src')
            table = content.xpath('.//div[@class="cruise-list__row__itinerary"]')[0]
            info = html.tostring(table.xpath('.//table')[0], encoding='unicode')
            result.append({
                'date': date,
                'duration': duration,
                'path': path,
                'ship': ship,
                'mapa': img,
                'info': info,
            })
    print(json_pretty_print(result))
    return result

def save_cruises(cruises):
    """Сохранение круизов во flatcontent
       :param cruises: массив со словарями
    """
    container = Containers.objects.filter(tag='cruises').first()
    if not container:
        container = Containers.objects.create(
            tag='cruises',
            name='Круизы',
            state=3,
        )
    for block in container.blocks_set.all():
        block.delete()
    for cruise in cruises:
        block = Blocks.objects.create(
            container=container,
            state=3,
            name=cruise['path'],
            created=str_to_date(cruise['date']),
            title=cruise['ship'],
            description=cruise['duration'],
            html=cruise['info'],
        )
        block.upload_img('%s%s' % ('https://b2b.astoriagrande.com', cruise['mapa']))

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--rebuild_catalogue',
            action = 'store_true',
            dest = 'rebuild_catalogue',
            default = False,
            help = 'Drop catalogue structure and recreate it')
        parser.add_argument('--cat_id',
            action = 'store',
            dest = 'cat_id',
            type = str,
            default = False,
            help = 'Set cat tag for update')
    def handle(self, *args, **options):

        started = time.time()
        cruises = get_cruises_page()
        result = parse_cruises(cruises)
        save_cruises(result)

        elapsed = time.time() - started
        print('%.2f' % elapsed)

