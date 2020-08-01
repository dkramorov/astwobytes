# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.files.models import Files

"""
Верхний объект иерархии - это компания, затем объект,
объект делится на титулы - области с установками,
в титул входят установки, которые соединены линиями
Линии могут идти через весь объект, но
наименование линии будет зависеть от титула
В линиях стыки
"""

class Company(Standard):
    """Компания,
       на чьем балансе находятся работы,
       верхний уровень иерархии,
       например, ООО "ИНК"
    """
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Компания, наименование предприятия-заказчика, например, ООО "ИНК"')
    location = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Место строительства предприятия, например, Ярактикинское НГКМ')
    # подрядчик
    contractor = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Наименоваение генподрядной и строительной организации и ее ведомственная принадлежность, например, АО "Хоневелл"')
    # монтажник
    fitter = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Наименование монтажной организации, например, ООО "Транспромстрой"')

    class Meta:
        verbose_name = 'Справочники - Компания'
        verbose_name_plural = 'Справочники - Компании'
        #default_permissions = []

class Subject(Standard):
    """Объект,
       второй уровень иерархии,
       например, ГФУ
    """
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Наименование сооружаемого объекта, например, ')
    company = models.ForeignKey(Company,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Комания (объект), например ТПС')
    class Meta:
        verbose_name = 'Справочники - Объект'
        verbose_name_plural = 'Справочники - Объекты'
        #default_permissions = []
        unique_together = ('name', 'company',)

class Titul(Standard):
    """Титул, например, У800"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Часть объекта, например, У800')
    subject = models.ForeignKey(Subject,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Объект, например ТПС-ГФУ')
    class Meta:
        verbose_name = 'Справочники - Титул'
        verbose_name_plural = 'Справочники - Титулы'
        #default_permissions = []
        unique_together = ('name', 'subject',)

class Base(Standard):
    """Установка"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Установка, например, БНТК-2 ТХ-18')
    titul = models.ForeignKey(Titul,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Часть объекта, например, У800')
    class Meta:
        verbose_name = 'Справочники - Установка'
        verbose_name_plural = 'Справочники - Установки'
        #default_permissions = []
        unique_together = ('name', 'titul',)

class Line(Standard):
    """Линия, например, 677-А2-LT-150"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    titul = models.ForeignKey(Titul,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Часть объекта, например, У800')
    base = models.ForeignKey(Base,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Установка в составе титула, например, ')
    scheme_number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер изометрической схемы, например, 229-ВО-304SS-6" 2,5" C')
    class Meta:
        verbose_name = 'Сварочные соединения - Линия'
        verbose_name_plural = 'Сварочные соединения - Линии'
        #default_permissions = []
        unique_together = ('name', 'titul',)

class LineFile(models.Model):
    """Файлы для линии, например, изометрическая схема,
       либо изображение
    """
    line = models.ForeignKey(Line,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Линия, например, 677-А2-LT-150')
    file = models.ForeignKey(Files,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Файл для линии')
    position = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Позиция файла')

class Joint(Standard):
    """Стык, например, 26А"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    line = models.ForeignKey(Line,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Номер линии, например, 913A')
    class Meta:
        verbose_name = 'Сварочные соединения - Стык'
        verbose_name_plural = 'Сварочные соединения - Стыки'
        #default_permissions = []
        unique_together = ('name', 'line',)
