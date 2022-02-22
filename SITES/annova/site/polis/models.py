# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.shop.models import Orders

class Polis(Standard):
    """Оформленный полис
    """
    order = models.OneToOneField(Orders,
        blank=True, null=True, db_index=True,
        on_delete=models.SET_NULL,
        verbose_name='Ссылка на заказ')
    number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер полиса/заказа')
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='ФИО')
    birthday = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата рождения')
    insurance_sum = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Общая страховая сумма')
    insurance_program = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Страховая программа')
    from_date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Период страхования с')
    to_date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Период страхования до')
    class Meta:
        verbose_name = 'Страховка - Полис'
        verbose_name_plural = 'Страховка - Полисы'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(Polis, self).save(*args, **kwargs)

