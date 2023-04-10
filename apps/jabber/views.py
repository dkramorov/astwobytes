# -*- coding:utf-8 -*-
import os
import json
import random
import requests
import datetime
import traceback
import base64

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count

from oauth2client.service_account import ServiceAccountCredentials
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.string_parser import kill_quotes, GenPasswd, get_request_ip, convert2camelcase
from apps.main_functions.date_time import date_plus_days
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from apps.main_functions.files import (check_path,
                                       open_file,
                                       make_folder,
                                       imageThumb,
                                       extension,
                                       catch_file, )

from apps.jabber.models import Registrations, FirebaseTokens, DeviceContacts
from apps.jabber.ejabberd_api import ejabberd_manager

JABBER_API = 'https://%s:5443' % settings.JABBER_DOMAIN

CUR_APP = 'jabber'
registrations_vars = {
    'singular_obj': 'Регистрация',
    'plural_obj': 'Регистрации',
    'rp_singular_obj': 'регистрации',
    'rp_plural_obj': 'регистраций',
    'template_prefix': 'jabber_registrations_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'jabber',
    'submenu': 'registrations',
    'show_urla': 'show_registrations',
    'create_urla': 'create_registration',
    'edit_urla': 'edit_registration',
    'model': Registrations,
    #'custom_model_permissions': Registrations,
}

FS_REG_CODES = []
for item in settings.FULL_SETTINGS_SET.get('FREESWITCH_REG_PHONES', '').split(','):
    FS_REG_CODES.append(item.strip()[-4:])
FS_REG_CODES_LEN = len(FS_REG_CODES)

def get_jabber_users(request):
    """Отдаем пользователей джаббера, например, для свича,
       чтобы он мог завести их в directory
    """
    result = []
    token = request.headers.get('token') or request.GET.get('token') or request.POST.get('token')
    if not token == settings.FS_TOKEN:
        return JsonResponse({'error': 'bad token'}, safe=False)
    registrations = Registrations.objects.filter(is_active=True).values('phone', 'passwd')
    for registration in registrations:
        phone = kill_quotes(registration['phone'], 'int')
        if not phone or not len(phone) == 11 or not registration['passwd']:
            continue
        result.append({
            'phone': phone,
            'passwd': registration['passwd'],
        })
    return JsonResponse(result, safe=False)

