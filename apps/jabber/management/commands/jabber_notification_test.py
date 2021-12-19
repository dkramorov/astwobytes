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

all_settings = settings.FULL_SETTINGS_SET
FIREBASE_SERVER_KEY_8800 = all_settings['FIREBASE_SERVER_KEY_8800']
FIREBASE_SERVER_KEY_223 = all_settings['FIREBASE_SERVER_KEY_223']

TOKEN_DROID_959223 = 'fUIbEaDuTeqI16yWE97h5m:APA91bGRwOxrFjID2_IB2GxbY-uHUvLsNzE9SVa9ZkHP5c1z_cyyiHVEV5LK3590ZN4nWg-gClHuYO2enwdPjKjJcACMWJpXfzoPeozti1scd7BNNj750RoTRsi0K8su2G8PnS1ExtL1'

TOKEN_IOS_959223 = 'dPNG8CWNYUP-jxyYI3dqLU:APA91bGosyPkq7GvTm1JStg8YMqdhGapg-BlFYQlQVxza803kufH_XXnhr9cvKqo9Icvxl5ixFhnMV3hBpdRuphexfApuYGFJlUA_OrD0cvmIR2t9krlSOEYSwtQN1VncAz81_aU9Nk6'

def send_push_notification(token):
    """Тест пушь уведомления
       :param token: токен куда отпрваляем сообщение
    """
    result = {}
    result['user_ip'] = 'localhost'

    tokens = [token]

    to_jid = '89148959223'
    from_jid = '89016598623'
    msg_body = 'test for background activity'
    name = '8 (901) 659-86-23'

    url = 'https://fcm.googleapis.com/fcm/send'
    data = {
        'data': {
            'sender': from_jid,
            'receiver': to_jid,
        },
        'notification': {
            'title': name,
            'body': msg_body,
        },
        #'to': to_token,
        'registration_ids': tokens, # many recipient
        'click_action': 'FLUTTER_NOTIFICATION_CLICK',
    }

    headers = {'Authorization': 'key=%s' % FIREBASE_SERVER_KEY_8800}
    r = requests.post(url, json=data, headers=headers)
    try:
        resp = r.json()
        results = resp.get('results', [])
        for item in results:
            if 'error' in item and item.get('error') == 'NotRegistered':
                for token in tokens:
                    new_data = {k: v for k, v in data.items() if k != 'registration_ids'}
                    new_data['to'] = token
                    new_r = requests.post(url, json=new_data, headers=headers)
                    if 'NotRegistered' in new_r.text:
                        print('remove Firebase token %s' % new_r.text)

    except Exception as e:
        result['error'] = str(e)

    print(json_pretty_print(data))
    result['result'] = r.text
    result['tokens'] = tokens
    print(json_pretty_print(result))


def send_data_notification(token):
    """Тест data уведомления
       :param token: токен куда отпрваляем сообщение
    """
    result = {}
    result['user_ip'] = 'localhost'

    tokens = [token]

    to_jid = '89148959223'
    from_jid = '89016598623'
    msg_body = 'test for background activity'
    name = '8 (901) 659-86-23'

    url = 'https://fcm.googleapis.com/fcm/send'
    data = {
        'to': tokens[0],
        'data': {
            'sender': from_jid,
            'receiver': to_jid,
            'badge': 10,
        },
        'content_available': True,
        'priority': 'high',
    }

    headers = {'Authorization': 'key=%s' % FIREBASE_SERVER_KEY_8800}
    r = requests.post(url, json=data, headers=headers)
    try:
        resp = r.json()
    except Exception as e:
        result['error'] = str(e)

    print(json_pretty_print(data))
    result['result'] = r.text
    result['tokens'] = tokens
    print(json_pretty_print(result))

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
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
        parser.add_argument('--ios',
            action = 'store_true',
            dest = 'ios',
            default = False,
            help = 'Set ios token')
    def handle(self, *args, **options):
        """Тестирования пуш уведомления и дата уведомления
        """
        is_running = search_process(q = ('jabber_notification_test', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()
        token = TOKEN_DROID_959223
        if options.get('ios'):
            token = TOKEN_IOS_959223

        if options.get('push'):
            send_push_notification(token)
        if options.get('data'):
            send_data_notification(token)