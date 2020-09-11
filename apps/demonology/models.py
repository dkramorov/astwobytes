# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

from apps.main_functions.models import Standard
from . services import create_daemon, drop_daemon

class Daemon(Standard):
    """Создание скрипта для системного демона"""
    exec_choices = (
        ('binary_com/binary_bot.py', 'Бинарные опционы'),
        ('spamcha/sms_hub.py', 'Телефоны для смс'),
    )
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    api_url = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    token = models.CharField(max_length=255, blank=True, null=True, db_index=True, verbose_name='Параметры для запуска: args')
    exec_path = models.CharField(choices=exec_choices, max_length=255, blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Сервисы - Демон'
        verbose_name_plural = 'Сервисы - Демон'

    def get_name(self):
        return 'daemon_%s.service' % (self.id, )

    def save(self, *args, **kwargs):
        super(Daemon, self).save(*args, **kwargs)
        daemon_name = self.get_name()
        if self.is_active and self.token and self.exec_path and self.api_url:
            #exec_path = 'binary_bot/binary_bot.py'
            exec_script = '%s/apps/%s' % (settings.BASE_DIR, self.exec_path)
            create_daemon(daemon_name, exec_script, self.token, api_url=self.api_url)
        else:
            drop_daemon(daemon_name)

    def delete(self, *args, **kwargs):
        daemon_name = self.get_name()
        drop_daemon(daemon_name)
        super(Daemon, self).delete(*args, **kwargs)

