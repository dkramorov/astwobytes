# -*- coding: utf-8 -*-
import logging
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.files import open_file
from apps.promotion.models import Vocabulary
from apps.main_functions.fortasks import search_process

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--fake',
            action = 'store_true',
            dest = 'fake',
            default = False,
            help = 'Do nothing')
    def handle(self, *args, **options):
        """Импорт запросов из selenium json файла"""
        is_running = search_process(q = ('import_selenium_json', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()
        with open('/home/jocker/selenium/json_queries.json') as f:
            queries = json.loads(f.read())
        for query in queries:
            query = query.strip()
            analog = Vocabulary.objects.filter(name=query).first()
            if not analog:
                Vocabulary.objects.create(name=query)

