# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.weld.enums import WELDING_TYPES, MATERIALS
from apps.weld.company_model import Subject

class Welder(Standard):
    """Сварщики"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    first_name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    last_name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    middle_name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    stigma = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Клеймо, например, 9SZN')
    stigma2 = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Клеймо по приказу, например, 9SZN')
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

class Certification(Standard):
    """Удостоверения для сварщиков
       это Аттестаты НАКС"""
    welder = models.ForeignKey(Welder,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Сварщик')
    number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер удостоверения')
    welding_type = models.IntegerField(choices=WELDING_TYPES,
        blank=True, null=True, db_index=True,
        verbose_name='Способ сварки')
    best_before = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='НАКС годен до, например, 27/04/20')
    place = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Место удостоверения')
    class Meta:
        verbose_name = 'Сварщики - Удостоверение'
        verbose_name_plural = 'Сварщики - Удостоверения'

class CertSections(Standard):
    """Группы технических устройств опасных производственных объектов"""
    group_choices = (
        (1, 'ПАО "Транснефть"'),
        (2, 'ПАО "Газпром"'),
        (3, 'ГДО Горнодобывающее оборудование'),
        (4, 'ГО Газовое оборудование'),
        (5, 'КО Котельное оборудование'),
        (6, 'КСМ Конструкции стальных мостов'),
        (7, 'МО Металлургическое оборудование'),
        (8, 'НГДО Нефтегазодобывающее оборудование'),
        (9, 'ОТОГ Оборудование для транспортировки опасных грузов'),
        (10, 'ОХНВП Оборудование химических, нефтехимических, нефтеперерабатывающих и взрывопожароопасных производств'),
        (11, 'ПТО Подъемно-транспортное оборудование'),
        (12, 'СК Строительные конструкции'),
    )
    certification = models.ForeignKey(Certification,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Удостоверение сварщика')
    welder = models.ForeignKey(Welder,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Сварщик')
    group = models.IntegerField(choices=group_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Группы технических устройств опасных производственных объектов, например, "ПАО "Газпром" "')
    points = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Пункты технических устройств опасных производственных объектов, например, 1,3')
    class Meta:
        verbose_name = 'Сварщики - Тех. устройство'
        verbose_name_plural = 'Сварщики - Тех. устройства'
        default_permissions = []

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

class HoldingKSS(Standard):
    """Проведение КСС
       для каждого КСС ВИК, УЗК, РК можно заливать файлы
    """
    certification = models.ForeignKey(Certification,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Удостоверение, на которое проводим КСС')
    place = models.ForeignKey(Subject,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Место проведения КСС (объект)')
    number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер КСС, например, КСС-195/2')
    standard_size = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Типоразмер, например, 100х300')
    material = models.IntegerField(choices=MATERIALS,
        blank=True, null=True, db_index=True,
        verbose_name='Материал - сталь, например, 12Х18Н10Т')
    test_number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер акта ВИК или УЗК/РК, например, 931')
    test_date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата проведения ВИК или УЗК/РК)')
    with_rk = models.BooleanField(default=False,
        blank=True, null=True, db_index=True,
        verbose_name='Проведен РК')
    with_uzk = models.BooleanField(default=False,
        blank=True, null=True, db_index=True,
        verbose_name='Проведен УЗК')
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
