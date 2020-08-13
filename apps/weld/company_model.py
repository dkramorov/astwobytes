# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

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
       например, ООО "Транспромстрой"
    """
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Компания, наименование предприятия-заказчика, например, ООО "Транспромстрой"')
    customer = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Компания, наименование предприятия-заказчика, например, ООО "ИНК"')
    location = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Место строительства предприятия, например, Ярактикинское НГКМ')
    # подрядчик
    contractor = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Наименование генподрядной и строительной организации и ее ведомственная принадлежность, например, АО "Хоневелл"')
    # монтажник
    fitter = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Наименование монтажной организации, например, ООО "Транспромстрой"')
    code = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Код компании, например, ТПС')

    class Meta:
        verbose_name = 'Структура - Компания'
        verbose_name_plural = 'Структура - Компании'
        #default_permissions = []

class Subject(Standard):
    """Объект,
       второй уровень иерархии,
       например, ГФУ
    """
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Наименование сооружаемого объекта, например, ')
    code = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Код объекта, например, ГФУ')
    company = models.ForeignKey(Company,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Комания (объект), например ТПС')
    class Meta:
        verbose_name = 'Структура - Объект'
        verbose_name_plural = 'Структура - Объекты'
        #default_permissions = []
        unique_together = ('code', 'company',)

class Titul(Standard):
    """Титул, например, У800"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Часть объекта, например, У800')
    description = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Описание титула, например, Отделение печей нагрева')
    subject = models.ForeignKey(Subject,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Объект, например ТПС-ГФУ')
    class Meta:
        verbose_name = 'Структура - Титул'
        verbose_name_plural = 'Структура - Титулы'
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
        verbose_name = 'Структура - Установка'
        verbose_name_plural = 'Структура - Установки'
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
    # Изменение статуса заявки на стык
    # должно вызывать изменение этих значений
    # Нужно иметь возможность полностью пересчитать их
    new_joints = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Количество новых заявок на стык')
    in_progress_joints = models.IntegerField(blank=True, null=True,
        db_index=True,
        verbose_name='Количество заявок на стык, находящихся в работе у лаборатории')
    repair_joints = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Количество заявок на стык на ремонт')
    complete_joints = models.IntegerField(blank=True, null=True,
        db_index=True,
        verbose_name='Количество выполненных заявок на стык')

    class Meta:
        verbose_name = 'Структура - Линия'
        verbose_name_plural = 'Структура - Линии'
        #default_permissions = []
        unique_together = ('name', 'titul',)

    def get_total_joints(self):
        """Получить общее кол-во стыков"""
        result = 0
        if self.new_joints:
            result += self.new_joints
        if self.in_progress_joints:
            result += self.in_progress_joints
        if self.repair_joints:
            result += self.repair_joints
        if self.complete_joints:
            result += self.complete_joints
        return result

class Joint(Standard):
    """Стык, например, 26А"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    line = models.ForeignKey(Line,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Номер линии, например, 913A')
    class Meta:
        verbose_name = 'Структура - Стык'
        verbose_name_plural = 'Структура - Стыки'
        #default_permissions = []
        unique_together = ('name', 'line',)
