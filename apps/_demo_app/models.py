# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

class DemoModel(Standard):
    """Модель пустышка для быстрого создания новой рабочей модельки для админки"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'DemoApp - demo_object'
        verbose_name_plural = 'DemoApp - demo_objects'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(DemoModel, self).save(*args, **kwargs)

