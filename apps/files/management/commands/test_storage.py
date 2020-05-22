#-*- coding:utf-8 -*-
import os
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.files.boto_storage import StorageS3

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

