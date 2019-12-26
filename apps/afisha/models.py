# -*- coding: utf-8 -*-
import os

from django.db import models

from apps.main_functions.string_parser import translit
from apps.main_functions.models import Standard

class Rubrics(Standard):
    """Рубрикатор мест"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    # tag = ссылка на донора irk.ru
    tag = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = 'Афиша - Рубрикатор мест'
        verbose_name_plural = 'Афиша - Рубрикатор мест'

class RGenres(Standard):
    """Рубрикатор жанров"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    altname = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    # tag = ссылка на донора irk.ru
    tag = models.CharField(max_length=255, blank=True, null=True, db_index=True)

    def find_genre_altname(self, z=0):
        if self.name:
            self.altname = translit(self.name)

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = 'Афиша - Жанры'
        verbose_name_plural = 'Афиша - Жанры'

class REvents(Standard):
    """События"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    # tag = ссылка на донора irk.ru
    tag = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    duration = models.CharField(max_length=255, blank=True, null=True, verbose_name="Продолжительность", db_index=True)
    label = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ограничение по возрасту", db_index=True)
    genre = models.CharField(max_length=255, blank=True, null=True, verbose_name="Жанр", db_index=True)
    rgenre = models.ForeignKey(RGenres, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Рубрика")
    country = models.CharField(max_length=255, blank=True, null=True, verbose_name="Страна производства")
    trailer = models.TextField(blank=True, null=True, verbose_name="Трейлер")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    producer = models.CharField(max_length=255, blank=True, null=True, verbose_name="Режиссер", db_index=True)
    actors = models.TextField(blank=True, null=True, verbose_name="Актеры")

    def __unicode__(self):
        return u"{}".format(self.name)

    class Meta:
        verbose_name = 'Афиша - События'
        verbose_name_plural = 'Афиша - События'

class Places(Standard):
    """Места (кинотеатры)"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    # tag = ссылка на донора irk.ru
    tag = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    address_str = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    phone_str = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    worktime_str = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    site_str = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    email_str = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    #branch = models.ForeignKey(Branches, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Привязка к филиалу")
    rubric = models.ForeignKey(Rubrics, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Привязка к рубрике")

    class Meta:
        verbose_name = 'Афиша - Места'
        verbose_name_plural = 'Афиша - Места'

class RSeances(Standard):
    """В каких местах, когда происходит событие"""
    place = models.ForeignKey(Places, blank=True, null=True, on_delete=models.SET_NULL,)
    event = models.ForeignKey(REvents, blank=True, null=True, on_delete=models.SET_NULL,)
    date = models.DateField(blank=True, null=True, db_index=True)
    hours = models.IntegerField(blank=True, null=True, db_index=True)
    minutes = models.IntegerField(blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Афиша - Сеансы'
        verbose_name_plural = 'Афиша - Сеансы'
