# -*- coding:utf-8 -*-
import os
import json
import requests
import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from oauth2client.service_account import ServiceAccountCredentials
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.string_parser import kill_quotes, GenPasswd, get_request_ip
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

from apps.jabber.models import Registrations, FirebaseTokens

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
                     row_id = row_id,
                     extra_vars = None, )

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

def search_registrations(request, *args, **kwargs):
    """Поиск токенов
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = tokens_vars,
                       cur_app = CUR_APP,
                       sfields = ('login', 'token'), )

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
        analog.login = phone
        analog.ip = get_request_ip(request)
        analog.save()

    elif action == 'registration' and phone:
        if len(phone) == 11 and phone[0] == '8' and phone[1] == '9':

            code = '0000'
            for i in range(10):
                code = GenPasswd(4, '1234567890')
                if not code.startswith('0'):
                    break

            platform = method.get('platform')
            version = method.get('version')
            passwd = method.get('passwd')
            name = method.get('name')

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

            # Скрипт отправляет на свич телефон и код,
            # свич звонит и диктует
            params = {
                'phone': phone,
                'digit': code,
            }
            uri = '%s/freeswitch/sms_service/say_code/' % settings.FREESWITCH_DOMAIN
            if not uri.startswith('https://'):
                uri = 'https://%s' % uri

            # Не ждем, завершаем запрос сразу,
            # запрос будет долгий, пока не завершится звонок
            try:
                r = requests.get(uri, params=params, timeout=(5, 0.1))
            except Exception as e:
                return JsonResponse(result, safe=False, status=status_code)

    elif action == 'confirm' and phone:
        code = method.get('code')
        # Берем только за последний час попытку регистрации
        now = datetime.datetime.now()
        long_ago = date_plus_days(now, minutes=-30)
        analog = Registrations.objects.filter(phone=phone,
                                              code=code,
                                              created__gte=long_ago,
                                              is_active=False).first()
        if analog:
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
            reg_result = reg_user_on_jabber(analog.phone, analog.passwd)
            status_code = reg_result['code']
            result['result'] = reg_result['msg']

    return JsonResponse(result, safe=False, status=status_code)

def reg_user_on_jabber(phone: str, passwd: str):
    """Регистрация пользователя на джаббере,
       либо смена пароля, если пользователь имеется
       :param phone: телефон
       :param passwd: пароль
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
                return {
                    'msg': 'Пароль пользователя %s успешно изменен' % phone,
                    'code': 201,
                }
        elif 'successfully registered' in reg_obj:
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

def trim_firebase_message(text):
    """Срезать размер текста в сообщении
       :param text: текст сообщения
    """
    if text:
        if len(text) > 30:
            text = '%s...' % text[:30]
    return text


@csrf_exempt
def notification_helper(request, app_id: str = None):
    """Апи-метод для отправки уведомления (пуша)
       https://firebase.google.com/docs/cloud-messaging/migrate-v1
       :param request: HttpRequest
       :param app_id: ид приложения (для получения файла json с ключем)
    """
    result = {}
    ip_white_list = ['138.68.109.138']
    user_ip = get_request_ip(request)
    result['user_ip'] = user_ip

    method = request.GET if request.method == 'GET' else request.POST
    body = None
    tokens = []

    to_token = None
    to_jid = None
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

    text = trim_firebase_message(msg_body or 'Новое сообщение от %s' % from_jid)
    title = name or 'Новое сообщение'
    url = url = get_firebase_messaging_url(app_id=app_id)
    headers = get_firebase_messaging_headers(app_id=app_id)
    # С ибучим api v 1 нельзя registration_ids, нужно использовать группы или топики
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
        },
    }
    if only_data:
        data = {
            'message': {
                'data': {
                    'sender': from_jid,
                    'receiver': to_jid,
                },
            },
        }
    data['message']['android'] = {
        'priority': 'high',
    }
    if additional_data and isinstance(additional_data, dict):
        for k, v in additional_data.items():
            data['message']['data'][k] = v
    for token in tokens:
        data['message']['token'] = token
        r = requests.post(url, json=data, headers=headers)
        resp = r.text
        try:
            resp = json.loads(r.text)
        except Exception as e:
            result['json_error_response'] = str(e)
        result[token] = resp
        if isinstance(result[token], dict):
            if 'error' in result[token]:
                if result[token]['error'].get('code') in (403, 404):
                    FirebaseTokens.objects.filter(token=token).delete()
                    result[token]['DELETED'] = True
    if not tokens:
        result['fail'] = 'tokens not found'
    result['url'] = url
    result['app_id'] = app_id
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
    media_folder = 'jabber_avatars'
    phone = request.POST.get('phone')
    credentials = request.POST.get('credentials')

    #result['phone'] = phone
    #result['credentials'] = credentials

    if request.FILES.get('file') and phone and credentials:
        analog = Registrations.objects.filter(phone=phone, is_active=True).first()
        img = request.FILES['file']
        ext = extension(img.name)

        #result['hash'] = analog.get_hash() if analog else ''
        #result['analog_phone'] = analog.phone if analog else ''

        if ext and analog and analog.get_hash() == credentials:
            if check_path(media_folder):
                make_folder(media_folder)
            path = os.path.join(media_folder, '%s%s' % (phone, ext))
            if catch_file(img, path):
                # тут мб ошибка, пусть будет, что грузанули
                #result['thumb'] = imageThumb(path, 1920, 1280)
                result['url'] = 'https://%s/media/%s' % (request.META['HTTP_HOST'], path)
            else:
                result['error'] = 'Не удалось сохранить файл'
        else:
            result['error'] = 'Пользователь не идентифицирован'
    else:
        result['error'] = 'Файл не отправлен'

    return JsonResponse(result, safe=False)

@csrf_exempt
def notification(request, app_id: int):
    """Апи-метод для отправки пуша
       :param app_id: ид приложения
    """
    return notification_helper(request, app_id=app_id)

