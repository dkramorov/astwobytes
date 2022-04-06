#-*- coding:utf-8 -*-
import os
import logging

from django.db.models import Count
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.products.models import Products

logger = logging.getLogger('main')

def demo_search():
    """Тестовый индексный поиск"""
    search = Products.indexer.search('бассейн')
    for item in search:
        print(item)

class Command(BaseCommand):
    """Проверка фильтров
    """
    def add_arguments(self, parser):
        parser.add_argument('--cat',
            action = 'store',
            dest = 'cat',
            type = str,
            default = False,
            help = 'Ид категории')

    def handle(self, *args, **options):
        if 'djapian' in settings.INSTALLED_APPS:
            print('DJAPIAN_APP on')
        else:
            print('DJAPIAN_APP off, terminated.')
            return
        from djapian.utils import load_indexes
        load_indexes()
        print(len(Products().get_all_props(prop_key='prop__prop__id'))) # для Property
        print(len(Products().get_all_props(prop_key='prop__id'))) # для PropertiesValues
