# -*- coding: utf-8 -*-
import logging
import time
import os
import shutil
import re
import json

from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--fake',
            action = 'store_true',
            dest = 'fake',
            default = False,
            help = 'Do nothing')
        parser.add_argument('--fake_value',
            action = 'store',
            dest = 'fake_value',
            type = str,
            default = False,
            help = 'Set fake value')

    def handle(self, *args, **options):
        """Тестирование отправки email"""
        mail = EmailMessage('Заголовок сообщения', 'Текст сообщения - проверка', settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
        mail.send()
