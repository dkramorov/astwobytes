#-*- coding:utf-8 -*-
import os
import logging

from django.db.models import Count
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.flatcontent.models import Blocks
from apps.flatcontent.flatcat import get_filters_for_cat

logger = logging.getLogger('main')

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
        cat = None
        if options.get('cat'):
            cat = Blocks.objects.filter(pk=options['cat']).first()
        if not cat:
            logger.info('cat not found')
            return
        logger.info('cat %s, %s' % (cat.tag, cat.link))
        result = get_filters_for_cat(cat.id)
        print(result.get('from_cache'))
        #print(json_pretty_print(get_filters_for_cat(cat.id)))

