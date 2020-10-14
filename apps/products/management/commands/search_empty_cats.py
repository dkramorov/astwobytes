#-*- coding:utf-8 -*-
import os
import logging

from django.db.models import Count
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.flatcontent.models import Containers, Blocks
from apps.products.models import ProductsCats

logger = logging.getLogger('main')

def recursive_search_products(blocks,
                              drop_empty: bool = False,
                              set_inactive_empty: bool = False):
    """Рекурсивный обход каталога в поиске товаров,
       там, где товары не встретились, надо выполнить
       is_active=False, либо удалить рубрику
       :param blocks: блоки контейнера
       :param drop_empty: удалять пустые рубрики?
       :param set_inactive_empty: проставлять is_active=False пустым рубрикам
    """
    for block in blocks:
        products_count = ProductsCats.objects.filter(cat=block).aggregate(Count('id'))['id__count']
        if not products_count:
            parents = '_%s' % block.id
            if block.parents:
                parents = '%s%s' % (block.parents, parents)
            subblocks = Blocks.objects.filter(parents=parents)
            if subblocks:
                recursive_search_products(subblocks, drop_empty, set_inactive_empty)
            else:
                logger.info('empty cat %s' % block.id)
                if drop_empty:
                    block.delete()
                elif set_inactive_empty:
                    Blocks.objects.filter(pk=block.id).update(is_active=False)

class Command(BaseCommand):
    """Помечаем пустые рубрики каталогов неактивными,
       либо совсем удаляем
    """
    def add_arguments(self, parser):
        parser.add_argument('--drop_empty',
            action = 'store_true',
            dest = 'drop_empty',
            default = False,
            help = 'Drop empty cat')
        parser.add_argument('--set_inactive_empty',
            action = 'store_true',
            dest = 'set_inactive_empty',
            default = False,
            help = 'Set is_active=False for empty cat')

    def handle(self, *args, **options):
        drop_empty = False
        if options.get('drop_empty'):
            drop_empty = True
        set_inactive_empty = False
        if options.get('set_inactive_empty'):
            set_inactive_empty = True

        catalogues = Containers.objects.filter(state=7)
        for catalogue in catalogues:
            logger.info(catalogue.name)
            blocks = catalogue.blocks_set.filter(parents='')
            recursive_search_products(blocks, drop_empty, set_inactive_empty)

