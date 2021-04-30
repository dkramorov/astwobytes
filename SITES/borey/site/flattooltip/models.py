# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.flatcontent.models import Blocks

class FlatToolTip(Standard):
    """Модель для создания подсказок на изобржениях flatcontent
       нужно для спецэффекта появления подсказки на картинке"""
    direction_choices = (
        (2, 'Слева'),
        (4, 'Справа'),
    )
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    xpos = models.IntegerField(blank=True, null=True, db_index=True)
    ypos = models.IntegerField(blank=True, null=True, db_index=True)
    img_size = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    direction = models.IntegerField(choices=direction_choices, blank=True, null=True, db_index=True, verbose_name='Направление/размещение подсказки')
    block = models.ForeignKey(Blocks, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подсказки - Подсказка'
        verbose_name_plural = 'Подсказки - Подсказки'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)

    def save(self, *args, **kwargs):
        super(FlatToolTip, self).save(*args, **kwargs)

