# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.flatcontent.models import Blocks

class Phones(Standard):
    """Телефоны 8800
    """
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Наименование контрагента')
    code = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Код контрагента')
    phone = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Телефон')
    email = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Email')
    site = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Сайт')
    menu = models.ForeignKey(Blocks,
        on_delete=models.CASCADE,
        blank=True, null=True, db_index=True,
        verbose_name='Привязка к менюшке')
    info1 = models.TextField(blank=True, null=True,
        verbose_name='Информация 1')
    info2 = models.TextField(blank=True, null=True,
        verbose_name='Информация 1')
    info3 = models.TextField(blank=True, null=True,
        verbose_name='Информация 1')

    class Meta:
        verbose_name = 'Телефоны 8800 - Телефон 8800'
        verbose_name_plural = 'Телефоны 8800 - Телефоны 8800'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(Phones, self).save(*args, **kwargs)

