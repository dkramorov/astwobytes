# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard
from apps.files.models import Files
from apps.weld.enums import (WELDING_TYPES,
                             MATERIALS,
                             JOIN_TYPES, )


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
        verbose_name='Наименование сооружаемого объекта, например, Усть-Кутская газофракционирующая установка')
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
    # Шифр НЕ используется для нумерации документов,
    # он используется для вывода формах PDF заключений
    code = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Шифр титула')
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
    project_joint_count = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Кол-во стыков по проекту')
    project_dinc = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=9, decimal_places=2,
        verbose_name='D-inc по проекту')

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
    complete_dinc = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=9, decimal_places=2,
        verbose_name='Выполнено D-inc')

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

    def get_files(self):
        """Получить файлы в виде списка"""
        files = self.linefile_set.select_related('file').all()
        return [{
            'id': item.id,
            'path': item.file.path,
            'name': item.file.name,
            'mime': item.file.mime,
            'folder': item.file.get_folder(),
        } for item in files]


class LineFile(models.Model):
    """Файлы для линий, например,
       изометрическая схема, либо изображение
    """
    line = models.ForeignKey(Line,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Линия')
    file = models.ForeignKey(Files,
        blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Файл для линии')
    position = models.IntegerField(blank=True, null=True, db_index=True,
        verbose_name='Позиция файла')

    class Meta:
        verbose_name = 'Структура - Файл для линии'
        verbose_name_plural = 'Структура - Файлы для линий'
        #default_permissions = []

    def delete(self, *args, **kwargs):
        """Переопределяем метод удаления,
           надо похерить файл, который привязан"""
        if self.file:
            self.file.delete()
        super(LineFile, self).delete(*args, **kwargs)

class Joint(Standard):
    """Стык, например, 26А"""
    # Вид сварного соединения
    welding_conn_view_choices = (
        (1, 'С17'),
        (2, 'У19'),
        (3, 'У20'),
        (4, 'С17/У20'),
        (5, 'У18'),
    )
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    line = models.ForeignKey(Line,
        blank=True, null=True, on_delete=models.SET_NULL,
        verbose_name='Номер линии, например, 913A')
    diameter = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=9, decimal_places=2,
        verbose_name='Диаметр в мм, например, 355.6')
    side_thickness = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=9, decimal_places=2,
        verbose_name='Толщина стенки, например, 4,78')
    welding_type = models.IntegerField(choices=WELDING_TYPES,
        blank=True, null=True, db_index=True,
        verbose_name='Тип сварки, например, РД')
    material = models.IntegerField(choices=MATERIALS,
        blank=True, null=True, db_index=True,
        verbose_name='Материал - сталь, например, 09Г2С')
    join_type_from = models.IntegerField(choices=JOIN_TYPES,
        blank=True, null=True, db_index=True,
        verbose_name='Свариваемые элементы, например, тройник/переходник')
    join_type_to = models.IntegerField(choices=JOIN_TYPES,
        blank=True, null=True, db_index=True,
        verbose_name='Свариваемые элементы, например, тройник/труба')
    welding_conn_view = models.IntegerField(choices=welding_conn_view_choices,
        blank=True, null=True, db_index=True,
        verbose_name='Вид сварного соединения, например, C17')
    dinc = models.DecimalField(blank=True, null=True, db_index=True,
        max_digits=9, decimal_places=2,
        verbose_name='D-inc, например, 6.30, нужен для отчетов, рассчитывается динамически, например, диаметр(160)/константа(25.4)=6.30')
    welding_date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата сварки, например, 12.03.2020')

    class Meta:
        verbose_name = 'Структура - Стык'
        verbose_name_plural = 'Структура - Стыки'
        #default_permissions = []
        unique_together = ('name', 'line',)

    def save(self, *args, **kwargs):
        exist = self.id
        self.dinc = None
        if self.diameter:
            try:
                self.dinc = float(self.diameter) / 25.4
            except ValueError:
                pass
        super(Joint, self).save(*args, **kwargs)
        # Обновляем номер заявки, если она есть
        if exist and hasattr(self, 'welding_joint'):
            self.welding_joint.update_request_number()

    def get_welders(self):
        """Получить сварщиков по стыку"""
        if not self.id:
            return {}
        result = {}
        welders = self.jointwelder_set.select_related('welder').all()
        for welder in welders:
            result[welder.position] = welder.welder
        return result

