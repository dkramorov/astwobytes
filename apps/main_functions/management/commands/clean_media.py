#-*- coding:utf-8 -*-
from django.core.management.base import BaseCommand#, CommandError
from django.conf import settings

from apps.main_functions.files import check_path, full_path, image_to_RGB, imageThumb, drop_folder, ListDir

import os

FOLDERS_BLACK_LIST = (
    '.DS_Store',
)

def drop_if_empty(folder: str = ''):
    """Удалить папку если она пустая
       :param folder: папка
    """
    items = ListDir(folder)
    if not items:
        drop_folder(folder)
    # Перебираем мусор
    for item in items:
        path = os.path.join(folder, item)
        if item in FOLDERS_BLACK_LIST:
            drop_foler(path)

class Command(BaseCommand):
  """Почистить папку media"""
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--drop_empty_folders',
            action = 'store_true',
            dest = 'drop_empty_folders',
            default = False,
            help = 'Drop empty folders')
        parser.add_argument('--index',
            action = 'store_true',
            dest = 'index',
            default = False,
            help = 'Partial djapian index')
    def handle(self, *args, **options):
        if options.get('drop_empty_folders'):
            drop_if_empty()
