#-*- coding:utf-8 -*-
import os
import logging
from ftplib import FTP

from django.core.management.base import BaseCommand

from apps.main_functions.files import open_file, full_path, make_folder

logger = logging.getLogger('main')

"""
выгрузку производить по адресу:92.53.96.221
Логин: dsarhirus_gorm
Пароль: U6ywjEYm
Порт: 21
для выгрузки папка: all
для картинок: picture
для второго пункта, папка: price
"""

def get_imports(ftp, dir: str):
    """Получаем всякие import0_1.xml из папки
       :param ftp: ftp соединение
       :param dir: путь
    """
    dest_folder = 'share'
    make_folder(dest_folder)
    make_folder(os.path.join(dest_folder, dir))
    content = ftp.nlst(dir) # ['all/import0_1.xml']
    for item in content:
        if not item.endswith('.xml'):
            continue
        source_file = os.path.join(dest_folder, item)
        with open_file(source_file, 'wb+') as f:
            ftp.retrbinary('RETR %s' % item, f.write)

def parse_imports(files: list):
    """Парсим файлы типа import0_1.xml и обновляем номенклатуру
       :param files: список файлов
    """


class Command(BaseCommand):
    """Проверка формирования файла с заказами"""
    def add_arguments(self, parser):
        parser.add_argument('--fake',
            action = 'store',
            dest = 'fake',
            type = str,
            default = False,
            help = 'Set fake')
    def handle(self, *args, **options):
        ftp = FTP(host='92.53.96.221', user='dsarhirus_gorm', passwd='U6ywjEYm')
        content = ftp.nlst()
        for item in content:
            if item == 'all':
                imports = get_imports(ftp, item)
        ftp.quit()
