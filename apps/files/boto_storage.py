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


