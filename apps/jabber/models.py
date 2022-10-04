# -*- coding: utf-8 -*-
import hashlib
from django.db import models

from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.models import Standard

class FirebaseTokens(Standard):
    """Токены пользователей,
       т/к токен дается приложению,
       а войти он может под любым аккаунтом,
       то при каждой авторизации надо обновлять токен
    """
    login = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Логин (телефон) пользователя')
    token = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Токен приложения пользователя')
    apns_token = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Токен APNS приложения пользователя')
    ip = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='IP пользователя')

    def save(self, *args, **kwargs):
        if self.login:
            self.login = kill_quotes(self.login, 'int')
        super(FirebaseTokens, self).save(*args, **kwargs)

class Registrations(Standard):
    """Регистрации с приложений
       is_active=True - подтвержденные, такие уже не трогаем
    """
    phone = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Телефон пользователя')
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Имя пользователя')
    passwd = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Пароль пользователя')
    code = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Код подтверждения телефона пользователя')
    version = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Версия приложения')
    platform = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Платформа')

    class Meta:
        verbose_name = 'Jabber - регистрация'
        verbose_name_plural = 'Jabber - регистрации'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        default_permissions = []

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = kill_quotes(self.phone, 'int')
        super(Registrations, self).save(*args, **kwargs)

    def get_hash(self):
        """Получение хэша по логину и паролю"""
        forhash = '%s%s' % (self.phone, self.passwd)
        h = hashlib.sha256()
        h.update(forhash.encode('utf-8'))
        return h.hexdigest()

