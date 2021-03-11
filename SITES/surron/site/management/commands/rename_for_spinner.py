#-*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import os
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from apps.main_functions.files import ListDir, isForD, full_path, drop_file

logger = logging.getLogger('main')

def drop_half_files(source_folder):
    """Наибнуть половину файлов"""
    items = ListDir(source_folder)
    for item in items:
        if not item.endswith('.jpg'):
            continue
        fin = item[-5]
        if fin in ('0', '2', '4', '6', '8'):
            src = os.path.join(source_folder, item)
            drop_file(src)

class Command(BaseCommand):
    """Проверка формирования файла с заказами"""
    def add_arguments(self, parser):
        parser.add_argument('--folder',
            action = 'store',
            dest = 'folder',
            type = str,
            default = False,
            help = 'Set folder with spinner files')
    def handle(self, *args, **options):
        #source_folder = 'spinner360/light_bee'
        source_folder = 'spinner360/test360'
        #drop_half_files(source_folder)
        items = ListDir(source_folder)
        z = 0
        for item in items:
            if not item.endswith('.jpg'):
                continue
            src = os.path.join(source_folder, item)
            if not isForD(src) == 'file':
                continue
            z += 1
            digit = z
            if z < 100:
                digit = '0%s' % z
            if z < 10:
                digit = '00%s' % z
            dest = os.path.join(source_folder, 'frame_%s.jpg' % digit)
            os.rename(full_path(src), full_path(dest))




