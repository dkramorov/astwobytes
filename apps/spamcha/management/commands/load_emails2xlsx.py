# -*- coding: utf-8 -*-
import os
import logging
import json
import requests
import xlsxwriter

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.main_functions.files import make_folder, full_path

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--test',
            action = 'store_true',
            dest = 'test',
            default = False,
            help = 'TEST')

    def handle(self, *args, **options):
        """Загрузка email ов для формирования xlsx
           для загрузки в спам лист для рассылки"""
        fname = 'clients_emails'
        link = 'https://223-223.ru/media/%s.json' % fname
        r = requests.get(link)
        rows = json.loads(r.text)
        folder = 'spamcha'
        make_folder(folder)

        xls_file = '%s.xlsx' % fname
        dest = full_path(os.path.join(folder, xls_file))
        book = xlsxwriter.Workbook(dest)
        sheet = book.add_worksheet('Лист 1')
        row_number = 0

        titles = (
            'client_id',
            'client_name',
            'dest',
            'name',
        )
        for i, title in enumerate(titles):
            sheet.write(row_number, i, title)

        for row in rows:
            row_number += 1
            for i, field in enumerate(row):
                sheet.write(row_number, i, field)
        book.close()

