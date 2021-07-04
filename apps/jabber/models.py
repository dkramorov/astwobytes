# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

class Jabber(Standard):
    """Модель пустышка"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Jabber - чат'
        verbose_name_plural = 'Jabber - чаты'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        default_permissions = []

    def save(self, *args, **kwargs):
        super(Jabber, self).save(*args, **kwargs)

