#-*- coding:utf-8 -*-
import json
import logging
import datetime
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.files import open_file
from apps.main_functions.date_time import date_plus_days, str_to_date

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
        today = datetime.date.today()
        end_date = date_plus_days(today, days=1)
        start_date = date_plus_days(end_date, days=-360)

        # ---------------------------
        # Задать дату начала парсинга
        # ---------------------------
        if options.get('start'):
            date = str_to_date(options['start'])
            if date:
                start_date = date

        # ------------------------------
        # Задать дату окончания парсинга
        # ------------------------------
        if options.get('end'):
            date = str_to_date(options['end'])
            if date:
                end_date = date


        root_url = "http://jsmnew.doko.link/service_api.php"
        key = "d296c101daa88a51f6ca8cfc1ac79b50"
        urla = "{}?key={}&module=yahoo&startDate={}&endDate={}".format(root_url, key, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

        fname = "ylots.json"
        r = requests.post(urla)
        content = r.json()
        f = open_file(fname, "w+")
        f.write(json.dumps(content))
        f.close()
