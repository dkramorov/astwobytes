#-*- coding:utf-8 -*-
import json
import logging
import datetime
import requests

from lxml import html

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.files import open_file
from apps.main_functions.date_time import date_plus_days, str_to_date

logger = logging.getLogger(__name__)

"""
s = requests.Session()
urla = 'https://jsmnew.doko.link/'

params = {
    'login': 'vallom',
    'parola': 'vallom',
    'captcha': captcha,
    'Login': 'Вход',
}
"""

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
        parser.add_argument('--sessid',
            action = 'store',
            dest = 'sessid',
            type = str,
            default = False,
            help = 'Set sessid for session')

    def handle(self, *args, **options):

        s = requests.Session()
        today = datetime.date.today()
        end_date = date_plus_days(today, days=1)
        start_date = date_plus_days(end_date, days=-1)
        sessid = 'vg8gii226edl4iv7nfm5fsfd25'

        # ------------------
        # Задать дату начала парсинга
        # ------------------
        if options.get('start'):
            date = str_to_date(options['start'])
            if date:
                start_date = date

        # ---------------------
        # Задать дату окончания парсинга
        # ---------------------
        if options.get('end'):
            date = str_to_date(options['end'])
            if date:
                end_date = date

        # -------------
        # Задать сессию
        # -------------
        if options.get('sessid'):
            sessid = options['sessid']

        s.cookies.update({'PHPSESSID': sessid})

        urla = 'https://jsmnew.doko.link/jp_jsm_balance.php'

        urla = 'https://jsmnew.doko.link/jp_victoria_balance_ajax.php'
        params = {
            'client': 181,
            'an': end_date.year,
            'luna': 'все',
            'dinterv': 1,
            'datas': start_date.strftime('%d.%m.%Y'),
            'datae': end_date.strftime('%d.%m.%Y'),
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'PHPSESSID=%s' % sessid,
            'Host': 'jsmnew.doko.link',
            'Pragma': 'no-cache',
            'Referer': 'https://jsmnew.doko.link/menu.php',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:81.0) Gecko/20100101 Firefox/81.0',
        }
        r = s.get(urla, params=params, headers=headers)
        tree = html.fromstring(r.text)
        spans = tree.xpath('//span')

        for i, span in enumerate(spans):
            if span.text and 'ОБЩИЙ БАЛАНС' in span.text:
                print(spans[i+1].text)
                break



