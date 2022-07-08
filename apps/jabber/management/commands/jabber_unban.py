# -*- coding: utf-8 -*-
import logging
import time
import json
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.fortasks import search_process
from apps.jabber.views import update_fs_users_db_version

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """Настройка доступа к апи
       https://docs.ejabberd.im/developer/ejabberd-api/simple-configuration/
    """
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--test',
            action = 'store_true',
            dest = 'test',
            default = False,
            help = 'test')
        parser.add_argument('--ip',
            action = 'store',
            type = str,
            dest = 'ip',
            default = False,
            help = 'Set ip for unban')

    def handle(self, *args, **options):
        """Разблокировка fail2ban ip адреса
           https://docs.ejabberd.im/archive/20_07/admin-api/#unban-ip
        """
        is_running = search_process(q = ('jabber_unban', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()
        all_settings = settings.FULL_SETTINGS_SET
        ip = options.get('ip')
        if ip:
            s = requests.Session()
            s.auth = ('%s@%s' % (all_settings['JABBER_ADMIN_LOGIN'], settings.JABBER_DOMAIN), all_settings['JABBER_ADMIN_PASSWD'])
            r = s.post('https://%s:5443/api/unban_ip' % settings.JABBER_DOMAIN, json={'address': ip}, verify=False)
            print(r.text)

