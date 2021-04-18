# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

class Robots(Standard):
    """Роботы"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    selenium_version = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    chrome_version = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    ip = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    server_name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    server_free_space = models.IntegerField(blank=True, null=True, db_index=True)
    info = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Роботы - Робот'
        verbose_name_plural = 'Роботы - Роботы'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(Robots, self).save(*args, **kwargs)