@login_required
def show_registrations(request, *args, **kwargs):
    """Вывод регистраций
       :param request: HttpRequest
    """
    return show_view(request,
                     model_vars = registrations_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_registration(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование регистрации
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    return edit_view(request,
                     model_vars = registrations_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id)

@login_required
def registrations_positions(request, *args, **kwargs):
    """Изменение позиций регистраций
       :param request: HttpRequest
    """
    result = {}
    mh_vars = registrations_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_registrations(request, *args, **kwargs):
    """Поиск регистраций
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = registrations_vars,
                       cur_app = CUR_APP,
                       sfields = ('phone', ), )

tokens_vars = {
    'singular_obj': 'Токен FCM',
    'plural_obj': 'Токены FCM',
    'rp_singular_obj': 'токена FCM',
    'rp_plural_obj': 'токенов FCM',
    'template_prefix': 'jabber_tokens_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'jabber',
    'submenu': 'tokens',
    'show_urla': 'show_tokens',
    'create_urla': 'create_token',
    'edit_urla': 'edit_token',
    'model': FirebaseTokens,
    #'custom_model_permissions': FirebaseTokens,
}

@login_required
def show_tokens(request, *args, **kwargs):
    """Вывод токенов
       :param request: HttpRequest
    """
    return show_view(request,
                     model_vars = tokens_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_token(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование токена
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    return edit_view(request,
                     model_vars = tokens_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def tokens_positions(request, *args, **kwargs):
    """Изменение позиций токенов
       :param request: HttpRequest
    """
    result = {}
    mh_vars = tokens_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_tokens(request, *args, **kwargs):
    """Поиск токенов
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = tokens_vars,
                       cur_app = CUR_APP,
                       sfields = ('login', 'token'), )

device_contacts_vars = {
    'singular_obj': 'Контакт утройства',
    'plural_obj': 'Контакты устройств',
    'rp_singular_obj': 'контакта устройства',
    'rp_plural_obj': 'контактов устройств',
    'template_prefix': 'jabber_device_contacts_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'jabber',
    'submenu': 'device_contacts',
    'show_urla': 'show_device_contacts',
    'create_urla': 'create_device_contact',
    'edit_urla': 'edit_device_contact',
    'model': DeviceContacts,
    #'custom_model_permissions': FirebaseTokens,
}

@login_required
def show_device_contacts(request, *args, **kwargs):
    """Вывод контактов устройств
       :param request: HttpRequest
    """
    return show_view(request,
                     model_vars = device_contacts_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_device_contact(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование контактов устройств
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    return edit_view(request,
                     model_vars = device_contacts_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def device_contacts_positions(request, *args, **kwargs):
    """Изменение позиций контактов устройств
       :param request: HttpRequest
    """
    result = {}
    mh_vars = device_contacts_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_device_contact(request, *args, **kwargs):
    """Поиск контактов устройств
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = device_contact_vars,
                       cur_app = CUR_APP,
                       sfields = ('jid', 'phones', 'display_name'), )

def register_user(request):
    """Апи-метод для регистрации нового пользователя
                     восстановление пароля
       1) Приложение отправляет нам телефон пользователя
       2) Мы запоминаем телефон, генерируем код подтверждения, вносим в таблицу
       3) Делаем звонок, сообщаем код подтверждения, пользователь вносит код
       4) Приложение отправляет код и если код подходит, выполняем регистрацию
       5) Если пользователь уже существует, заменяем парольку

       Апи метод для обновления токена,
       необходимо перейти на ejabberd связку логина и токена
    """
    result = {}
    status_code = 200 # код ответа

    method = request.GET if request.method == 'GET' else request.POST
    action = method.get('action')
    phone = method.get('phone')
    if phone:
        phone = kill_quotes(phone, 'int')
    if action == 'update_token' and phone:
        token = method.get('token')
        analog = FirebaseTokens.objects.filter(token=token).first()
        if not analog:
            analog = FirebaseTokens(token=token)
        analog.apns_token = method.get('apns_token')
        analog.login = phone
        analog.ip = get_request_ip(request)
        analog.save()

    elif action == 'registration' and phone:
        if len(phone) == 11 and phone[0] == '8' and phone[1] == '9':
            # Сильно часто не даем проходить регистрации
            now = datetime.datetime.now()
            long_ago = now - datetime.timedelta(minutes=15)
            prev_registrations = Registrations.objects.filter(
                phone=phone,
                is_active=False,
                created__gte=long_ago,
            ).aggregate(Count('id'))['id__count']
            if prev_registrations:
                return JsonResponse({
                    'message': 'Мы уже отправили вам звонок, если звонок не пришел, повторите попытку через полчаса',
                    'code': 429,
                    'status': 'too_many_attempts',
                }, safe=False, status=429)

            code = '0000'
            for i in range(10):
                code = GenPasswd(4, '1234567890')
                if not code.startswith('0'):
                    break

            platform = method.get('platform')
            version = method.get('version')
            passwd = method.get('passwd')
            name = method.get('name')

            # Скрипт отправляет на свич телефон и код,
            # свич звонит и диктует
            params = {
                'phone': phone,
                'digit': code,
            }

            # Для упрощенной первичной регистрации надо отправлять
            # simple_reg=1 в параметрах (чтобы регнуться по 4 последним цифрам входящего)
            simple_reg = method.get('simple_reg')
            # Если регистрация новая (нет активных регистраций),
            # тогда отправляем звонок со сбросом
            # и подтверждение будет по 4 последним цифрам номера,
            # если активные регистрации есть,
            # тогда отправляем звонок и код проговаривается
            ind = 0
            if simple_reg:
                active_registrations = Registrations.objects.filter(
                    phone=phone,
                    is_active=True
                ).aggregate(Count('id'))['id__count']
                if not active_registrations:
                    ind = random.randint(0, FS_REG_CODES_LEN-1)
                    code = FS_REG_CODES[ind]
                    # в луа скрипте в table индекс первого элемента = 1
                    params['digit'] = '%s' % (ind + 1, )
                    params['script'] = 'reg_call.lua'
                    params['simple_reg'] = 1

            # Заносим пользователя как отключенного (is_active=False)
            analog = Registrations(is_active=False)
            analog.phone = phone
            analog.code = code
            analog.name = name if name else phone
            analog.platform = platform
            analog.version = version
            analog.passwd = passwd
            analog.save()
            # Код передаем на свич - поэтому,
            # он секретная инфа, как паролька
            result = object_fields(analog, pass_fields=('passwd', 'code'))
            if 'simple_reg' in params:
                result['simple_reg'] = True

            uri = '%s/freeswitch/sms_service/say_code/' % settings.FREESWITCH_DOMAIN
            if not uri.startswith('https://'):
                uri = 'https://%s' % uri

            # Не ждем, завершаем запрос сразу,
            # запрос будет долгий, пока не завершится звонок
            try:
                r = requests.get(uri, params=params, timeout=(5, 0.1))
            except Exception as e:
                pass
            return JsonResponse(result, safe=False, status=status_code)

    elif action == 'confirm' and phone:
        code = method.get('code')
        # Берем только за последний час попытку регистрации
        now = datetime.datetime.now()
        long_ago = date_plus_days(now, minutes=-30)
        # Проверяем, сколько раз чел вводил проверочный код
        analog = Registrations.objects.filter(phone=phone,
                                              created__gte=long_ago,
                                              is_active=False).last()
        if analog:
            attempt = 0
            if analog.state:
                attempt = analog.state
            attempt += 1
            Registrations.objects.filter(pk=analog.id).update(state=attempt)

            if attempt >= 3:
                return JsonResponse({
                    'message': 'Слишком много попыток, повторите регистрацию через полчаса',
                    'code': 429,
                    'status': 'too_many_attempts',
                }, safe=False, status=429)
            if not code == analog.code:
                return JsonResponse({
                    'message': 'Неправильный код подтверждения',
                    'code': 401,
                    'status': 'error',
                }, safe=False, status=401)

            # Все регистрации делаем неактивными
            Registrations.objects.filter(phone=phone).update(is_active=False, updated=now)
            # Делаем текущую активной
            analog.is_active = True
            analog.save()

            result = object_fields(analog, pass_fields=('passwd', 'code'))
            # Инкремент версии в связи с новой регистрацией
            update_fs_users_db_version()
            # Отправляем запрос, чтобы freeswitch обновил пользователей
            r = requests.get(settings.FULL_SETTINGS_SET.get('FS_UPDATE_USERS_TASK'))

            # Делаем запрос на реальную регистрацию пользователя
            # https://docs.ejabberd.im/developer/ejabberd-api/admin-api/
            reg_result = reg_user_on_jabber(analog.phone, analog.passwd, name=analog.name)
            status_code = reg_result['code']
            result['result'] = reg_result['msg']

    return JsonResponse(result, safe=False, status=status_code)

def reg_user_on_jabber(phone: str, passwd: str, name: str = None):
    """Регистрация пользователя на джаббере,
       либо смена пароля, если пользователь имеется
       :param phone: телефон
       :param passwd: пароль
       :param name: имя для создания vcard
    """
    r = requests.post('%s/api/register' % JABBER_API, json={'user': phone, 'host': settings.JABBER_DOMAIN, 'password': passwd}, verify=False)
    try:
        reg_obj = r.json()
    except Exception as e:
        reg_obj = None
    if reg_obj:
        if 'code' in reg_obj and reg_obj['code'] == 10090:
            r = requests.post('%s/api/change_password' % JABBER_API, json={'user': phone, 'host': settings.JABBER_DOMAIN, 'newpass': passwd}, verify=False)
            if r.text == '0':
                ejabberd_manager.set_vcard(
                    login=phone,
                    vcard_field='FN',
                    vcard_value=name or phone,
                )
                return {
                    'msg': 'Пароль пользователя %s успешно изменен' % phone,
                    'code': 201,
                }
        elif 'successfully registered' in reg_obj:
            ejabberd_manager.set_vcard(
                login=phone,
                vcard_field='FN',
                vcard_value=name or phone,
            )
            return {
                'msg': 'Пользователь %s успешно зарегистрирован' % phone,
                'code': 200,
            }

def update_fs_users_db_version():
    """Записываем новую версию для пользователей свича
       свич сам заберет эту новую версию и если она
       действительно новая, тогда инициируем обновление
       пользователей и перезапуск свича
    """
    fs_users_db_version_path = 'fs_users_db_version.json'
    if check_path(fs_users_db_version_path):
        version = 1
    else:
        with open_file(fs_users_db_version_path, 'r', encoding='utf-8') as f:
            content = json.loads(f.read())
        version = int(content['version']) + 1
    with open_file(fs_users_db_version_path, 'w+', encoding='utf-8') as f:
        f.write(json.dumps({'version': version}))
    return version

def get_firebase_messaging_token(app_id: str):
    """Получение токена для firebase messaging
       :param app_id: приложение firebase messaging (Project Id)
    """
    fsm_scope = 'https://www.googleapis.com/auth/firebase.messaging'
    key = settings.FULL_SETTINGS_SET['FIREBASE_KEY_FILE_%s' % app_id.upper().replace('-', '_')]
    cred = ServiceAccountCredentials.from_json_keyfile_name(key, fsm_scope)
    token = cred.get_access_token().access_token
    return token.split('.....')[0]

def get_firebase_messaging_headers(app_id: str):
    """Получение заголовка авторизации для firebase messaging
       :param app_id: приложение firebase messaging (Project Id)
    """
    return {'Authorization': 'Bearer %s' % get_firebase_messaging_token(app_id=app_id)}

def get_firebase_messaging_url(app_id: str):
    """Получение ссылки для отправки push для firebase messaging
       :param app_id: приложение firebase messaging (Project Id)
    """
    return 'https://fcm.googleapis.com/v1/projects/%s/messages:send' % (app_id, )

def get_firebase_batch_template(app_id: str):
    """Получение шаблона для пакетной отправки пушей
    """
    return '''--subrequest_boundary
Content-Type: application/http
Content-Transfer-Encoding: binary

POST /v1/projects/%s/messages:send
Content-Type: application/json
accept: application/json

{}

''' % (app_id, )

def trim_firebase_message(text):
    """Срезать размер текста в сообщении
       :param text: текст сообщения
    """
    if text:
        if len(text) > 30:
            text = '%s...' % text[:30]
    return text

def set_name_from_phonebook(to_jid: str, from_jid: str, data: dict):
    """Найти имя по телефонной книге
       :param to_jid: кому придет сообщение, значит, ищем в его контактов от кого
       :param from_jid: от кого идет сообщение, он должен подисаться из контактов to_jid
       :param data: словарь с данными пушь сообщения
    """
    device_contact = DeviceContacts.objects.filter(jid_owner=to_jid, phones__contains=from_jid).first()
    if device_contact:
        data['message']['data']['displayName'] = device_contact.display_name

def parse_batch_response(resp_text: str):
    """Анализируем ответ батчем, например, такой:
