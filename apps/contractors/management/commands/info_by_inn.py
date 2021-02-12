#-*- coding:utf-8 -*-
import os
import requests
import logging

from django.core.management.base import BaseCommand

from apps.main_functions.catcher import json_pretty_print
from apps.contractors.services import get_info_by_inn

logger = logging.getLogger('simple')

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--inn',
            action = 'store',
            dest = 'inn',
            type = str,
            default = False,
            help = 'Show info by inn')

    def handle(self, *args, **options):
        """Получение данные по ИНН"""
        url = 'https://egrul.nalog.ru/'
        inn = ''
        if options.get('inn'):
            inn = options['inn']
        if not inn:
            logger.info('inn not set')
            return
        print(json_pretty_print(get_info_by_inn(inn)))
