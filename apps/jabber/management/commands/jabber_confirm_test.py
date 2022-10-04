# -*- coding: utf-8 -*-
import logging
import time
import json
import random
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.fortasks import search_process
from apps.jabber.views import FS_REG_CODES, FS_REG_CODES_LEN

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--test',
            action = 'store_true',
            dest = 'test',
            default = False,
            help = 'test')
    def handle(self, *args, **options):
        """Проверка кода для регистрации аккаунта через подтверждение по телефону (поледним цифрам)
        """
        is_running = search_process(q = ('jabber_confirm_test', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()
        print(FS_REG_CODES)
        params = {}
        ind = random.randint(0, FS_REG_CODES_LEN-1)
        code = FS_REG_CODES[ind]
        # в луа скрипте в table индекс первого элемента = 1
        params['code'] = '%s' % (ind + 1, )
        params['ind'] = ind
        params['phone'] = FS_REG_CODES[ind]
        print(params)
