# -*- coding: utf-8 -*-
import logging
import xml.etree.ElementTree as ET
from django.db.models import Q

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.str2xml import parse_query, make_query

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--fake',
            action = 'store_true',
            dest = 'fake',
            default = False,
            help = 'Do nothing')
        parser.add_argument('--fake_value',
            action = 'store',
            dest = 'fake_value',
            type = str,
            default = False,
            help = 'Set fake value')

    def handle(self, *args, **options):
        """Тестирование парсинга запроса"""
        xml_query = parse_query('state=true and (substate=true and level=1 or (substate=false and level=2))')
        print(ET.tostring(xml_query, encoding='unicode'))
        query = make_query(xml_query)
        print('->', query)

