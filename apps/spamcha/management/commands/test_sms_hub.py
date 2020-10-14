# -*- coding: utf-8 -*-
import logging
import json
import redis

from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--multiple',
            action = 'store_true',
            dest = 'multiple',
            default = False,
            help = 'Send to multiple accounts')
        parser.add_argument('--single',
            action = 'store_true',
            dest = 'single',
            default = False,
            help = 'Send to single account')
    def handle(self, *args, **options):
        """Тестовая отправка почты smtplib"""
        rediska = redis.Redis()
        icc_id ='897010244266343012ff'
        cache_key = '%s_%s' % (settings.SMS_HUB_TOKEN, icc_id)
        rediska.set(cache_key, json.dumps([
            {'phone': '89148959223', 'text': 'редиска, сосика и молоко купи'}
        ]))


