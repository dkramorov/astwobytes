# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.weld.enums import replace_eng2rus

class Material(Standard):
    """Материал, сталь,
       например, 09Г2С
       только русские буквы для названия
    """
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    class Meta:
        verbose_name = 'Сварочные соединения - Материал (сталь)'
        verbose_name_plural = 'Сварочные соединения - Материалы (сталь)'
        #default_permissions = []

    def save(self, *args, **kwargs):
        if self.name:
            search_eng = replace_eng2rus(self.name)
            if not search_eng:
                assert False
        super(Material, self).save(*args, **kwargs)