# -*- coding: utf-8 -*-
import json
from django.db import models

from apps.main_functions.models import Standard
from apps.net_tools.models import IPAddress

from apps.site.miners.whatsminer import WhatsMinerApi

class Comp(Standard):
    """Компутеры"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    ip = models.ForeignKey(IPAddress, blank=True, null=True, on_delete=models.SET_NULL)
    api_enabled = models.BooleanField(default=False, db_index=True,
        verbose_name='Включено ли апи')
    token_data = models.CharField(max_length=255,
        blank=True, null=True)
    pcb_sn = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Miners - Компьютер'
        verbose_name_plural = 'Miners - Компьютеры'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def get_token_data(self):
        if self.token_data:
            return json.loads(self.token_data)
        return {}

    def set_token_data(self, token_data):
        self.token_data = json.dumps(self.token_data)
        Comp.objects.filter(pk=self.id).update(token_data=self.token_data)

    def check_authorization_helper(self, token_data: dict = None):
        result = {}
        result['new'] = True
        if token_data:
            result['new'] = False
        api = WhatsMinerApi(ip=self.ip.ip, passwd='admin', token_data=token_data)
        auth = api.authorization()
        set_zone = api.set_zone()
        result['set_zone'] = set_zone
        status = set_zone.get('STATUS')
        if (status == 'E'):
            result['error'] = set_zone.get('Msg')
        elif (status == 'S'):
            result['auth'] = auth
            if auth.get('salt') and auth.get('newsalt'):
                self.token_data = json.dumps(auth)
                Comp.objects.filter(pk=self.id).update(token_data=self.token_data)
        return result

    def check_authorization(self):
        if not self.ip or not self.ip.ip:
            assert False
        token_data = self.get_token_data()
        result = self.check_authorization_helper(token_data)
        if result.get('set_zone', {}).get('Code') in (135, ):
            prev_set_zone = result['set_zone']
            result = self.check_authorization_helper()
            result['prev_set_zone'] = prev_set_zone
            result['prev_token_data'] = token_data
        return result

    def save(self, *args, **kwargs):
        super(Comp, self).save(*args, **kwargs)