--batch_0g-_f3BLSE6_rLaD1n2xwU_gS-_bitPm
Content-Type: application/http
Content-ID: response-

HTTP/1.1 404 Not Found
Vary: Origin
Vary: X-Origin
Vary: Referer
Content-Type: application/json; charset=UTF-8

{
  "error": {
    "code": 404,
    "message": "Requested entity was not found.",
    "status": "NOT_FOUND",
    "details": [
      {
        "@type": "type.googleapis.com/google.firebase.fcm.v1.FcmError",
        "errorCode": "UNREGISTERED"
      }
    ]
  }
}

--batch_0g-_f3BLSE6_rLaD1n2xwU_gS-_bitPm
Content-Type: application/http
Content-ID: response-

HTTP/1.1 200 OK
Content-Type: application/json; charset=UTF-8
Vary: Origin
Vary: X-Origin
Vary: Referer

{
  "name": "projects/mastermechat/messages/0:1678168501415742%971636b0971636b0"
}

--batch_0g-_f3BLSE6_rLaD1n2xwU_gS-_bitPm--
       :param resp_text: ответ от сервера
    """
    lines = resp_text.splitlines()
    step = 0
    responses = []
    content = ''
    for line in lines:
        line = line.strip()
        if line.startswith('--batch'):
            if content:
                responses.append(json.loads(content))
            content =  ''
            step = 1
        elif line == '' and step == 1:
            step = 2
        elif line.startswith('{') and step == 2:
            step = 3
        if step == 3:
            content += line
    if content:
        responses.append(json.loads(content))
    return responses

def create_notification_data(from_jid: str,
                             to_jid: str,
                             title: str,
                             text: str,
                             only_data: bool, 
                             additional_data: dict = None):
    """Формируем тело для пушь сообщения
       :param from_jid: от кого (телефон)
       :param to_jid: кому (телефон)
       :param title: заголовок
       :param text: текст
       :param only_data: если нужно только data-сообщение
       :param additional_data: дополнительные параметры в сообщении
    """
    data = {
        'message': {
            'data': {
                'sender': from_jid,
                'receiver': to_jid,
            },
        },
    }
    if only_data:
        data['message']['data']['body'] = text
    else:
        data['message']['notification'] = {
            'title': title,
            'body': text,
        }
    data['message']['android'] = {
        'priority': 'high',
    }
    if additional_data and isinstance(additional_data, dict):
        for k, v in additional_data.items():
            data['message']['data'][k] = v
    return data

def drop_broken_token(token: str, resp: dict):
    """Удаление битых токенов, если ответ на пуши был с ошибкой
       :param token: токен, который пушили
       :param resp: ответ от сервера пушей (тело)
    """
    if isinstance(resp, dict) and 'error' in resp:
        if resp['error'].get('code') in (403, 404):
            FirebaseTokens.objects.filter(token=token).delete()
            print(token, 'deleted')
            return True

@csrf_exempt
def notification_batch_helper(request, app_id: str = None):
    """Апи-метод пакетной отправки пушей
       curl --data-binary @batch.txt -H 'Content-Type: multipart/mixed; boundary="subrequest_boundary"' -H 'Authorization: Bearer ya29....' https://fcm.googleapis.com/batch

       Содержимое файла
