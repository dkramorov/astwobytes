# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.weld.enums import WELDING_TYPE_DESCRIPTIONS, CONCLUSION_STATES
from apps.weld.models import WeldingJoint
from apps.weld.welder_model import Defectoscopist


class JointConclusion(Standard):
    """Заключения (акты) на заявки на сварку (стык)
    """
    pvk_control_choices = (
        (1, 'первичный'),
        (2, 'вторичный'),
    )
    welding_joint = models.ForeignKey(WeldingJoint,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Заявка на стык')
    date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата актов/заключений')
    welding_type = models.IntegerField(choices=WELDING_TYPE_DESCRIPTIONS,
        blank=True, null=True, db_index=True,
        verbose_name='Тип сварки, например, аргонодуговая')
    # -------
    # Акт ВИК
    # -------
    vik_active = models.BooleanField(blank=True, null=True, db_index=True,
        verbose_name='Проведен ВИК (показываем в таблице, что проведен)')
    vik_defects = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Выявленные дефекты ВИК')
    vik_controller = models.ForeignKey(Defectoscopist, related_name='vik_controller',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Пользователь, выполнивший контроль ВИК')
    vik_director = models.ForeignKey(Defectoscopist, related_name='vik_director',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Руководитель работ по визуальному и измерительному контролю')
    # -------------
    # РК Заключение
    # -------------
    rk_active = models.BooleanField(blank=True, null=True, db_index=True,
        verbose_name='Проведен РК (показываем в таблице, что проведен)')
    rk_defectoscopist1 = models.ForeignKey(Defectoscopist, related_name='rk_defectoscopist1',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Стык принял по внешнему виду дефектоскопист')
    rk_defectoscopist2 = models.ForeignKey(Defectoscopist, related_name='rk_defectoscopist2',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Контроль произвел дефектоскопист')
    rk_defectoscopist3 = models.ForeignKey(Defectoscopist, related_name='rk_defectoscopist3',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Заключение выдал дефектоскопист')
    # --------------
    # ПВК Заключение
    # --------------
    pvk_active = models.BooleanField(blank=True, null=True, db_index=True,
        verbose_name='Проведен ПВК (показываем в таблице, что проведен)')
    pvk_control_type = models.IntegerField(choices=pvk_control_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Вид контроля, например, вторичный')
    pvk_defects = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Выявленные дефекты ПВК')
    pvk_state = models.IntegerField(choices=CONCLUSION_STATES,
        blank=True, null=True, db_index=True,
        verbose_name='Оценка качества')
    pvk_director = models.ForeignKey(Defectoscopist, related_name='pvk_director',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Начальник ЛНК')
    pvk_defectoscopist = models.ForeignKey(Defectoscopist, related_name='pvk_defectoscopist',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Дефектоскопист')
    # --------------
    # УЗК Заключение
    # --------------
    uzk_active = models.BooleanField(blank=True, null=True, db_index=True,
        verbose_name='Проведен УЗК (показываем в таблице, что проведен)')
    uzk_ray_angle = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Угол ввода луча в градусах')
    uzk_sensitivity = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Условная чувствительность зарубка в мм')
    uzk_defects = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Выявленные дефекты УЗК')
    uzk_notice = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Примечание')
    uzk_state = models.IntegerField(choices=CONCLUSION_STATES,
        blank=True, null=True, db_index=True,
        verbose_name='Оценка качества')
    uzk_operator = models.ForeignKey(Defectoscopist, related_name='uzk_operator',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Оператор')
    uzk_defectoscopist1 = models.ForeignKey(Defectoscopist, related_name='uzk_defectoscopist1',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Стык принял по внешнему виду дефектоскопист')
    uzk_defectoscopist2 = models.ForeignKey(Defectoscopist, related_name='uzk_defectoscopist2',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Контроль произвел дефектоскопист')
    uzk_defectoscopist3 = models.ForeignKey(Defectoscopist, related_name='uzk_defectoscopist3',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Заключение выдал дефектоскопист')
    class Meta:
        verbose_name = 'Сварочные соединения - Заключение (акт) на стык'
        verbose_name_plural = 'Сварочные соединения - Заключения (акты) на стыки'
        #default_permissions = []

class RKFrames(Standard):
    """Снимки на РК контроль для РК заключения
    """
    joint_conclusion = models.ForeignKey(JointConclusion,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Акт/заключение по заявке на стык')
    number = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Номер снимка, координаты мерного пояса')
    sensitivity = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=6, decimal_places=2,
        verbose_name='Чувствительность снимка в мм или %') # 9000,00
    defects = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Выявленные дефекты')
    notice = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Примечание')
    state = models.IntegerField(choices=CONCLUSION_STATES,
        blank=True, null=True, db_index=True,
        verbose_name='Заключение')
    class Meta:
        verbose_name = 'Сварочные соединения - Снимок на РК заключение'
        verbose_name_plural = 'Сварочные соединения - Снимки на РК заключения'
        default_permissions = []
