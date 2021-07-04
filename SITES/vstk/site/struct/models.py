# -*- coding: utf-8 -*-
from django.db import models

from apps.files.models import Files
from apps.main_functions.models import Standard

class StructObject(Standard):
    """Объект
       ГИП (главный инженер проекта)
           заполняет
           1) исходные данные
           2) техническое задание на проектирование
              (согласованное с заказчиком)
       Архитектурный отдел (АР)
           заполняет
           1) предварительные планировочные решения
              (планы этажей, разрезы зданий)
           2) описательная часть
       Инженерный (ОВ, ВК, ЭМ) и Конструкторский отделы (КР)
           заполняют
           1) задания на дополнение, внесение изменений в
              планировочные решения от КР, ОВ, ВК, ЭМ
       Архитектурный отдел
           заполняет
           1) планировочные решения
              (планы этажей, разрезы зданий)
              для дальнейшей работы КР, ОВ, ВК, ЭМ
       Инженерный (ОВ, ВК, ЭМ) и Конструкторский отделы (КР)
           заполняют
           1) задания на отверстия для КР от ОВ, ВК, ЭМ
    """
    state_choice = (
        (1, 'Гип вносит исходные данные и тех. задание на проектирование'),
        (2, 'Архитектурный отедл вносит предварительные планировочные решения и описательную часть'),
        (3, 'Инженерный и конструкторский отедлы вносят задания на дополнение, внесение изменений в планировочные решения от КР, ОВ, ВК, ЭМ'),
        (4, 'Архитектурный отедл вносит планировочные решения для дальнейшей работы КР, ОВ, ВК, ЭМ'),
        (5, 'Задания на отверстия для КР от ОВ, ВК, ЭМ'),
    )
    name = models.CharField(max_length=255, blank=True, null=True,
        db_index=True)
    description = models.CharField(max_length=255, blank=True, null=True,
        db_index=True)

    class Meta:
        verbose_name = 'Объекты - объект'
        verbose_name_plural = 'Объекты - объекты'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(StructObject, self).save(*args, **kwargs)

class GenericStructObject(Standard):
    """Общая модель для сущностей структуры"""
    obj = models.ForeignKey(StructObject, blank=True, null=True,
        on_delete=models.CASCADE,
        verbose_name='Объект')
    name = models.CharField(max_length=255, blank=True, null=True,
        db_index=True)
    description = models.CharField(max_length=255, blank=True, null=True,
        db_index=True)
    doc = models.ForeignKey(Files, blank=True, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Документ/Файл')

    class Meta:
        abstract = True

class SourceData(GenericStructObject):
    """Исходные данные для проекта"""

    class Meta:
        verbose_name = 'Объекты - исходные данные'
        verbose_name_plural = 'Объекты - исходные данные'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

class TechTask(GenericStructObject):
    """Техническое задание на проектирование"""

    class Meta:
        verbose_name = 'Объекты - тех. задание'
        verbose_name_plural = 'Объекты - тех. задания'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

class PrePlanDesicions(GenericStructObject):
    """Предварительные планировочные решения
       (планы этажей, разрезы зданий)
    """

    class Meta:
        verbose_name = 'Объекты - пред. планировочное решение'
        verbose_name_plural = 'Объекты - пред. планировочные решения'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

class Descriptions(GenericStructObject):
    """Описательная часть
    """

    class Meta:
        verbose_name = 'Объекты - описательная часть'
        verbose_name_plural = 'Объекты - описательные части'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

class ChangeTasks(GenericStructObject):
    """Задания на дополнение, внесение изменений
       и планировочные решения от КР, ОВ, ВК, ЭМ
    """

    class Meta:
        verbose_name = 'Объекты - задание на изменение'
        verbose_name_plural = 'Объекты - задания на изменения'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

class PlanDesicions(GenericStructObject):
    """Планировочные решения
       (планы этажей, разрезы зданий)
       для дальнейшей работы КР, ОВ, ВК, ЭМ
    """

    class Meta:
        verbose_name = 'Объекты - планировочное решение'
        verbose_name_plural = 'Объекты - планировочные решения'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

class HoleTasks(GenericStructObject):
    """Задания на отверстия для КР от ОВ, ВК, ЭМ
    """

    class Meta:
        verbose_name = 'Объекты - задание на отверстие'
        verbose_name_plural = 'Объекты - задания на отверстия'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

