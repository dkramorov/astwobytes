# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.string_parser import kill_quotes
from apps.main_functions.models import Standard
from apps.addresses.models import Address
from apps.flatcontent.models import Blocks


class MainCompany(Standard):
    """Сущность для группы компаний
    """
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    tag = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    resume = models.TextField(blank=True, null=True)

class MainCompany2Category(models.Model):
    """Связка группы компаний с категориями"""
    main_company = models.ForeignKey(MainCompany, blank=True, null=True, on_delete=models.CASCADE)
    cat = models.ForeignKey(Blocks, blank=True, null=True, on_delete=models.CASCADE)

class Company(Standard):
    """Компания, по сути это филиал компании
       может быть головной офис
    """
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    tag = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    site = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    email = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    twitter = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    facebook = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    instagram = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    phone = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    main_company = models.ForeignKey(MainCompany, blank=True, null=True,
        verbose_name='Родительская компания группы филиалов', on_delete=models.SET_NULL)
    address = models.ForeignKey(Address, blank=True, null=True,
        verbose_name='Адрес', on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Компании - филиал'
        verbose_name_plural = 'Компании - филиалы'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = kill_quotes(self.phone, 'int')
        super(Company, self).save(*args, **kwargs)

class Company2Category(models.Model):
    """Связка филиалов с категориями"""
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE)
    cat = models.ForeignKey(Blocks, blank=True, null=True, on_delete=models.CASCADE)

class Contact(Standard):
    """Контакты компаний, пока только телефоны"""
    ctype_choices = (
        (1, 'phone'),
        (2, 'site'),
        (3, 'email'),
        (4, 'twitter'),
        (5, 'facebook'),
        (6, 'instagram'),
    )
    main_company = models.ForeignKey(MainCompany,
        blank=True, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(Company,
        blank=True, null=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Значение в человеческом виде')
    indexed_value = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Значение для индексации')
    ctype = models.IntegerField(choices=ctype_choices,
        blank=True, null=True, db_index=True)
    comment = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Комментарий к телефону')

    def save(self, *args, **kwargs):
        if self.ctype == 1 and self.value:
            self.indexed_value = kill_quotes(self.value, 'int')
        else:
            self.indexed_value = self.value
        super(Contact, self).save(*args, **kwargs)
