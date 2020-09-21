#-*- coding:utf-8 -*-
import os
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.files import make_folder, check_path, full_path, ListDir, open_file

logger = logging.getLogger(__name__)

import mammoth

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--path',
            action = 'store',
            dest = 'path',
            type = str,
            default = False,
            help = 'Set path to docx folder')

    def handle(self, *args, **options):
        """Конвертация docx в html"""
        path = 'docx'
        dest_path = 'mammoth'
        make_folder(dest_path)
        if options.get('path'):
            path = options['path']
        if check_path(path):
            logger.info('path not exists')
            return
        files = ListDir(path)
        for item in files:
            if not item.endswith('.docx'):
                continue
            cur_item = os.path.join(path, item)
            with open(full_path(cur_item), 'rb') as docx_file:
                result = mammoth.convert_to_html(docx_file)
                html = result.value
                messages = result.messages
                #print(messages) #warnings
                dest = os.path.join(dest_path, item.replace('.docx', '.html'))
                with open_file(dest, 'w+') as f:
                    f.write(html)

