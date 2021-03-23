# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.string_parser import kill_quotes, get_request_ip
from apps.main_functions.models import Standard
from apps.main_functions.functions import object_fields
from apps.personal.utils import get_user_name

class Shopper(Standard):
    """Модель пользователя сайта"""
    oauth_choices = (
        (1, 'обычная авторизация'),
        (2, 'vk'),
        (3, 'yandex'),
    )
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    first_name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    last_name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    email = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    phone = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    phone_confirmed = models.BooleanField(db_index=True,
        default=False,
        verbose_name='Телефон подтвержден')
    address = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    login = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    passwd = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    oauth = models.IntegerField(choices=oauth_choices, blank=True, null=True, db_index=True)
    discount = models.IntegerField(blank=True, null=True, db_index=True, verbose_name='Персональная скидка')
    balance = models.DecimalField(blank=True, null=True, max_digits=13, decimal_places=2, db_index=True, verbose_name='Баланс пользователя') # 99 000 000 000,00
    ip = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='ip адрес пользователя')

    def __str__(self):
        return get_user_name(self)

    def to_dict(self):
        return object_fields(self, only_fields=(
            'id',
            'name',
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'phone',
            'phone_confirmed',
            'address',
            'login',
            'discount',
            'balance',
            'ip',
        ))

    class Meta:
        verbose_name = 'Пользователи - пользователь'
        verbose_name_plural = 'Пользователи - пользователи'
        #permissions = (
        #    ('view_shopper', 'Просмотр пользователей'),
        #    ('create_shopper', 'Создание пользователей'),
        #    ('edit_shopper', 'Редактирование пользователей'),
        #    ('drop_shopper', 'Удаление пользователей'),
        #)

    def save(self, *args, **kwargs):
        if self.phone:
            phone = kill_quotes(self.phone, 'int')
            self.phone = phone
        super(Shopper, self).save(*args, **kwargs)

def get_personal_user(request, guest_enter: bool = False):
    """Пользователь из сессии
       :param request: HttpRequest
       :param guest_enter: гостевой вход (завести виртуального юзера)
       :return: Shopper, не надо возвращать dict
    """
    shopper = request.session.get('shopper')
    promocode = request.session.get('promocode')
    if not guest_enter:
        if isinstance(shopper, dict):
            user = Shopper()
            for k, v in shopper.items():
                setattr(user, k, v)
            if promocode:
                user.promocode = promocode
            return user
        if shopper:
            shopper.promocode = promocode
        return shopper

    # Создаем виртуального пользователя
    ip = get_request_ip(request)
    if not shopper:
        shopper = Shopper(name='Гость', ip=ip)
        request.session['shopper'] = shopper.to_dict()
    else:
        shopper = Shopper.objects.filter(pk=shopper.id).first()
        if not shopper:
            shopper = Shopper(name='Гость', ip=ip)
            request.session['shopper'] = shopper.to_dict()
    shopper.promocode = promocode
    return shopper