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
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--update_fs_users_db_version',
            action = 'store_true',
            dest = 'update_fs_users_db_version',
            default = False,
            help = 'Update fs users db version')
        parser.add_argument('--reg',
            action = 'store_true',
            dest = 'reg',
            default = False,
            help = 'Register my user')
    def handle(self, *args, **options):
        """Регистрация пользователя на ejabberd по апи
           $ ejabberdctl help unregister
             Description: Unregister a user
           $ ejabberdctl unregister badlop3 localhost
           $ ejabberdctl unregister 89148959224 anhel.1sprav.ru
           $ ejabberdctl help registered_users
             Description: List all registered users in HOST
           $ ejabberdctl registered_users localhost
        """
        is_running = search_process(q = ('jabber_reg_test', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()

        EJABBERD_LOCAL = 'https://127.0.0.1:5443'.rstrip('/')
        phone = '89148959224'
        passwd = '123'

        if options.get('update_fs_users_db_version'):
            new_version = update_fs_users_db_version()
            print('new version', new_version)

        if options.get('reg'):
            r = requests.post('%s/api/register' % EJABBERD_LOCAL, json={'user': phone, 'host': settings.JABBER_DOMAIN, 'password': passwd}, verify=False)
            print(r.text)
            try:
                reg_obj = r.json()
            except Exception as e:
                print('err: reg not json response')
                reg_obj = None
            if reg_obj:
                print(json_pretty_print(reg_obj))
                if 'code' in reg_obj and reg_obj['code'] == 10090:
                    r = requests.post('%s/api/change_password' % EJABBERD_LOCAL, json={'user': phone, 'host': settings.JABBER_DOMAIN, 'newpass': passwd}, verify=False)
                    if r.text == '0':
                        msg = 'Пароль пользователя %s успешно изменен' % phone
                        print(msg)
                elif 'successfully registered' in reg_obj:
                    msg = 'Пользователь %s успешно зарегистрирован' % phone
                    print(msg)


