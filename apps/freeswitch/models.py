# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

class Redirects(Standard):
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    link = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    desc = models.TextField(blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    path = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Freeswitch - Переадресация'
        verbose_name_plural = 'Freeswtich - Переадресации'



