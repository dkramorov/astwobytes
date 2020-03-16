# -*- coding: utf-8 -*-
import logging
import os

from django.core.management.base import BaseCommand

from apps.main_functions.fortasks import search_process
from apps.main_functions.files import ListDir, isForD, drop_file, full_path

logger = logging.getLogger(__name__)

def drop_empty_folders(path: str = ''):
    """Удаление пустых папок"""
    items = ListDir(path)
    for item in items:
        new_path = os.path.join(path, item)
        if isForD(new_path) == 'dir':
            drop_empty_folders(new_path)
    if not items:
        fname = full_path(path)
        os.rmdir(fname)
        logger.info('drop_file %s' % fname)

class Command(BaseCommand):
    def handle(self, *args, **options):
        """Удаление пустых папок в media"""
        is_running = search_process(q = ('drop_empty_media_folders', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()
        drop_empty_folders()

