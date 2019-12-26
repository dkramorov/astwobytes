# -*- coding: utf-8 -*-
import logging

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
        """Тестирование удаления/добавления пользователя в группу"""
        pass

