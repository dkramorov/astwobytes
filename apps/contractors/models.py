# -*- coding: utf-8 -*-
from django.db import models

from apps.addresses.models import Address
from apps.main_functions.models import Standard

class Contractor(Standard):
    """Контрагенты
       Контрагентом называют обычно одну из сторон договора
    """
    ctype_choices = (
        (1, 'Физическое лицо'),
        (2, 'Индивидуальный предприниматель'),
        (3, 'Юридическое лицо'),
    )
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Наименование контрагента')
    code = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Код контрагента')
    phone = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Телефон контрагента')
    email = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Email контрагента')
    address = models.ForeignKey(Address,
        blank=True, null=True, on_delete=models.SET_NULL,
        related_name='address',
        verbose_name='Физический адрес контрагента')
    legal_address = models.ForeignKey(Address,
        blank=True, null=True, on_delete=models.SET_NULL,
        related_name='legal_address',
        verbose_name='Юридический адрес контрагента')
    ctype = models.IntegerField(blank=True, null=True, db_index=True,
        choices=ctype_choices,
        verbose_name='Тип контрагента')
    # Реквизиты юридического лица
    company_name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Наименование компании')
    inn = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='ИНН')
    kpp = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='КПП контрагента')
    # Для индивидуального предпринимателя здесь заполняем
    # ОГРНИП
    ogrn = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='ОГРН контрагента')
    okpo = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='ОКПО контрагента')
    # Расчетчный счет
    bik = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='БИК')
    bank = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Банк')
    bank_address = models.ForeignKey(Address,
        blank=True, null=True, on_delete=models.SET_NULL,
        related_name='bank_address',
        verbose_name='Адрес банка')
    ks = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Корр. счет')
    rs = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Расчетный счет')
    # Индивидуальный предприниматель
    first_name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Имя')
    last_name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Фамилия')
    middle_name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Отчество')
    certificate_number = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Номер свидетельства')
    certificate_date = models.DateField(blank=True, null=True, db_index=True,
        verbose_name='Дата свидетельства')

    class Meta:
        verbose_name = 'Контрагенты - Контрагент'
        verbose_name_plural = 'Контрагенты - Контрагенты'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(Contractor, self).save(*args, **kwargs)

