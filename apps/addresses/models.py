# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

class Address(Standard):
    """Адреса объектов
       https://developer.here.com/rest-apis/documentation/geocoder/topics/resource-geocode.html
       country, state, county,
       city, district, subdistrict,
       street, houseNumber, postalCode,
       addressLines, additionalData
       place = место этого адреса (например, ТЦ Юбилейный)
    """
    postalCode = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    country = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    state = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    county = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    city = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    district = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    subdistrict = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    street = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    houseNumber = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    addressLines = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    additionalData = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    latitude = models.DecimalField(blank=True, null=True,
        max_digits=30, decimal_places=25, db_index=True)
    longitude = models.DecimalField(blank=True, null=True,
        max_digits=30, decimal_places=25, db_index=True)
    place = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Адреса - адрес объекта'
        verbose_name_plural = 'Адреса - адреса объектов'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def fix_decimal(self, digits):
        """Ибучий фикс на округления decimal,
           типа шлем 104.172018 =>
           в базу получаем 104.1720179999999942310751067
           нахуй нам такое надо?"""
        if not digits:
            return None
        float_str = str(digits)
        inta, decimal = float_str.split('.')
        digits = '%s.%s%s' % (inta, decimal, '0'*25)
        return digits

    def save(self, *args, **kwargs):
        self.latitude = self.fix_decimal(self.latitude)
        self.longitude = self.fix_decimal(self.longitude)
        super(Address, self).save(*args, **kwargs)

    def address_str(self):
        """Вывод адреса строкой"""
        result = ''
        for field in ('postalCode',
                      #'country', 'state', 'county',
                      'city', 'district', 'subdistrict',
                      'street', 'houseNumber', ):
            value = getattr(self, field)
            if value:
                if field.name == 'additionalData':
                    result += '(%s) ' % value
                else:
                    result += value
                    if not field.name == 'houseNumber':
                        result += ', '
                    else:
                        result += ' '
        return result


