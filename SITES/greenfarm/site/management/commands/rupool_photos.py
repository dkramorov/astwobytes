#-*- coding:utf-8 -*-
import re
import os
import time
import json
import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from apps.products.models import Products, Property, PropertiesValues, ProductsProperties, ProductsCats, ProductsPhotos
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.files import check_path, copy_file

logger = logging.getLogger(__name__)

"""Обновление фоток для товаров
   фотки получены с rupool rupool_report скриптом
"""

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
        folder = 'rupool/images'

        started = time.time()
        by = 100
        query = Products.objects.all()
        total_rows = query.aggregate(Count('id'))['id__count']
        pages = (int(total_rows/by)) + 1
        for i in range(pages):
            print('%s/%s' % (i+1, pages))
            products = query[i*by:i*by+by]
            for product in products:
                code = product.code
                if not code:
                    continue
                first_digit = code[0]
                src_folder = os.path.join(folder, first_digit)

                for photo in product.productsphotos_set.all():
                    photo.delete()

                for i in range(1, 10):
                    fname = '%s_%s.jpg' % (code, i)
                    src = os.path.join(src_folder, fname)
                    if check_path(src):
                        break

                    if i == 1:
                        product.drop_img()
                        dest = os.path.join(product.get_folder(), fname)
                        copy_file(src, dest)
                        Products.objects.filter(pk=product.id).update(img=fname)
                    else:
                        photo = ProductsPhotos.objects.create(product=product)
                        dest = os.path.join(photo.get_folder(), fname)
                        copy_file(src, dest)
                        ProductsPhotos.objects.filter(pk=photo.id).update(img=fname)

        elapsed = time.time() - started
        print('%.2f' % elapsed)

