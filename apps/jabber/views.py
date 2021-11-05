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

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.string_parser import kill_quotes, GenPasswd, get_request_ip
from apps.main_functions.date_time import date_plus_days
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from apps.main_functions.files import (check_path,
                                       make_folder,
                                       imageThumb,
                                       extension,
                                       catch_file, )

from apps.jabber.models import Registrations, FirebaseTokens

EJABBERD_LOCAL = 'https://127.0.0.1:5443'.rstrip('/')
FIREBASE_SERVER_KEY_8800 = 'AAAA6p6J3i8:APA91bEY6_SxH2vh-yiyqYY3UmPrKktbHohMFHhTVV38zfeYAKI6PDExh77IW6MiTFRaYobsy8oeSBmgMi0xs9YtEmXmnNo4X10j1dzcvMgrowZoH1hinzAsIJlZEedfpbM_nqz8-ULW'
FIREBASE_SERVER_KEY_223 = 'AAAA2qpHlwc:APA91bGgP-wP2qxq3G7NEZgoH2WYmEzqM2tmcES97c5_Mj6_I8eE9fedMILjI1HycKj_dx8TkubsVvSM82OLMMf7JNErhN722oXLiiAGq6NNnlMe_uVEWaXRc98s-SRcoIg_71AwrMmb'

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

            # Заносим пользователя как отключенного (is_active=False)
            analog = Registrations(is_active=False)
            analog.phone = phone
            analog.code = code
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
        one_hour = date_plus_days(now, minutes=-30)
        analog = Registrations.objects.filter(phone=phone,
                                              code=code,
                                              created__gte=one_hour,
                                              is_active=False).first()
        if analog:
            # Все регистрации делаем неактивными
            Registrations.objects.filter(phone=phone).update(is_active=False, updated=now)
            # Делаем текущую активной
            analog.is_active = True
            analog.save()

            result = object_fields(analog, pass_fields=('passwd', 'code'))
            # Делаем запрос на реальную регистрацию пользователя
            r = requests.post('%s/api/register' % EJABBERD_LOCAL, json={'user': analog.phone, 'host': settings.JABBER_DOMAIN, 'password': analog.passwd}, verify=False)
            try:
                # Добавляем пользователя на свич
                save_user2fs(analog.phone)

                json_data = r.json()
            except Exception as e:
                json_data = None
                result['json_parse_error'] = True
                print(e)

            if json_data:
                result['result'] = json_data
                # '{"status":"error","code":10090,"message":"User 89148959223@anhel.1sprav.ru already registered"}'
                if isinstance(json_data, dict) and json_data['code'] == 10090:
                    r = requests.post('%s/api/change_password' % EJABBERD_LOCAL, json={'user': analog.phone, 'host': settings.JABBER_DOMAIN, 'newpass': analog.passwd}, verify=False)
                    if r.text == '0':
                        status_code = 201 # Пароль изменен
            else:
                result['result'] = r.text
    return JsonResponse(result, safe=False, status=status_code)

@csrf_exempt
def test_notification(request, skey: str = None):
    """Апи-метод для отправки пуша
       TODO: сравнивать айпишники,
       чтобы пуши не могли подделать
       :param skey: серверный ключ firebase для отправки сообщения
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

    # Серверный ключ Firebase
    server_key = FIREBASE_SERVER_KEY_8800
    if skey:
        server_key = skey

    if request.body:
        try:
            body = json.loads(request.body)
        except Exception as e:
            result['error'] = str(e)
        if body:
            credentials = body.get('credentials')
            to_jid = body.get('toJID')
            from_jid = body.get('fromJID')
            msg_body = body.get('body')
            name = body.get('name')
            result['body'] = body
            if 'credentials' in result['body']:
                del result['body']['credentials']

            analog = Registrations.objects.filter(phone=from_jid, is_active=True).first()
            if analog and analog.get_hash() == credentials:
                tokens = list(FirebaseTokens.objects.filter(login=to_jid).values_list('token', flat=True))
            else:
                result['error'] = 'Restricted access'

    text = msg_body or 'Новое сообщение от %s' % from_jid
    if text:
        if len(text) > 30:
            text = '%s...' % text[:30]
    title = name or 'Новое сообщение'

    url = 'https://fcm.googleapis.com/fcm/send'
    data = {
        'data': {
            'sender': from_jid,
            'receiver': to_jid,
        },
        'notification': {
            'title': title,
            'body': text,
        },
        # one recipient
        #'to': to_token,
        'registration_ids': tokens, # many recipient
        'click_action': 'FLUTTER_NOTIFICATION_CLICK',
    }

    headers = {'Authorization': 'key=%s' % server_key}
    if tokens:
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
                            FirebaseTokens.objects.filter(token=token).delete()

        except Exception as e:
            result['error'] = str(e)

        result['result'] = r.text
        result['tokens'] = tokens
    else:
        result['fail'] = 'tokens not found'
    return JsonResponse(result, safe=False)

def get_registered_users():
    """Получение списка всех зарегистрированных пользователей
    """
    r = requests.post('%s/api/registered_users' % EJABBERD_LOCAL, json={'host': settings.JABBER_DOMAIN}, verify=False)
    return r.json()

def save_users2fs():
    """Сохранить/обновить всех пользователей ejabberd
       на сервере телефонии
    """
    users = get_registered_users()
    if not isinstance(users, (list, tuple)):
        print('error: users is not list %s' % users)
        return
    for user in users:
        save_user2fs(user)

def save_user2fs(username: str):
    """После регистрации и/или подтверждения номера,
       надо на свиче синхануть пользователя
       Пользователи сайта /freeswitch/admin/personal_users/
       Обновление происходит по userkey
       телефон_домен - в таком формате шлем пользователя
       :param username: логин пользователя (например, 89999999999)
    """
    endpoint = '/freeswitch/personal_users/sync/'
    user_at_domain = '%s_%s' % (username, settings.JABBER_DOMAIN)
    params = {
        'userkey': user_at_domain,
        'username': user_at_domain,
        'phone': username,
        'phone_confirmed': 10,
    }
    headers = {
        'token': settings.FS_TOKEN,
    }
    r = requests.post('https://%s%s' % (settings.FREESWITCH_DOMAIN, endpoint), data=params, headers=headers)
    #print('save user2fs %s' % user_at_domain)


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
    if app_id == '8800':
        return test_notification(request, skey=FIREBASE_SERVER_KEY_8800)
    elif app_id == '223':
        return test_notification(request, skey=FIREBASE_SERVER_KEY_223)
    return test_notification(request)

