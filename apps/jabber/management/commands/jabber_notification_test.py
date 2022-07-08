# -*- coding: utf-8 -*-
import logging
import time
import json
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.fortasks import search_process
from apps.jabber.views import (
    update_fs_users_db_version,
    get_firebase_messaging_token,
    get_firebase_messaging_headers,
    get_firebase_messaging_url,
)
from apps.jabber.models import Registrations

logger = logging.getLogger(__name__)

# https://firebase.google.com/docs/cloud-messaging/concept-options#customizing_a_message_across_platforms

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--notification_sender',
            action = 'store_true',
            dest = 'notification_sender',
            default = False,
            help = 'Send push over notification_sender function')
        parser.add_argument('--notification_request',
            action = 'store_true',
            dest = 'notification_request',
            default = False,
            help = 'Send push over notification_request function')
        parser.add_argument('--data',
            action = 'store_true',
            dest = 'data',
            default = False,
            help = 'Send data notification')
        parser.add_argument('--push',
            action = 'store_true',
            dest = 'push',
            default = False,
            help = 'Send push notification')
        parser.add_argument('--token',
            action = 'store',
            type = str,
            dest = 'token',
            default = False,
            help = 'Set token')
        parser.add_argument('--app_id',
            action = 'store',
            type = str,
            dest = 'app_id',
            default = False,
            help = 'Set app_id')
    def handle(self, *args, **options):
        """Тестирования пуш уведомления и дата уведомления
        """
        is_running = search_process(q = ('jabber_notification_test', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()


        app_id = 'infoservice-f0261'
        if options.get('app_id'):
            app_id = options['app_id']
        #token = get_firebase_messaging_token(app_id)
        #print(token)

        only_data = False
        if options.get('data'):
            only_data = True

        token = None
        if options.get('token'):
            token = options['token']

        if options.get('notification_sender'):
            notification_sender(token=token, only_data=only_data, app_id=app_id)
        if options.get('notification_request'):
            notification_request(only_data=only_data, app_id=app_id)


def notification_request(app_id: str = 'chateriha',
                         only_data: bool = False,
                         phone = '89148959223'):
    """Отправка push уведомления через сервер
       :param app_id: приложение для получения ключа из json
       :param only_data: только data-push или с notification
       :param phone: телефон с регистрацией
    """
    #domain = 'http://127.0.0.1:8000'
    domain = 'https://chat.masterme.ru'
    uri = '%s/jabber/notification/%s/' % (domain, app_id)
    
    name = 'Den'
    title = 'Новое сообщение от %s' % name
    text = 'Новое сообщение от %s' % phone

    reg = Registrations(phone=phone, passwd='123')
    data = {
        'additional_data': {
            'action': 'call',
        },
        'name': 'Den',
        'toJID': phone,
        'fromJID': phone,
        'credentials': reg.get_hash(),

        'title': title,
        'body': text,
        #'wakeUpScreen': True,
    }
    if only_data:
        data['only_data'] = only_data
    print('req=>',json_pretty_print(data))
    r = requests.post(uri, json=data)
    print(r.text)
    print('resp=>', json_pretty_print(r.json()))


def notification_sender(token: str = None,
                        app_id: str = 'chateriha',
                        only_data: bool = False):
    """Отправка push уведомления
       :param token: токен клиента
       :param app_id: приложение для получения ключа из json
       :param only_data: только data-push или с notification
    """
    if not token:
        print('empty token')
        return
    to_jid = '79148959223'
    from_jid = '79148959223'
    name = 'Den'
    text = 'Новое сообщение от %s' % from_jid
    if text:
        if len(text) > 30:
            text = '%s...' % text[:30]
    title = name or 'Новое сообщение'

    url = get_firebase_messaging_url(app_id=app_id)

    data = {
        'message': {
            'data': {
                'sender': from_jid,
                'receiver': to_jid,
            },
            'notification': {
                'title': title,
                'body': text,
            },
            'token': token, # one recipient
        },
    }
    if only_data:
        data = {
            'message': {
                'data': {
                    'sender': from_jid,
                    'receiver': to_jid,
                },
                'token': token, # one recipient
            },
        }
    headers = get_firebase_messaging_headers(app_id=app_id)
    print(url)
    print(json_pretty_print(data))
    print(json_pretty_print(headers))
    r = requests.post(url, json=data, headers=headers)
    print(r.text)

