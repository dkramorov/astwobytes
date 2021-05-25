# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.currency_cbr import get_currency_cbr

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--fake',
            action = 'store_true',
            dest = 'fake',
            default = False,
            help = 'Do nothing')
        parser.add_argument('--date',
            action = 'store',
            dest = 'date',
            type = str,
            default = False,
            help = 'Set date')

    def handle(self, *args, **options):
        """Тестирование получения курса валют с центробанка"""
        date = None
        if options.get('date'):
            date = options['date']
        print(json_pretty_print(get_currency_cbr(date)))

