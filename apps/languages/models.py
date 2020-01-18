# -*- coding: utf-8 -*-
from django.db import models
from apps.main_functions.models import Standard
from django.contrib.contenttypes.models import ContentType

class Translate(Standard):
    """Переводы для модели/поля"""
    domain_pk = models.IntegerField(blank = True,
        null = True,
        verbose_name = 'Домен на каждый сайт из settings.py',
        db_index = True)
    content_type = models.ForeignKey(ContentType,
        blank = True,
        null = True,
        on_delete = models.CASCADE,
        verbose_name = 'Привязка к модели')
    model_pk = models.IntegerField(blank=True,
        null = True,
        verbose_name = 'id по content_type',
        db_index = True)
    field = models.CharField(max_length=255,
        blank = True,
        null = True,
        verbose_name = 'Поле, которое переводим',
        db_index = True)
    text = models.TextField(blank=True,
        null = True,
        verbose_name = 'Перевод')

    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'

