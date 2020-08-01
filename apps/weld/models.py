# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.weld.enums import WELDING_TYPES, MATERIALS, JOIN_TYPES
from apps.weld.welder_model import Welder
from apps.weld.company_model import Company, Titul, Base, Line, Joint

class WeldingJoint(Standard):
    """Заявки на стыки"""
    # Смена
    workshift_choices = (
        (1, '1'),
        (2, '2'),
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
    )
    # Вид сварного соединения
    welding_conn_view_choices = (
        (1, 'С17'),
        (2, 'У19'),
        (3, 'У20'),
        (4, 'С17/У20'),
    )
    # Категория
    category_choices = (
        (1, 'I'),
        (2, 'II'),
        (3, 'III'),
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
    # Номер ремонта
    repair_choices = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
    )
    state_choices = (
        (1, 'Новый стык'),
        (2, 'В работе'),
        (3, 'Готовый стык'),
        (4, 'В ремонте'),
    )

    titul = models.ForeignKey(Titul,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Титул, например, У101')
    joint = models.ForeignKey(Joint,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Номер стыка, например, 26А')
    repair = models.IntegerField(choices=repair_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Ремонт, например, 2 (второй ремонт)')
    cutout = models.BooleanField(blank=True, null=True, db_index=True,
        verbose_name='Вырез')
    diameter = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=9, decimal_places=2,
        verbose_name='Диаметр в мм, например, 355.6')
    side_thickness = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=9, decimal_places=2,
        verbose_name='Толщина стенки, например, 4,78')
    material = models.IntegerField(choices=MATERIALS,
        blank=True, null=True, db_index=True,
        verbose_name='Материал - сталь, например, 09Г2С')
    join_type_from = models.IntegerField(choices=JOIN_TYPES,
        blank=True, null=True, db_index=True,
        verbose_name='Свариваемые элементы, например, тройник/переходник')
    join_type_to = models.IntegerField(choices=JOIN_TYPES,
        blank=True, null=True, db_index=True,
        verbose_name='Свариваемые элементы, например, тройник/труба')
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
    welding_type = models.IntegerField(choices=WELDING_TYPES,
        blank=True, null=True, db_index=True,
        verbose_name='Тип сварки, например, РД')
    category = models.IntegerField(choices=category_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Категория, например I')
    control_result = models.IntegerField(choices=control_result_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Результат контроля, например, Вырезать')
    conclusion_number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер заключения, например, ТПС-БНТК-1 ТХ-18-875-РК-23')
    conclusion_date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата заключения, например, 3/29/20')
    notice = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Примечание, например, только Вик')
    #dinc = models.DecimalField(blank=True, null=True, db_index=True,
    #    max_digits=9, decimal_places=2,
    #    verbose_name='D-inc, например, 6.30, нужен для отчетов, рассчитывается динамически, например, диаметр(160)/константа(25.4)=6.30')
    state = models.IntegerField(choices=state_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Статус заявки, например, в работе')

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
        verbose_name='Заявка на стык')
    actually = models.BooleanField(blank=True, null=True, db_index=True,
        verbose_name='Фактический сварщик (тот, кто проводит работы), другие сващики могут быть указаны в заявках, потому что у фактических нет допуска')

    class Meta:
        verbose_name = 'Сварочные соединения - Сварщик стыка'
        verbose_name_plural = 'Сварочные соединения - Сварщики стыков'
        default_permissions = []
