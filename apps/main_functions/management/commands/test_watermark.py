# -*- coding: utf-8 -*-
import logging
import time
import os
import shutil
import re
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.files import watermark_image, drop_folder

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--fake',
            action = 'store_true',
            dest = 'fake',
            default = False,
            help = 'Do nothing')
        parser.add_argument('--fake_value',
            action = 'store',
            dest = 'fake_value',
            type = str,
            default = False,
            help = 'Set fake value')

    def handle(self, *args, **options):
        """Тестирование создания вотремарки"""
        img_name = 'test.png'
        source = 'misc'
        #size = '150x150'
        size = ''
        mark = 'misc/logo_mini.png'
        position = 'tile'
        opacity = 0.025
        folder = 'resized'
        rotate = 45
        drop_folder('misc/resized')
        watermark_image(img_name,
                        source,
                        size,
                        mark,
                        position,
                        opacity,
                        folder,
                        rotate)

