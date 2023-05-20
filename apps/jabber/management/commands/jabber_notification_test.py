# -*- coding: utf-8 -*-
import logging
import datetime
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
    get_firebase_batch_template,
    create_notification_data,
    parse_batch_response,
)
from apps.jabber.models import Registrations
from apps.jabber.ejabberd_api import EjabberdApi

logger = logging.getLogger(__name__)

# https://firebase.google.com/docs/cloud-messaging/concept-options#customizing_a_message_across_platforms

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--notification_request',
            action = 'store_true',
            dest = 'notification_request',
            default = False,
            help = 'Send push over notification_request function')
        parser.add_argument('--notification_batch_request',
            action = 'store_true',
            dest = 'notification_batch_request',
            default = False,
            help = 'Send push over notification_batch_request function')
        parser.add_argument('--notification_sender',
            action = 'store_true',
            dest = 'notification_sender',
            default = False,
            help = 'Send push over notification_sender function')
        parser.add_argument('--notification_batch_sender',
            action = 'store_true',
            dest = 'notification_batch_sender',
            default = False,
            help = 'Send multile notifications')
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
        parser.add_argument('--notification_from_bot',
            action = 'store',
            type = str,
            dest = 'notification_from_bot',
            default = False,
            help = 'Send push notification from bot to channel')
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

        if options.get('notification_request'):
            notification_request(only_data=only_data, app_id='mastermechat')

        if options.get('notification_batch_request'):
            notification_batch_request(only_data=only_data, app_id='mastermechat', phones=['89016598623', '89148959223'])
            return

            # Тест для отправки в группу
            phones = None
            group_name = 'GROUP_gg3'
            field = 'DESC'
            ejabberd_manager = EjabberdApi()
            group_vcard = ejabberd_manager.get_vcard(login=group_name, vcard_field=field)
            if group_vcard.status_code == 200:
                desc = group_vcard.json()['content']
                if desc:
                    phones = json.loads(desc)['users']
            if not phones:
                print('set phones by default')
                phones = ['89148959223', '89016598623']
            notification_batch_request(only_data=only_data, app_id='mastermechat', phones=phones)

        if options.get('notification_sender'):
            token = 'dK0O0quQR6eN2be77EJSGX:APA91bG2jRZnzRS8Jfp4AIlz1p3zquNtfHji-64UBwQoWAeWbTkGVhV-KVdHLajp198cz9IixKqu8vQMg5QbatV3_sYMMtVuHywJNrl_gs6bKYn3Qx60gYOhvv0lyhxrE3cZJoMGbYBt'
            notification_sender(token=token, only_data=only_data, app_id='mastermechat')

        if options.get('notification_batch_sender'):
            tokens = [
                'dK0O0quQR6eN2be77EJSGX:APA91bG2jRZnzRS8Jfp4AIlz1p3zquNtfHji-64UBwQoWAeWbTkGVhV-KVdHLajp198cz9IixKqu8vQMg5QbatV3_sYMMtVuHywJNrl_gs6bKYn3Qx60gYOhvv0lyhxrE3cZJoMGbYBt',
                'cKkZOrFISqKBwPLUc4iZmK:APA91bGCBlyQaARO6LB_Hi8HMvw0dj1ej63DRcEawvSbZF-PAml0j0ClgMMBnBtyBVPT3BW9j9fGF-Q_UkkQ9Z2CA2WAiW-gV3kNS4m3ajdcVXBaKivlzT5Hz5AdwMNMhUg0L-H4eMUs',
            ]
            notification_batch_sender(tokens=tokens, app_id='mastermechat', only_data=only_data)

        if options.get('notification_from_bot'):
            text = options['notification_from_bot']
            notification_from_bot(text=text, app_id='mastermechat')

