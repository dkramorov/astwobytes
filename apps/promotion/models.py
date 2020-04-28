# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

class Vocabulary(Standard):
    """Запросы для раскрутки (семантический словарь)"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Promotion - семантический словарь'
        verbose_name_plural = 'Promotion - семантический словарь'

    def save(self, *args, **kwargs):
        analogs = Vocabulary.objects.filter(name=self.name)
        if self.id:
            analogs = analogs.exclude(pk=self.id)
        if analogs:
            return

        super(Vocabulary, self).save(*args, **kwargs)

