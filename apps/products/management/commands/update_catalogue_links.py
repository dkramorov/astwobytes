#-*- coding:utf-8 -*-
import os
import logging

from django.db.models import Count
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.flatcontent.models import Containers, Blocks
from apps.products.models import ProductsCats

logger = logging.getLogger('main')

def recursive_update_links(blocks, container):
    """Рекурсивный обход каталога и обновление ссылей,
       там, где товары не встретились, надо выполнить
       is_active=False, либо удалить рубрику
       :param blocks: блоки контейнера
       :param container: контейнер подливаем в блок, чтобы постоянно его не выдирать
    """
    for block in blocks:
        block.container = container
        old_link = block.link
        block.create_cat_link(force=True)
        if not old_link == block.link:
            Blocks.objects.filter(pk=block.id).update(link=block.link)

        # В каталожных линковках обновляем контейнер,
        # потому что не может быть, что привязка к одной категории,
        # а контейнер - другой
        ProductsCats.objects.filter(cat=block).update(container=container)

        parents = '_%s' % block.id
        if block.parents:
            parents = '%s%s' % (block.parents, parents)
        subblocks = Blocks.objects.filter(parents=parents)
        if subblocks:
            recursive_update_links(subblocks, container)

class Command(BaseCommand):
    """Помечаем пустые рубрики каталогов неактивными,
       либо совсем удаляем
    """
    def add_arguments(self, parser):
        parser.add_argument('--repair_cat_links',
            action = 'store_true',
            dest = 'repair_cat_links',
            default = False,
            help = 'Repair cat links, fill parent container')

    def handle(self, *args, **options):
        catalogues = Containers.objects.filter(state=7)
        for catalogue in catalogues:
            logger.info(catalogue.name)
            blocks = catalogue.blocks_set.select_related('container').filter(parents='')
            recursive_update_links(blocks, catalogue)

