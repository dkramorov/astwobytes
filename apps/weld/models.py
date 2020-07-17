# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

class Base(Standard):
    """Установка"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Установка, например, БНТК-2 ТХ-18')
    class Meta:
        verbose_name = 'Сварочные соединения - Установка'
        verbose_name_plural = 'Сварочные соединения - Установки'
        #default_permissions = []

class Contract(Standard):
    """Договор"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Договор, например, UOP')
    class Meta:
        verbose_name = 'Сварочные соединения - Договор'
        verbose_name_plural = 'Сварочные соединения - Договоры'
        #default_permissions = []

class Titul(Standard):
    """Титул, например, У800"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    class Meta:
        verbose_name = 'Сварочные соединения - Титул'
        verbose_name_plural = 'Сварочные соединения - Титулы'
        #default_permissions = []

class Line(Standard):
    """Линия, например, 677-А2-LT-150"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    class Meta:
        verbose_name = 'Сварочные соединения - Линия'
        verbose_name_plural = 'Сварочные соединения - Линии'
        #default_permissions = []

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

class Scheme(Standard):
    """Схема,
       например, 229-ВО-304SS-6" 2,5" C
    """
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    class Meta:
        verbose_name = 'Сварочные соединения - Схема'
        verbose_name_plural = 'Сварочные соединения - Схемы'
        #default_permissions = []

class Material(Standard):
    """Материал, сталь,
       например, 09Г2С
    """
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    class Meta:
        verbose_name = 'Сварочные соединения - Материал (сталь)'
        verbose_name_plural = 'Сварочные соединения - Материалы (сталь)'
        #default_permissions = []

class JoinType(Standard):
    """Свариваемые элементы, например, трубы/отвод"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    class Meta:
        verbose_name = 'Сварочные соединения - Свариваемый элемент'
        verbose_name_plural = 'Сварочные соединения - Свариваемые элементы'
        #default_permissions = []

class Welder(Standard):
    """Сварщик, Сейтниязов"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    stigma = models.CharField(max_length=255,
        blank=True, null=True,
        verbose_name='Клеймо, например, 9SZN')
    class Meta:
        verbose_name = 'Сварочные соединения - Сварщик'
        verbose_name_plural = 'Сварочные соединения - Сварщики'
        #default_permissions = []

class Company(Standard):
    """Компания, на чьем балансе находятся работы,
       например, ООО "ИНК" или ЛНК
    """
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    class Meta:
        verbose_name = 'Сварочные соединения - Компания'
        verbose_name_plural = 'Сварочные соединения - Компании'
        #default_permissions = []

class WeldingJoint(Standard):
    """Сварочные соединения"""
    # Смена
    workshift_choices = (
        (1, '1'),
        (2, '2'),
        (3, '-'),
    )
    # Вид контроля
    control_choices = (
        (1, 'РК'),
        (2, 'УЗК'),
        (3, 'ВИК'),
        (4, 'РК-УЗК-ЦД'),
        (5, 'РК/УЗК'),
        (6, 'УК'),
        (7, 'ПВК'),
        (8, '*'),
    )
    # Вид сварного соединения
    welding_conn_view_choices = (
        (1, 'С17'),
        (2, 'У20'),
        (4, 'С17/У20'),
        (5, 'У19'),
    )
    # Тип сварки
    welding_type_choices = (
        (1, 'РАД'),
        (2, 'РД'),
        (3, 'РАД/РД'),
    )
    # Категория
    category_choices = (
        (1, 'I'),
        (2, 'II'),
        (3, 'III'),
        (4, '*'),
    )
    # Результат контроля
    control_result_choices = (
        (1, 'Вырезать'),
        (2, 'Годен'),
        (3, 'Ремонт'),
        (4, 'УЗК'),
        (5, 'Пересвет'),
        (6, 'Брак'),
    )
    base = models.ForeignKey(Base,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Установка, где размещен стык, например, БНТК-2 ТХ-18')
    contract = models.ForeignKey(Contract,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Договор, например, UOP')
    titul = models.ForeignKey(Titul,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Титул, например, У101')
    joint = models.ForeignKey(Joint,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Номер стыка, например, 26А')
    scheme = models.ForeignKey(Scheme,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Номер изом. схемы, например, 229-ВО-304SS-6" 2,5" C')
    repair = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Ремонт, например, 2 (второй ремонт)')
    cutout = models.BooleanField(blank=True, null=True, db_index=True,
        verbose_name='Вырез')
    diameter = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=9, decimal_places=2,
        verbose_name='Диаметр в мм, например, 355.6')
    side_thickness = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=9, decimal_places=2,
        verbose_name='Толщина стенки, например, 4,78')
    material = models.ForeignKey(Material,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Материал - сталь, например, 12Х18Н10Т')
    join_type = models.ForeignKey(JoinType,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Свариваемые элементы, например, тройник/переходник')
    welding_date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата сварки, например, 12.03.2020')
    workshift = models.IntegerField(choices=workshift_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Номер, смены, например, 1')
    request_number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер заявки на НК, например, ТПС-БНТК-1 ТХ-18-875-РК-23')
    request_control_date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата заявки на НК, например, 3/12/20')
    control_type = models.IntegerField(choices=control_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Вид контроля, например, РК')
    welding_conn_view = models.IntegerField(choices=welding_conn_view_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Вид сварного соединения, например, C17')
    welding_type = models.IntegerField(choices=welding_type_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Тип сварки, например, РД')
    category = models.IntegerField(choices=category_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Категория, например I')
    control_result = models.IntegerField(choices=control_result_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Результат контроля, например, Вырезать')
    #company = models.ForeignKey(Company,
    #    blank=True, null=True, on_delete=models.SET_NULL,
    #    verbose_name='На чьем балансе, например, ЛНК')
    conclusion_number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер заключения, например, ТПС-БНТК-1 ТХ-18-875-РК-23')
    conclusion_date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата заключения, например, 3/29/20')
    notice = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Примечание, например, только Вик')
    dinc = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=17, decimal_places=15,
        verbose_name='D-inc на человека или стык, например, 10,748031496063')

    class Meta:
        verbose_name = 'Сварочное соединение - Бланк-заявка'
        verbose_name_plural = 'Сварочные соединения - Бланк-заявки'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(WeldingJoint, self).save(*args, **kwargs)

class JointWelder(models.Model):
    """Сварщики, которые назначены на стык
       WeldingJoint могут варить несколько сварщиков,
       например, Сейтниязов + Бедиров Ш
    """
    welder = models.ForeignKey(Welder,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Сварщик')
    welding_joint = models.ForeignKey(WeldingJoint,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Сварочное соединение')

    class Meta:
        verbose_name = 'Сварочные соединения - Сварщик стыка'
        verbose_name_plural = 'Сварочные соединения - Сварщики стыков'
        default_permissions = []
