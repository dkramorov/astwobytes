# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.telegram.telegram import TelegramBot

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        bot = TelegramBot()
        logger.info(json_pretty_print(bot.get_updates()))