--subrequest_boundary
Content-Type: application/http
Content-Transfer-Encoding: binary

POST /v1/projects/mastermechat/messages:send
Content-Type: application/json
accept: application/json

{
  "message":{
     "token":"dK0O0quQR6eN2be77EJSGX:APA91bG2jRZnzRS8Jfp4AIlz1p3zquNtfHji-64UBwQoWAeWbTkGVhV-KVdHLajp198cz9IixKqu8vQMg5QbatV3_sYMMtVuHywJNrl_gs6bKYn3Qx60gYOhvv0lyhxrE3cZJoMGbYBt",
     "notification":{
       "title":"FCM Message",
       "body":"This is an FCM notification message!"
     }
  }
}

--subrequest_boundary
Content-Type: application/http
Content-Transfer-Encoding: binary

POST /v1/projects/mastermechat/messages:send
Content-Type: application/json
accept: application/json

{
  "message":{
     "token":"cKkZOrFISqKBwPLUc4iZmK:APA91bGCBlyQaARO6LB_Hi8HMvw0dj1ej63DRcEawvSbZF-PAml0j0ClgMMBnBtyBVPT3BW9j9fGF-Q_UkkQ9Z2CA2WAiW-gV3kNS4m3ajdcVXBaKivlzT5Hz5AdwMNMhUg0L-H4eMUs",
     "notification":{
       "title":"FCM Message",
       "body":"This is an FCM notification message!"
     }
  }
}
--subrequest_boundary--
    """
    result = {}
    ip_white_list = ['138.68.109.138']
    result['user_ip'] = get_request_ip(request)

    method = request.GET if request.method == 'GET' else request.POST
    body = None
    tokens = []

    to_token = None
    to_jids = []
    to_tokens = [] # связка логин: токен кому шлем
    from_jid = None
    msg_body = None
    name = None
    only_data = False # только data push
    additional_data = {} # доп параметры в data push

    if request.body:
        try:
            body = json.loads(request.body)
        except Exception as e:
            result['error'] = str(e)
        if body:

            credentials = body.get('credentials')
            to_jids = body.get('toJIDs') or []
            from_jid = body.get('fromJID') # не преобразуем т/к хэш будет неправильный
            msg_body = body.get('body')
            name = body.get('name')
            result['body'] = body
            # Только data push
            if 'only_data' in body:
                only_data = True
            if 'additional_data' in body:
                additional_data = body['additional_data']
            if 'credentials' in result['body']:
                del result['body']['credentials']

            # Отправлена группа на которую надо разослать, вытаскиваем по ней пользователей
            to_group_jid = kill_quotes(body.get('toGroupJid', ''), 'just_text')
            if to_group_jid:
                additional_data['group'] = to_group_jid
                group_name = 'GROUP_%s' % to_group_jid.split('@')[0]
                field = 'DESC'
                group_vcard = ejabberd_manager.get_vcard(login=group_name, vcard_field=field)
                if group_vcard.status_code == 200:
                    desc = group_vcard.json()['content']
                    if desc:
                        phones = json.loads(desc)['users']
                        for phone in phones:
                            if phone != from_jid and not phone in to_jids:
                                to_jids.append(phone)

            analog = Registrations.objects.filter(phone=from_jid, is_active=True).first()
            if analog and analog.get_hash() == credentials:
                tokens = list(FirebaseTokens.objects.filter(login__in=to_jids).values('token', 'login'))
                to_tokens = {}
                for token in tokens:
                    to_tokens[token['login']] = token['token']
            else:
                result['error'] = 'Restricted access'

    text = trim_firebase_message(msg_body or 'Новое сообщение от %s' % from_jid)
    title = name or 'Новое сообщение'
    url = 'https://fcm.googleapis.com/batch'
    headers = get_firebase_messaging_headers(app_id=app_id)
    headers['Content-Type'] = 'multipart/mixed; boundary="subrequest_boundary"'
    template = get_firebase_batch_template(app_id=app_id)

    tokens_order = []
    batch = ''
    for to_jid, token in to_tokens.items():
        data = create_notification_data(from_jid, to_jid, title, text, only_data, additional_data)
        data['message']['token'] = token
        # Надо подписать от кого поибашило сообщение по книге контактов кому прибашило
        # значит, надо достать контакты того кому шлем
        set_name_from_phonebook(to_jid, from_jid, data)
        json_data = json_pretty_print(data)
        batch += template.format(json_data)
        tokens_order.append(token)
    batch += '--subrequest_boundary--'

    r = requests.post(url, data=batch.encode('utf-8'), headers=headers)

    result['url'] = url
    result['app_id'] = app_id

    try:
        responses = parse_batch_response(r.text)
        if len(responses) == len(tokens_order):
            for i, response in enumerate(responses):
                if drop_broken_token(tokens_order[i], response):
                    result[tokens_order[i]] = 'DELETED'
    except Exception as e:
        traceback.print_exc()

    return JsonResponse(result, safe=False)

def single_push(app_id: str, body: dict):
    """Отправка одиночного пуша"""
    result = {}

    tokens = []
    to_token = None
    only_data = False # только data push
    additional_data = {} # доп параметры в data push

    credentials = body.get('credentials')
    to_jid = body.get('toJID')
    from_jid = body.get('fromJID') # не преобразуем т/к хэш будет неправильный
    msg_body = body.get('body')
    name = body.get('name')
    result['body'] = body
    # Только data push
    if 'only_data' in body:
        only_data = True
    if 'additional_data' in body:
        additional_data = body['additional_data']
    if 'credentials' in result['body']:
        del result['body']['credentials']

    analog = Registrations.objects.filter(phone=from_jid, is_active=True).first()
    if analog and analog.get_hash() == credentials:
        tokens = list(FirebaseTokens.objects.filter(login=to_jid).values_list('token', flat=True))
    else:
        result['error'] = 'Restricted access'
        return result

    text = trim_firebase_message(msg_body or 'Новое сообщение от %s' % from_jid)
    title = name or 'Новое сообщение'
    url = url = get_firebase_messaging_url(app_id=app_id)
    headers = get_firebase_messaging_headers(app_id=app_id)
    # С ибучим api v1 нельзя registration_ids, нужно использовать группы или топики
    data = create_notification_data(from_jid, to_jid, title, text, only_data, additional_data)

    # Надо подписать от кого поибашило сообщение по книге контактов кому прибашило
    # значит, надо достать контакты того кому шлем
    device_contact = DeviceContacts.objects.filter(jid_owner=to_jid, phones__contains=from_jid).first()
    if device_contact:
        data['message']['data']['displayName'] = device_contact.display_name

    for token in tokens:
        data['message']['token'] = token
        r = requests.post(url, json=data, headers=headers)
        resp = r.text
        try:
            resp = json.loads(r.text)
        except Exception as e:
            result['json_error_response'] = str(e)
        result[token] = resp

        if drop_broken_token(token, resp):
            result[token] = 'DELETED'
    if not tokens:
        result['fail'] = 'tokens not found'

    result['url'] = url
    return result

@csrf_exempt
def notification_helper(request, app_id: str = None):
    """Апи-метод для отправки уведомления (пуша)
       https://firebase.google.com/docs/cloud-messaging/migrate-v1
       :param request: HttpRequest
       :param app_id: ид приложения (для получения файла json с ключем)
    """
    result = {}
    ip_white_list = ['138.68.109.138']

    method = request.GET if request.method == 'GET' else request.POST
    body = None

    if request.body:
        try:
            body = json.loads(request.body)
        except Exception as e:
            result['error'] = str(e)
        if body:
            result = single_push(app_id, body)

    result['app_id'] = app_id
    result['user_ip'] = get_request_ip(request)
    return JsonResponse(result, safe=False)

def get_registered_users():
    """Получение списка всех зарегистрированных пользователей
    """
    r = requests.post('%s/api/registered_users' % JABBER_API, json={'host': settings.JABBER_DOMAIN}, verify=False)
    return r.json()

@csrf_exempt
def vcard(request):
    """Апи-метод для обновления vCard
       Обновляем только фото, остальные поля
       отлично обновляются через XMPP
    """
    result = {}
    method = request.GET if request.method == 'GET' else request.POST

    media_folder = 'jabber_avatars'
    phone = method.get('phone')
    credentials = method.get('credentials')
    action = method.get('action')

    analog = Registrations.objects.filter(phone=phone, is_active=True).first()
    if not analog or not analog.get_hash() == credentials:
        return JsonResponse({'error': 'not found'}, safe=False)

    result['action'] = action
    if action == 'get_vcard':
        field = method.get('field')
        resp = ejabberd_manager.get_vcard(login=phone, vcard_field=field)
        result['result'] = {
            'status_code': resp.status_code,
            field: resp.json(),
        }

    if action == 'set_vcard':
        resp = ejabberd_manager.set_vcard(
            login=phone,
            vcard_field=method.get('field'),
            vcard_value=method.get('value'),
        )
        result['result'] = {
            'status_code': resp.status_code if resp else 400,
            'json': resp.text if resp else '-1',
        }

    if request.FILES.get('file'):
        img = request.FILES['file']
        ext = extension(img.name)

        if ext:
            if check_path(media_folder):
                make_folder(media_folder)
            path = os.path.join(media_folder, '%s%s' % (phone, ext))
            if catch_file(img, path):
                result['url'] = 'https://%s/media/%s' % (request.META['HTTP_HOST'], path)
            else:
                result['error'] = 'Не удалось сохранить файл'
        else:
            result['error'] = 'Пользователь не идентифицирован'

    return JsonResponse(result, safe=False)


@csrf_exempt
def group_vcard(request):
    """Апи-метод для обновления группового vCard
       Пишем всех пользователей состоящих в группе в VCard
    """
    result = {}
    method = request.GET if request.method == 'GET' else request.POST

    phone = credentials = to_group = None
    if request.body:
        try:
            body = json.loads(request.body)
        except Exception as e:
            result['error'] = str(e)
        if body:
            credentials = body.get('credentials')
            phone = kill_quotes(body.get('JID'), 'int')
            to_group = body.get('to_group', '')
            if not '@conference.' in to_group:
                to_group = None
            else:
                to_group = kill_quotes(body.get('to_group', '').split('@')[0], 'just_text')
            result['phone'] = phone
            result['credentials'] = credentials
            result['to_group'] = to_group
    if phone and credentials and to_group:
        analog = Registrations.objects.filter(phone=phone, is_active=True).first()
        if not analog or not analog.get_hash() == credentials:
            result['error'] = 'not found'
        else:
            result['success'] = 1
            field = 'DESC'
            group_name = 'GROUP_%s' % to_group
            resp = ejabberd_manager.get_vcard(login=group_name, vcard_field=field)
            need_update = False
            if 'error_no_vcard_found' in resp.text:
                desc = {'users': [phone]}
                need_update = True
            else:
                desc = json.loads(resp.json()['content'])
                users = desc['users']
                if not phone in users:
                    need_update = True
                    users.append(phone)
                    desc['users'] = users
            if need_update:
                ejabberd_manager.set_vcard(
                    login=group_name,
                    vcard_field=field,
                    vcard_value=json.dumps(desc),
                )

    return JsonResponse(result, safe=False)

@login_required
def test_push(request):
    """Тест отправки push сообщения
    """
    result = {}
    name = 'Тест отправки push сообщения'
    root_url = reverse('jabber:test_push', current_app=CUR_APP)
    context = {
         'app': CUR_APP,
         'title': name,
         'singular_obj': name,
         'rp_singular_obj': 'Теста отправки push сообщения',
         'breadcrumbs': [{
             'name': 'Чат Jabber',
             'link': root_url,
         }, {
             'name': name,
             'link': root_url,
         }],
         'menu': tokens_vars['menu'],
         'submenu': 'test_push',
    }

    # Переменные
    chat_app = 'mastermechat'
    action = 'chat'
    login = '89148959223'
    passwd = '123'
    to_phone = '89016598623'
    text = 'test'
    only_data = True
    notify_endpoint = '/jabber/notification/%s/' % chat_app;
    url = 'https://%s%s' % (settings.JABBER_DOMAIN, notify_endpoint)

    if request.is_ajax() and request.method == 'POST':
        if request.POST.get('chat_app'):
            chat_app = request.POST['chat_app']
        if request.POST.get('action'):
            action = request.POST['action']
        if request.POST.get('chat'):
            chat = request.POST['chat']
        if request.POST.get('login'):
            login = request.POST['login']
        if request.POST.get('passwd'):
            passwd = request.POST['passwd']
        if request.POST.get('to_phone'):
            to_phone = request.POST['to_phone']
        if request.POST.get('text'):
            text = request.POST['text']
        if request.POST.get('only_data'):
            only_data = True
        else:
            only_data = False

        data = {
            'additional_data': {
                'action': action,
            },
            'name': login, # от кого
            'toJID': kill_quotes(to_phone, 'int'),
            'fromJID': kill_quotes(login, 'int'),
            'credentials': Registrations(phone=kill_quotes(login, 'int'), passwd=passwd).get_hash(),
            'body': text,
        }
        if only_data:
            data['only_data'] = True
        #return JsonResponse(data, safe=False)
        r = requests.post(url, json=data)
        return JsonResponse(r.json(), safe=False)

    template = '%s_test_push.html' % (CUR_APP, )
    return render(request, template, context)


@csrf_exempt
def set_device_contacts(request):
    """Апи-метод для получения контактов с устройства
       :param request: HttpRequest
    """
    result = {}
    method = request.GET if request.method == 'GET' else request.POST
    jid = credentials = None
    contacts = []
    if request.body:
        try:
            body = json.loads(request.body)
            credentials = body.get('credentials')
            jid = kill_quotes(body.get('JID'), 'int')
            contacts = json.loads(base64.b64decode(body.get('contacts', [])))
        except Exception as e:
            result['error'] = str(e)

    if jid and credentials and contacts:
        reg = Registrations.objects.filter(phone=jid, is_active=True).first()
        if not reg or not reg.get_hash() == credentials:
            return JsonResponse({'error': 'not found'}, safe=False)

        result['jid'] = jid
        result['contacts'] = contacts
        for contact in contacts:
            good_phones = ''
            phones = contact['phones'].split('|')
            for phone in phones:
                phone = kill_quotes(phone, 'int').strip()
                if not len(phone) == 11:
                    continue
                good_phones += '| %s' % phone
            if not good_phones:
                continue
            need_save = False
            analog = DeviceContacts.objects.filter(jid_owner=jid, phones=good_phones).first()
            if not analog:
                analog = DeviceContacts(jid_owner=jid, phones=good_phones)
                need_save = True
            for field in ('display_name', 'given_name', 'middle_name', 'family_name',
                          'company', 'job_title', 'emails', 'postal_addresses', 'birthday'):
                value = getattr(analog, field)
                camel_field = convert2camelcase(field)
                new_value = contact.get(camel_field)
                if not new_value:
                    continue
                new_value = new_value.strip()
                if new_value and new_value != value:
                    setattr(analog, field, new_value)
                    need_save = True
            if need_save:
                analog.save()

    return JsonResponse(result, safe=False)

@csrf_exempt
def notification(request, app_id: str):
    """Апи-метод для отправки пуша
       :param app_id: ид приложения
    """
    return notification_helper(request, app_id=app_id)

@csrf_exempt
def notification_batch(request, app_id: str):
    """Апи-метод для отправки пушей батчем
       :param app_id: ид приложения
    """
    return notification_batch_helper(request, app_id=app_id)
