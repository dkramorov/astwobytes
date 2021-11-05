#-*- coding:utf-8 -*-
import os
import time
import logging
import json

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from cairosvg import svg2png

from apps.flatcontent.models import Containers, Blocks
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import open_file, full_path, imageThumb, check_path

from apps.site.companies.models import MainCompany

logger = logging.getLogger(__name__)

default_folder = settings.MEDIA_ROOT

def to_png(svg_code: str, output: str):
    """Конвертация svg => png
       :param svg_code: svg строкой
       :param output: путь для сохранения png
    """
    svg2png(bytestring=svg_code, write_to=output)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--demo_mode',
            action = 'store_true',
            dest = 'demo_mode',
            default = False,
            help = 'Set demo mode')
        parser.add_argument('--cat_id',
            action = 'store',
            dest = 'cat_id',
            type = str,
            default = False,
            help = 'Set cat tag for update')

    def handle(self, *args, **options):
        started = time.time()
        errors = []
        for main_company in MainCompany.objects.filter(img__endswith='.svg'):
            if main_company.img.startswith('http'):
                errors.append('svg in url %s' % main_company.id)
                continue
            folder = main_company.get_folder()
            svg = os.path.join(folder, main_company.img)
            new_img = '%s.png' % main_company.id
            dest = os.path.join(folder, new_img)
            if check_path(svg):
                errors.append('svg not found %s, company %s' % (svg, main_company.id))
                continue
            with open_file(svg, 'r', encoding='utf-8') as f:
                try:
                    to_png(f.read(), full_path(dest))
                except Exception as e:
                    print(e)
                    errors.append('svg incorrect %s, company %s' % (svg, main_company.id))
                    continue

                if imageThumb(dest, 600, 600):
                    MainCompany.objects.filter(pk=main_company.id).update(img=new_img)
                    print(folder, main_company.img, '=>', new_img)
                else:
                    errors.append('error with resize after convert %s, company %s' % (svg, main_company.id))
        print(json_pretty_print(errors))
