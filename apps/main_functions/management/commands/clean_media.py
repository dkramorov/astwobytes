#-*- coding:utf-8 -*-
import os
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.fortasks import search_process
from apps.main_functions.files import (check_path,
                                       full_path,
                                       image_to_RGB,
                                       imageThumb,
                                       drop_folder,
                                       isForD,
                                       ListDir, )
logger = logging.getLogger('main')

FOLDERS_BLACK_LIST = (
    '.DS_Store',
)

def drop_if_empty(folder: str = ''):
    """Удалить папку если она пустая
       :param folder: папка
    """
    items = ListDir(folder)
    if not items:
        logger.info('[DROP because EMPTY]: %s' % folder)
        drop_folder(folder)
        return
    # Перебираем мусор
    for item in items:
        path = os.path.join(folder, item)
        if item in FOLDERS_BLACK_LIST:
            logger.info('[DROP from BLACK LIST]: %s' % path)
            drop_folder(path)
        else:
            if isForD(path) == 'folder':
                drop_if_empty(path)

class Command(BaseCommand):
    """Почистить папку media"""
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--drop_empty_folders',
            action = 'store_true',
            dest = 'drop_empty_folders',
            default = False,
            help = 'Drop empty folders')
        parser.add_argument('--drop_pyc',
            action = 'store_true',
            dest = 'drop_pyc',
            default = False,
            help = 'Drop pyc files')

    def handle(self, *args, **options):

        is_running = search_process(q = ('clean_media', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()

        if options.get('drop_empty_folders'):
            drop_if_empty()

        if options.get('drop_pyc'):
            os.system('find %s -name "*.pyc" -exec rm -f {} \;' % (settings.BASE_DIR, ))
            os.system('find %s -name ".DS_Store" -exec rm -f {} \;' % (settings.BASE_DIR, ))
            os.system('find %s -name __pycache__ -exec rmdir {} \+' % (settings.BASE_DIR, ))
