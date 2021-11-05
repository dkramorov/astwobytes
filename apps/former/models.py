# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

class Former(Standard):
    """Конструктор форм"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    desc = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Former - конструктор форм'
        verbose_name_plural = 'Former - конструкторы форм'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(Former, self).save(*args, **kwargs)

