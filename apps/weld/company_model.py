# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

class Company(Standard):
    """Компания,
       на их балансе находятся работы,
       например, ООО "ИНК" или ЛНК
    """
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    class Meta:
        verbose_name = 'Сварочные соединения - Компания'
        verbose_name_plural = 'Сварочные соединения - Компании'
        #default_permissions = []
