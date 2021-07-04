# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

class Vocabulary(Standard):
    """Запросы для раскрутки (семантический словарь)"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Promotion - поисковый запрос'
        verbose_name_plural = 'Promotion - поисковые запросы'

    def save(self, *args, **kwargs):
        analogs = Vocabulary.objects.filter(name=self.name)
        if self.id:
            analogs = analogs.exclude(pk=self.id)
        if analogs:
            return

        super(Vocabulary, self).save(*args, **kwargs)

class SVisits(Standard):
    """Статистика для посещений сайтов ботом"""
    date = models.DateField(blank=True, null=True, db_index=True)
    ip = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    company_id = models.IntegerField(blank=True, null=True, db_index=True)
    profile = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    count = models.IntegerField(blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Promotion - посещение сайта'
        verbose_name_plural = 'Promotion - посещения сайтов'

class SeoReport(Standard):
    """Отчет о сео-проблемах"""
    state_choices = (
        1, 'Нет названия компании',
        2, 'Не заполнен title',
        3, 'Дублирующийся title',
    )
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    link = models.CharField(max_length=255, blank=True, null=True, db_index=True)

