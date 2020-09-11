# -*- coding: utf-8 -*-
import logging
import os
from django.conf import settings

from boto import connect_s3
from boto.exception import S3CreateError, S3ResponseError

from django_boto.s3.storage import S3Storage
from django_boto.s3.shortcuts import upload

logger = logging.getLogger('main')

"""
Работа с https://mcs.mail.ru
Access key ID и Secret access key вы можете создать в административном интерфейсе сервиса Cloud Storage в разделе «Аккаунты»

Действия с ключами (Keys) можно делать через Bucket
TODO: исключить django_boto из схемы

import mimetypes
from boto.s3.connection import Bucket, Key
from boto import connect_s3
a = connect_s3(aws_access_key_id=settings.GS_ACCESS_KEY_ID, aws_secret_access_key=settings.GS_SECRET_ACCESS_KEY, host=settings.GS_HOST, is_secure=False)
S3Connection:storage.googleapis.com
bucket = a.get_bucket(settings.GS_BUCKET_NAME)
fname = '/home/jocker/Downloads/test.txt'
mime = mimetypes.guess_type(fname)[0]
content = open(fname).read()
k = Key(bucket)
k.key = 'test/text.txt'
k.set_metadata('Content-Type', mime)
k.set_contents_from_string(content) # .set_contents_from_filename(open(fname))
k.set_acl('public-read')
# k.delete()
"""

class StorageS3(S3Storage):
    # https://github.com/qnub/django-boto/blob/master/django_boto/s3/storage.py
    # На случай сраного
    # ssl.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
    # certificate verify failed (_ssl.c:852)
    # переопределяем самостоятельно s3 и бакет
    # USAGE: StorageS3(bucket_name='my_bucket2')
    @property
    def bucket(self):
        if not self._bucket:
            self.s3 = connect_s3(
                aws_access_key_id=self.key,
                aws_secret_access_key=self.secret,
                host=self.host, is_secure=False)
            try:
                self._bucket = self.s3.create_bucket(
                    self.bucket_name, location=self.location, policy=self.policy)
            except (S3CreateError, S3ResponseError):
                self._bucket = self.s3.get_bucket(self.bucket_name)
        return self._bucket

    def upload_to_storage(self, path: str,
                          name: str, prefix: str = 'test', **kwargs):
        """Загрузка файла в хранилище
           :param path: путь по которому надо сохранить файл
           :param name: имя файла
           :param prefix: префикс пути до файла
           :return: ссылка на файл
        """
        if not isinstance(path, str):
            logger.exception('path is not str')
            return None
        f = open(path, 'rb')
        fname = os.path.join(prefix, name.lstrip('/'))
        self.save(fname, f)
        # url(full_path, expires, query_auth, force_http)
        return self.url(fname, 30, False, False)

    def drop_from_storage(self, name: str, prefix: str = 'test', **kwargs):
        """Удаление файла из хранилища
           :param name: имя файла
           :param prefix: префикс пути до файла
        """
        fname = os.path.join(prefix, name.lstrip('/'))
        self.delete(fname)


class CustomBotoStorage:
    def __init__(self):
        self.conn = connect_s3(
            aws_access_key_id=settings.GS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.GS_SECRET_ACCESS_KEY,
            host=settings.GS_HOST,
            is_secure=False, )
        self.bucket = self.conn.get_bucket(settings.GS_BUCKET_NAME)

    def update_file_by_content(self,
                               fname: str,
                               content: str,
                               mime: str = 'text/xml',
                               acl: str = 'public-read'):
        """Обновление файла в хранилище
           :param fname: путь до файла в хранилище
           :param content: содержимое файла
           :param mime: mimetype файла
           :param acl: разрешение на файл
        """
        k = Key(self.bucket)
        k.key = fname
        k.set_metadata('Content-Type', mime)
        k.set_contents_from_string(content)
        k.set_acl(acl)

    def get_content(self, fname: str):
        """Получить файл из хранилища
           :param fname: путь до файла в хранилище
        """
        k = Key(self.bucket)
        k.key = fname
        return k.get_contents_as_string()

    def is_exists(self, fname: str):
        """Узнать, существует ли файл в хранилище
           :param fname: путь до файла в хранилище
        """
        return self.bucket.get_key(fname)
