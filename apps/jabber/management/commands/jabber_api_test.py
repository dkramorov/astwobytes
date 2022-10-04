# -*- coding: utf-8 -*-
import logging
import time
import json
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.fortasks import search_process
from apps.main_functions.catcher import json_pretty_print
from apps.jabber.ejabberd_api import EjabberdApi

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--test1',
            action = 'store_true',
            dest = 'test1',
            default = False,
            help = 'test1')

    def handle(self, *args, **options):
        """Тестирование апи ejabberd
        """
        is_running = search_process(q = ('jabber_api_test', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()

        api = EjabberdApi()
        resp = api.create_user(login='potestua', passwd='123')
        print('resp=>', resp.status_code, resp.text)
        print('---')
        resp = api.drop_user(login='potestua')
        print('resp=>', resp.status_code, resp.text)

        jaba_domain = 'https://%s' % settings.JABBER_DOMAIN.rstrip('/')
        endpoint = '/jabber/get_jabber_users'
        url = '%s%s' % (jaba_domain, endpoint)
        headers = {
            'token': settings.FS_TOKEN,
        }
        r = requests.get(url, headers=headers)
        print(r.status_code, r.text)

