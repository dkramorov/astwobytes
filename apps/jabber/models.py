# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

class Registrations(Standard):
    """Регистрации с приложений
       state=1 - подтвержденные, такие уже не трогаем
    """
    phone = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Телефон пользователя')
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
        super(Registrations, self).save(*args, **kwargs)

