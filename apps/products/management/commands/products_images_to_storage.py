#-*- coding:utf-8 -*-
import os
import logging

from django.db.models import Count
from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.files import check_path, full_path, drop_folder
from apps.files.boto_storage import StorageS3
from apps.products.models import Products, ProductsPhotos

logger = logging.getLogger('main')

class Command(BaseCommand):
    """Проверка функций работы с хранилищем"""
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--create_bucket',
            action = 'store_true',
            dest = 'create_bucket',
            default = False,
            help = 'Create bucket in storage')
        parser.add_argument('--upload',
            action = 'store',
            dest = 'upload',
            type = str,
            default = False,
            help = 'Upload file to storage')
        parser.add_argument('--remove',
            action = 'store',
            dest = 'remove',
            type = str,
            default = False,
            help = 'Remove file from storage')

    def handle(self, *args, **options):
        if options.get('create_bucket'):
            logger.info('create bucket => %s' % StorageS3(bucket_name='my_bucket2').bucket)
            return

        if options.get('upload'):
            s3 = StorageS3()
            path = options['upload']
            if not os.path.exists(path):
                path = os.path.join(settings.STATIC_ROOT, 'img/ups.png')
            fname = os.path.split(path)[-1]

            result = s3.upload_to_storage(path, fname, prefix='test1')
            logger.info('%s => %s' % (path, result))

            result = s3.upload_to_storage(path, fname, prefix='test2')
            logger.info('%s => %s' % (path, result))

        if options.get('remove'): # ups.png
            s3 = StorageS3()
            fname = options['remove']

            result = s3.drop_from_storage(fname, prefix='test1')
            logger.info('%s => %s' % (fname, result))

            result = s3.drop_from_storage(fname, prefix='test2')
            logger.info('%s => %s' % (fname, result))

        """Загрузка всех фоток в хранилище"""
        s3 = StorageS3(bucket_name='')
        prefix = 'photos'
        photos_query = ProductsPhotos.objects.all().exclude(img__startswith='http')
        by = 100
        total_photos = photos_query.aggregate(Count('id'))['id__count']
        total_pages = int(total_photos / by) + 1
        for i in range(total_pages):
            rows = photos_query[i*by:i*by+by]
            for row in rows:
                path = row.imagine()
                fpath = full_path(path)
                if not check_path(fpath):
                    url = s3.upload_to_storage(fpath, row.img, prefix=prefix)
                    if url:
                        ProductsPhotos.objects.filter(pk=row.id).update(img=url)
                        drop_folder(row.get_folder())

        prefix = 'products'
        products_query = Products.objects.filter(img__isnull=False).exclude(img__startswith='http')
        by = 100
        total_photos = products_query.aggregate(Count('id'))['id__count']
        total_pages = int(total_photos / by) + 1
        for i in range(total_pages):
            rows = products_query[i*by:i*by+by]
            for row in rows:
                path = row.imagine()
                fpath = full_path(path)
                if not check_path(fpath):
                    url = s3.upload_to_storage(fpath, row.img, prefix=prefix)
                    if url:
                        Products.objects.filter(pk=row.id).update(img=url)
                        drop_folder(row.get_folder())
