# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.weld.enums import WELDING_TYPES, MATERIALS
from apps.weld.company_model import Subject

class Welder(Standard):
    """Сварщики"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    stigma = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Клеймо, например, 9SZN')
    notice = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Примечание, например, нет закл. ВИК, РК, ДЛ')
    subject = models.ForeignKey(Subject,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Находится на объекте, например, ГФУ')
    # is_active - уволен/не уволен
    class Meta:
        verbose_name = 'Сварщики - Сварщик'
        verbose_name_plural = 'Сварщики - Сварщики'
        #default_permissions = []

class Defectoscopist(Standard):
    """Дефектоскописты"""
    state_choices = (
        (1, 'Начальник лаборатории'),
        (2, 'Дефектоскопист'),
        (3, 'Ведущий специалист ЛНК'),
    )
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Полное имя, например, Проскоков Никита Владимирович')
    stigma = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер удостоверения, например, 0048-1962')
    notice = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Примечание')
    state = models.IntegerField(choices=state_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Должность')
    # is_active - уволен/не уволен
    class Meta:
        verbose_name = 'Контроль - Дефектоскопист'
        verbose_name_plural = 'Контроль - Дефектоскописты'
        #default_permissions = []

class LetterOfGuarantee(Standard):
    """Гарантийные письма на сварщиков"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Гарантийное письмо на сварщика, например, №38УК/093-19 от 18.11.19г о сроках проведения мех.испытаний до 25.02.20')
    letter = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Путь до файла с самим письмом')
    welder = models.ForeignKey(Welder,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Сварщик')

    class Meta:
        verbose_name = 'Сварщики - Гарантийное письмо'
        verbose_name_plural = 'Сварщики - Гарантийные письма'
        #default_permissions = []

class Vik(Standard):
    """Акт ВИК (vik)"""
    number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер, например, 2226 или D/5')
    date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата для номера, например, 20/10/2018')
    welder = models.ForeignKey(Welder,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Сварщик')

    class Meta:
        verbose_name = 'Сварщики - Акт ВИК'
        verbose_name_plural = 'Сварщики - Акты ВИК'
        #default_permissions = []

class ControlK(Standard):
    """УЗК/РК (control)"""
    number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='УЗК/РК номер, например, 13-РК')
    date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата для УЗК/РК номера, например, 10/20/2018')
    welder = models.ForeignKey(Welder,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Сварщик')

    class Meta:
        verbose_name = 'Сварщики - УЗК/РК контроль'
        verbose_name_plural = 'Сварщики - УЗК/РК контроль'
        #default_permissions = []

class HoldingKSS(Standard):
    """Проведение КСС (holding)"""
    # TT/MK
    holding_choices = (
        (1, 'ТТ / МК'),
        (2, 'МК'),
        (3, 'ТТ'),
        (4, 'Уволен'),
        (5, 'Увольняется'),
        (6, 'Уехал'),
    )
    spent_length_choices = (
        (1, 0.3),
    )
    standard_size = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Типоразмер, например, 100х300')
    material = models.IntegerField(choices=MATERIALS,
        blank=True, null=True, db_index=True,
        verbose_name='Материал - сталь, например, 12Х18Н10Т')
    spent_length = models.IntegerField(choices=spent_length_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Затрачиваемая длина 150мм*2, например, 0.3')
    number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер КСС, например, КСС-2226/1')
    state = models.IntegerField(choices=holding_choices,
        blank=True, null=True, db_index=True,
        verbose_name='ТТ/МК, например, ТТ')
    welder = models.ForeignKey(Welder,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Сварщик')

    class Meta:
        verbose_name = 'Сварщики - Проведение КСС'
        verbose_name_plural = 'Сварщики - Проведения КСС'
        #default_permissions = []

class MechTest(Standard):
    """Мехиспытание (mechtest)"""
    number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер для мехиспытания, например, 6/2-ТПС')
    date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата для мехиспытания, например, 29/10/18')
    welder = models.ForeignKey(Welder,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Сварщик')

    class Meta:
        verbose_name = 'Сварщики - Мехиспытание'
        verbose_name_plural = 'Сварщики - Мехиспытания'
        #default_permissions = []

class AdmissionSheet(Standard):
    # Допускной лист (admission)
    number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер для допускного листа, например, 17-18')
    date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата для допускного листа, например, 30/10/18')
    welder = models.ForeignKey(Welder,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Сварщик')

    class Meta:
        verbose_name = 'Сварщики - Лист допуска'
        verbose_name_plural = 'Сварщики - Листы допуска'
        #default_permissions = []

class NAX(Standard):
    """Номер НАКС (nax)
       Аттестат"""
    identification_choices = (
        (1, 'офис Иркутск'),
    )
    number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер удостоверения, например, ВСР-1ГАЦ-I-08121')
    best_before = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='НАКС годен до, например, 27/04/20')
    welding_type = models.IntegerField(choices=WELDING_TYPES,
        blank=True, null=True, db_index=True,
        verbose_name='Тип сварки, например, РД')
    half_year_mark = models.BooleanField(blank=True, null=True,
        db_index=True, default=False,
        verbose_name='Полугодовая отметка, например, есть')
    identification = models.IntegerField(choices=identification_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Место идентификации, например, офис Иркутск')
    # НГДО - нефтегазодобывающее оборудование (3,4,5,12)
    # СК - стальные конструкции (листы, металлические трубы) (1,3)
    acl = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Допуск')
    welder = models.ForeignKey(Welder,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Сварщик')

    class Meta:
        verbose_name = 'Сварщики - Аттестат (НАКС)'
        verbose_name_plural = 'Сварщики - Аттестаты (НАКС)'
        #default_permissions = []

