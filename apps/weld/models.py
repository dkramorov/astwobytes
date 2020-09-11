# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import User

from apps.main_functions.models import Standard
from apps.weld.enums import (WELDING_TYPES,
                             MATERIALS,
                             JOIN_TYPES,
                             WELDING_JOINT_STATES,
                             WELDING_TYPE_DESCRIPTIONS,
                             CONCLUSION_STATES, )
from apps.weld.welder_model import Welder
from apps.weld.company_model import Company, Titul, Base, Line, Joint
from apps.files.models import Files

class WeldingJoint(Standard):
    """Заявки на стыки"""
    # Смена
    workshift_choices = (
        (1, '1'),
        (2, '2'),
    )
    # Вид контроля
    control_choices = (
        (1, 'РК'), # Радиографический контроль
        (2, 'УЗК'), # Ультразвуковой контроль
        (3, 'ВИК'), # Визуально-измерительный контроль
        (4, 'РК-ВИК'),
        (5, 'УК'),
        (6, 'УЗК-ЦД'),
        (7, 'РК-УЗК'),
        (8, 'РК-УЗК-ЦД'),
        (9, 'ПВК'), # Капиллярный метод проверки
        (10, 'МК'), # Магнитный контроль
        (11, 'ВК'), # Входной контроль
        (12, 'СР'), # Скрытые работы
    )
    # Вид сварного соединения
    welding_conn_view_choices = (
        (1, 'С17'),
        (2, 'У19'),
        (3, 'У20'),
        (4, 'С17/У20'),
        (5, 'У18'),
    )
    # Категория
    category_choices = (
        (1, 'I'),
        (2, 'II'),
        (3, 'III'),
    )
    # Номер ремонта
    repair_choices = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
    )
    joint = models.OneToOneField(Joint,
        blank=True, null=True, on_delete=models.SET_NULL,
        related_name='welding_joint',
        verbose_name='Номер стыка, например, 26А')
    repair = models.IntegerField(choices=repair_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Ремонт, например, 2 (второй ремонт)')
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
    control_result = models.IntegerField(choices=CONCLUSION_STATES,
        blank=True, null=True, db_index=True,
        verbose_name='Результат контроля, например, Вырезать')
    notice = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Примечание, например, только ВИК')
    dinc = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=9, decimal_places=2,
        verbose_name='D-inc, например, 6.30, нужен для отчетов, рассчитывается динамически, например, диаметр(160)/константа(25.4)=6.30')
    state = models.IntegerField(choices=WELDING_JOINT_STATES,
        blank=True, null=True, db_index=True,
        verbose_name='Статус заявки, например, в работе')
    requester = models.ForeignKey(User, related_name='requester',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Заявку подал')
    receiver = models.ForeignKey(User, related_name='receiver',
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Заявку принял')

    class Meta:
        verbose_name = 'Сварочное соединение - Бланк-заявка'
        verbose_name_plural = 'Сварочные соединения - Бланк-заявки'
        permissions = (
            ('in_progress', 'Просмотр заявок в работе'),
            ('repair', 'Просмотр заявок в ремонте'),
        )
        #default_permissions = []

    def save(self, *args, **kwargs):
        self.dinc = None
        if self.diameter:
            try:
                self.dinc = float(self.diameter) / 25.4
            except ValueError:
                pass
        super(WeldingJoint, self).save(*args, **kwargs)
        self.request_number = self.update_request_number()

    def update_request_number(self):
        """Обновление номера заявки"""
        if not self.id:
            return
        request_number = ''
        obj = WeldingJoint.objects.select_related(
            'joint',
            'joint__line',
            'joint__line__base',
            'joint__line__titul',
            'joint__line__titul__subject',
            'joint__line__titul__subject__company',
        ).filter(pk=self.id).only(
            'joint__line__titul__subject__company__code',
            'joint__line__titul__subject__code',
            'joint__line__titul__name',
            'joint__line__base__name',
            'joint__line__name',
            'joint__name',
        ).first()
        if obj.joint and obj.joint.line and obj.joint.line.titul and obj.joint.line.titul.subject and obj.joint.line.titul.subject.company:
            repair = ''
            if self.repair:
                repair = 'р%s' % self.repair
            request_number = '%s%s-%s-%s-%s-%s-%s' % (
                obj.joint.name or '',
                repair,
                obj.joint.line.titul.subject.company.code or '',
                obj.joint.line.titul.subject.code or '',
                obj.joint.line.titul.name or '',
                obj.joint.line.name or '',
                obj.get_control_type_display() or '',
            )
            #print('numbers {} and {}'.format(self.request_number, request_number))
            if not self.request_number == request_number:
                WeldingJoint.objects.filter(pk=self.id).update(request_number=request_number)
        return request_number

    def get_files(self):
        """Получить файлы в виде списка"""
        files = self.weldingjointfile_set.select_related('file').all()
        return [{
            'id': item.id,
            'path': item.file.path,
            'name': item.file.name,
            'mime': item.file.mime,
            'folder': item.file.get_folder(),
        } for item in files]

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
    actually = models.BooleanField(blank=True, null=True,
        db_index=True, default=False,
        verbose_name='Фактический сварщик (тот, кто проводит работы), другие сващики могут быть указаны в заявках, потому что у фактических нет допуска')
    position = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Позиция (от 1 до 4)')

    class Meta:
        verbose_name = 'Сварочные соединения - Сварщик стыка'
        verbose_name_plural = 'Сварочные соединения - Сварщики стыков'
        default_permissions = []

class WeldingJointFile(models.Model):
    """Файлы для заявок на стык, например,
       изометрическая схема, либо изображение
    """
    welding_joint = models.ForeignKey(WeldingJoint,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Заявка на стык')
    file = models.ForeignKey(Files,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Файл для заявки на стык')
    position = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Позиция файла')

    class Meta:
        verbose_name = 'Сварочные соединения - Файл заявки на стык'
        verbose_name_plural = 'Сварочные соединения - Файлы заявок на стык'
        #default_permissions = []

    def delete(self, *args, **kwargs):
        """Переопределяем метод удаления,
           надо похерить файл, который привязан"""
        if self.file:
            self.file.delete()
        super(WeldingJointFile, self).delete(*args, **kwargs)

class WeldingJointState(models.Model):
    """Смена статуса заявки, так как для этого
       нужны специальные права,
       а также логирование
    """
    welding_joint = models.ForeignKey(WeldingJoint,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Заявка на стык')
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name='Пользователь, сменивший статус')
    date = models.DateTimeField(blank=True, null=True, db_index=True,
        auto_now_add=True, verbose_name='Время смены статуса')
    from_state = models.IntegerField(choices=WELDING_JOINT_STATES,
        blank=True, null=True, db_index=True,
        verbose_name='Статус заявки, например, в работе')
    to_state = models.IntegerField(choices=WELDING_JOINT_STATES,
        blank=True, null=True, db_index=True,
        verbose_name='Статус заявки, например, в работе')

    class Meta:
        verbose_name = 'Сварочные соединения - Смена статуса заявки на стык'
        verbose_name_plural = 'Сварочные соединения - Смена статусов заявкок на стыки'
        permissions = (
            ('repair_completed', 'Смена статуса - Ремонт выполнен'),
        )
        #default_permissions = []

def recalc_joints(line: Line):
    """Пересчет количества заявок на линии
       процент готовности линии
    """
    result = {
        'new_joints': {'state': 1, 'count': 0},
        'in_progress_joints': {'state': 2, 'count': 0},
        'repair_joints': {'state': 4, 'count': 0},
        'complete_joints': {'state': 3, 'count': 0},
    }
    query = WeldingJoint.objects.filter(joint__line=line)
    for key, value in result.items():
        result[key]['count'] = query.filter(state=value['state']).aggregate(models.Count('id'))['id__count']
    params = {key: value['count'] for key, value in result.items()}
    Line.objects.filter(pk=line.id).update(**params)
