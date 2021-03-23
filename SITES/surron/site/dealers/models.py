# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.addresses.models import Address

class Dealer(Standard):
    """Дилеры"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    address = models.ForeignKey(Address,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Адрес')
    worktime = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    site = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    phone = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Дилеры - Дилер'
        verbose_name_plural = 'Дилеры - Дилеры'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(Dealer, self).save(*args, **kwargs)

