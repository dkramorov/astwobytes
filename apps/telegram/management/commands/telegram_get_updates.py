# -*- coding: utf-8 -*-
import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.telegram.telegram import TelegramBot

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    # USAGE:
    # python manage.py telegram_get_updates --token='...'
    # python manage.py telegram_get_updates --proxy='10.10.9.1:3128' --token='...' --chat_id='-478220379'
    def add_arguments(self, parser):
        parser.add_argument('--token',
            action = 'store',
            dest = 'token',
            type = str,
            default = False,
            help = 'Set bot token')
        parser.add_argument('--chat_id',
            action = 'store',
            dest = 'chat_id',
            type = str,
            default = False,
            help = 'Set bot chat_id')
        parser.add_argument('--proxy',
            action = 'store',
            dest = 'proxy',
            type = str,
            default = False,
            help = 'Set bot proxy')
        parser.add_argument('--create_invite_link',
            action = 'store_true',
            dest = 'create_invite_link',
            default = False,
            help = 'Create invite link for chat')
    def handle(self, *args, **options):
        kwargs = {}
        token = options.get('token')
        if token:
            kwargs['token'] = token
        chat_id = options.get('chat_id')
        if chat_id:
            kwargs['chat_id'] = chat_id
        proxy = options.get('proxy')
        if proxy:
            kwargs['proxies'] = {
                'http': proxy,
                'https': proxy,
            }
        logger.info(kwargs)
        bot = TelegramBot(**kwargs)
        logger.info(json_pretty_print(bot.get_updates()))

        if options.get('create_invite_link'):
            print(bot.create_invite_link())

