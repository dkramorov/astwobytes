# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.net_tools.models import IPAddress

class Comp(Standard):
    """Компутеры"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    ip = models.ForeignKey(IPAddress, blank=True, null=True, on_delete=models.SET_NULL)
    api_enabled = models.BooleanField(default=False, db_index=True,
        verbose_name='Включено ли апи')

    class Meta:
        verbose_name = 'Miners - Компьютер'
        verbose_name_plural = 'Miners - Компьютеры'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(Comp, self).save(*args, **kwargs)