def notification_request(app_id: str = 'chateriha',
                         only_data: bool = False,
                         phone = '89148959223'):
    """Отправка push уведомления через сервер
       :param app_id: приложение для получения ключа из json
       :param only_data: только data-push или с notification
       :param phone: телефон с регистрацией
    """
    domain = 'http://127.0.0.1:8000'
    #domain = 'https://chat.masterme.ru'
    uri = '%s/jabber/notification/%s/' % (domain, app_id)
    
    name = 'Den'
    title = 'Новое сообщение от %s' % name
    text = 'Новое сообщение от %s' % phone

    reg = Registrations(phone=phone, passwd='123')
    data = {
        'additional_data': {
            'action': 'chat', # call
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

def notification_batch_request(app_id: str = 'chateriha',
                               only_data: bool = False,
                               phones = None):
    """Отправка push уведомления через сервер батчем
       :param app_id: приложение для получения ключа из json
       :param only_data: только data-push или с notification
       :param phones: телефоны с регистрацией
    """
    domain = 'http://127.0.0.1:8000'
    #domain = 'https://chat.masterme.ru'
    uri = '%s/jabber/notification_batch/%s/' % (domain, app_id)
    
    name = 'Den'
    title = 'Новое сообщение от %s' % name
    text = 'Новое сообщение от %s' % phones[0]

    reg = Registrations(phone=phones[0], passwd='123')
    print(reg, 'hash=%s' % reg.get_hash())
    data = {
        'additional_data': {
            'action': 'chat', # call
        },
        'name': 'Den',
        #'toJIDs': phones,
        'toGroupJid': 'gg3',
        'fromJID': phones[0],
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
    headers = get_firebase_messaging_headers(app_id=app_id)

    data = create_notification_data(from_jid, to_jid, title, text, only_data)
    data['message']['token'] = token

    print(url)
    print(json_pretty_print(data))
    print(json_pretty_print(headers))
    r = requests.post(url, json=data, headers=headers)
    print(r.text)

def notification_batch_sender(tokens: list = None,
                              app_id: str = 'mastermechat',
                              only_data: bool = False):
    """Отправка пушей батчем
       curl --data-binary @batch.txt -H 'Content-Type: multipart/mixed; boundary="subrequest_boundary"' -H 'Authorization: Bearer ya29....' https://fcm.googleapis.com/batch
    """
    if not tokens:
        print('empty tokens')
        return
    to_jid = '79148959223'
    from_jid = '79148959223'
    title = 'Проверка'
    text = 'Новое сообщение'
    url = 'https://fcm.googleapis.com/batch'
    headers = get_firebase_messaging_headers(app_id=app_id)
    headers['Content-Type'] = 'multipart/mixed; boundary="subrequest_boundary"'

    data = create_notification_data(from_jid, to_jid, title, text, only_data)
    template = get_firebase_batch_template(app_id=app_id)

    batch = ''
    for token in tokens:
        data['message']['token'] = token
        json_data = json_pretty_print(data)
        batch += template.format(json_data)
    batch += '--subrequest_boundary--'
    #print(url)
    #print(json_pretty_print(data))
    print(json_pretty_print(headers))
    print(batch)
    r = requests.post(url, data=batch.encode('utf-8'), headers=headers)
    print(r.status_code, r.text)
    print(json_pretty_print(parse_batch_response(r.text)))

def notification_from_bot(text: str = None, app_id: str = 'mastermechat'):
    """Отправка группового сообщения от бота
       1) Принимаем данные - от кого (бот, по нему найдем канал) и сообщение
    """
    domain = 'http://127.0.0.1:8000'
    if not settings.DEBUG:
        domain = 'https://chat.masterme.ru'
    url = '%s/jabber/notification_from_bot/%s/' % (domain, app_id)
    if not text:
        text = 'hello %s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'channel': 'dbupdates',
        'text': text,
        'passwd': '75ij5tvx49',
        'only_data': True,
        'additional_data': {
            'action': 'chat',
        },
    }
    r = requests.post(url, json=data)
    print(r.text)

