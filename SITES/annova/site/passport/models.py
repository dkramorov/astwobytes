# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.flatcontent.models import Blocks
from apps.personal.models import Shopper

class Passport(Standard):
    """Паспортные данные
    """
    passport_choices = (
        (1, 'Паспорт гражданина РФ'),
        (2, 'Загранпаспорт гражданина РФ'),
    )
    shopper = models.ForeignKey(Shopper,
        blank=True, null=True,
        on_delete = models.SET_NULL,
        verbose_name='Пользователь')
    birthday = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата рождения')
    series = models.CharField(max_length=64,
        blank=True, null=True, db_index=True,
        verbose_name='Серия паспорта')
    number = models.CharField(max_length=64,
        blank=True, null=True, db_index=True,
        verbose_name='Номер паспорта')
    issued = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Кем выдан')
    issued_date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Когда выдан')
    registration = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Адрес регистрации')
    ptype = models.IntegerField(choices=passport_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Тип паспорта: рф/загран'
    )

    class Meta:
        verbose_name = 'Пользователь - Паспортные данные'
        verbose_name_plural = 'Пользователь - Паспортные данные'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(Passport, self).save(*args, **kwargs)

