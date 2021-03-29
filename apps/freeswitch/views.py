# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Q

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import ModelHelper, create_model_helper
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from .models import Redirects, CdrCsv, FSUser, PhonesWhiteList, PersonalUsers
from .backend import FreeswitchBackend
from .services import voice_code

CUR_APP = 'freeswitch'
redirects_vars = {
    'singular_obj': 'Переадресация',
    'plural_obj': 'Переадресации',
    'rp_singular_obj': 'переадресации',
    'rp_plural_obj': 'переадресаций',
    'template_prefix': 'redirects_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'freeswitch',
    'submenu': 'redirects',
    'show_urla': 'show_redirects',
    'create_urla': 'create_redirect',
    'edit_urla': 'edit_redirect',
    'model': Redirects,
}

def api(request, action: str = 'redirects'):
    """Апи-метод для получения всех данных"""
    if action == 'phones_white_list':
        result = ApiHelper(request, phones_white_list_vars, CUR_APP)
    elif action == 'cdr_csv':
        restrictions = []
        app_label = cdrcsv_vars['model']._meta.app_label
        model_name = cdrcsv_vars['model']._meta.model_name
        if not request.user.has_perm('%s.view_%s' % (app_label, model_name)):
            personal_user_id = request.headers.get('token', 0)
            restrictions.append(Q(personal_user_id=personal_user_id))
        result = ApiHelper(request, cdrcsv_vars, CUR_APP, restrictions=restrictions)
    else:
        result = ApiHelper(request, redirects_vars, CUR_APP)
    return result

@login_required
def show_redirects(request, *args, **kwargs):
    """Вывод переадресаций"""
    return show_view(request,
                     model_vars = redirects_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_redirect(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование переадресации"""
    return edit_view(request,
                     model_vars = redirects_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def redirects_positions(request, *args, **kwargs):
    """Изменение позиций файлов"""
    result = {}
    mh_vars = redirects_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

cdrcsv_vars = {
    'singular_obj': 'Звонок',
    'plural_obj': 'Звонки',
    'rp_singular_obj': 'звонка',
    'rp_plural_obj': 'звонков',
    'template_prefix': 'cdrcsv_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'freeswitch',
    'submenu': 'cdrcsv',
    'show_urla': 'show_cdrcsv',
    'model': CdrCsv,
}

@login_required
def show_cdrcsv(request, *args, **kwargs):
    """Вывод звонков"""
    mh_vars = cdrcsv_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    context = mh.context

    # -----------------------
    # Фильтрация и сортировка
    # -----------------------
    if not mh.filters_and_sorters['sorters']:
        mh.filters_and_sorters['params']['sorters']['created'] = 'desc'
        for rsorter in mh.filters_and_sorters['sorters']:
            mh.order_by_add(rsorter)

    cache_var_sip_codes = 'sip_codes_cache'
    cache_time_sip_codes = 3600
    sip_codes = cache.get(cache_var_sip_codes)
    if not sip_codes:
        sip_codes = CdrCsv.objects.values_list('state', flat=True).distinct()
        cache.set(cache_var_sip_codes, sip_codes, cache_time_sip_codes)
    context['sip_codes'] = sip_codes

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        result = []
        for row in rows:
            item = object_fields(row)
            #item['folder'] = row.created.strftime('%Y-%m-%d')
            item['record'] = row.get_record_path()
            result.append(item)

        if request.GET.get('page'):
            result = {'data': result,
                      'last_page': mh.raw_paginator['total_pages'],
                      'total_records': mh.raw_paginator['total_records'],
                      'cur_page': mh.raw_paginator['cur_page'],
                      'by': mh.raw_paginator['by'], }
        return JsonResponse(result, safe=False)
    template = '%stable.html' % (mh.template_prefix, )
    return render(request, template, context)

call_from_site_vars = {
    'singular_obj': 'Звонок с сайта',
    'plural_obj': 'Звонки с сайта',
    'rp_singular_obj': 'звонка с сайта',
    'rp_plural_obj': 'звонков с сайта',
    'template_prefix': 'call_from_site_',
    'action_create': 'Тест',
    'action_edit': '',
    'action_drop': '',
    'menu': 'freeswitch',
    'submenu': 'call_from_site',
    'show_urla': 'call_from_site',
    'model': None,
}

@login_required
def call_from_site(request, *args, **kwargs):
    """Звонок из браузера"""
    mh_vars = call_from_site_vars.copy()
    template = 'call_from_site.html'
    context = {key: value for key, value in mh_vars.items()}
    breadcrumbs = [{
        'name': 'Виртуальная АТС',
        'link': 'javascript:void(0);',
    },
    {
        'name': mh_vars['singular_obj'],
        'link': 'javascript:void(0);',
    }]
    context.update({
        'breadcrumbs': breadcrumbs,
        'freeswitch_domain': settings.FREESWITCH_DOMAIN,
        'freeswitch_wss': settings.FREESWITCH_WSS,
    })
    return render(request, template, context)

callcenter_vars = {
    'singular_obj': 'Коллцентр',
    'plural_obj': 'Коллцентр',
    'rp_singular_obj': 'коллцентр',
    'rp_plural_obj': 'коллцентр',
    'template_prefix': 'callcenter_',
    'action_create': 'Тест',
    'action_edit': '',
    'action_drop': '',
    'menu': 'freeswitch',
    'submenu': 'callcenter',
    'show_urla': 'callcenter',
    'model': None,
}

@login_required
def callcenter(request, *args, **kwargs):
    """Коллцентр в браузере"""
    mh_vars = callcenter_vars.copy()
    template = 'callcenter.html'
    context = {key: value for key, value in mh_vars.items()}
    breadcrumbs = [{
        'name': 'Виртуальная АТС',
        'link': 'javascript:void(0);',
    },
    {
        'name': mh_vars['singular_obj'],
        'link': 'javascript:void(0);',
    }]
    context.update({
        'breadcrumbs': breadcrumbs,
        'freeswitch_domain': settings.FREESWITCH_DOMAIN,
        'freeswitch_wss': settings.FREESWITCH_WSS,
    })
    return render(request, template, context)

users_vars = {
    'singular_obj': 'Пользователь АТС',
    'plural_obj': 'Пользователи АТС',
    'rp_singular_obj': 'пользователя АТС',
    'rp_plural_obj': 'пользователей АТС',
    'template_prefix': 'fs_users_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'freeswitch',
    'submenu': 'fs_users',
    'show_urla': 'show_users',
    'create_urla': 'create_user',
    'edit_urla': 'edit_user',
    'model': FSUser,
}

@login_required
def show_users(request, *args, **kwargs):
    """Вывод пользователей АТС"""
    mh_vars = users_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('user')
    mh.select_related_add('personal_user')
    context = mh.context

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        result = []
        for row in rows:
            item = object_fields(row)
            user = item['user']
            item['user'] = user['username']
            item['user__username'] = user['username']

            personal_user = item['personal_user']
            if personal_user:
                item['personal_user'] = personal_user['username']
                item['personal_user__username'] = personal_user['username']

            item['actions'] = row.id
            item['folder'] = row.get_folder()
            result.append(item)

        if request.GET.get('page'):
            result = {'data': result,
                      'last_page': mh.raw_paginator['total_pages'],
                      'total_records': mh.raw_paginator['total_records'],
                      'cur_page': mh.raw_paginator['cur_page'],
                      'by': mh.raw_paginator['by'], }
        return JsonResponse(result, safe=False)
    template = '%stable.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def edit_user(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование пользователя АТС"""
    mh_vars = users_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('user')
    mh.select_related_add('personal_user')
    row = mh.get_row(row_id)
    context = mh.context

    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))

    if request.method == 'GET':
        if action == 'create':
            mh.breadcrumbs_add({
                'link': mh.url_create,
                'name': '%s %s' % (mh.action_create, mh.rp_singular_obj),
            })
        elif action == 'edit' and row:
            mh.breadcrumbs_add({
                'link': mh.url_edit,
                'name': '%s %s' % (mh.action_edit, mh.rp_singular_obj),
            })
        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удален' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'

    elif request.method == 'POST':
        pass_fields = ()
        mh.post_vars(pass_fields=pass_fields)
        #mh.row_vars['user'] = User.objects.filter(pk=mh.row_vars['user']).first()
        #mh.row_vars['personal_user'] = PersonalUsers.objects.filter(pk=mh.row_vars['personal_user']).first()

        # Если есть аналоги - не сохраняем
        isError = False
        analogs = FSUser.objects.filter(user=mh.row_vars['user'])
        if mh.row:
            analogs = analogs.exclude(pk=mh.row.id)
        if analogs:
            context['error'] = 'Этот пользователь уже создан'
            isError = True

        if not isError and (action == 'create' or (action == 'edit' and row)):
            if action == 'create':
                if mh.permissions['create']:
                    mh.row = mh.model()
                    mh.save_row()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            if action == 'edit':
                if mh.permissions['edit']:
                    mh.save_row()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'

    if mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        context['row'] = object_fields(mh.row, pass_fields=('user', 'personal_user'))
        context['redirect'] = mh.get_url_edit()
        personal_user = mh.row.personal_user
        if personal_user:
            context['row']['personal_user'] = object_fields(personal_user, pass_fields=('password', ))
        user = mh.row.user
        if user:
            context['row']['user'] = object_fields(user, pass_fields=('password', ))

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def users_positions(request, *args, **kwargs):
    """Изменение позиций пользователей АТС"""
    result = {}
    mh_vars = users_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

monitoring_vars = {
    'singular_obj': 'Мониторинг',
    'plural_obj': 'Мониторинг',
    'rp_singular_obj': 'мониторинг',
    'rp_plural_obj': 'мониторинг',
    'template_prefix': 'monitoring_',
    'action_create': 'Тест',
    'action_edit': '',
    'action_drop': '',
    'menu': 'freeswitch',
    'submenu': 'monitoring',
    'show_urla': 'monitoring',
    'model': None,
}

@login_required
def monitoring(request, *args, **kwargs):
    """Мониторинг колцентра в браузере"""
    if request.is_ajax():
        context = {}
        action = None
        if request.method == 'GET':
            action = request.GET.get('action')
        elif request.method == 'POST':
            action = request.POST.get('action')
        fs = FreeswitchBackend(settings.FREESWITCH_URI)
        if action == 'monitoring':
            context = {
                'registrations': fs.get_registrations(),
                'channels': fs.get_channels(),
                'calls': fs.get_bridged_calls(),
            }
        elif action == 'drop_channel' and request.user.is_superuser:
            channel = request.POST.get('uuid')
            if channel:
                output = fs.kill_channel(channel)
                context['output'] = output
        return JsonResponse(context, safe=False)

    mh_vars = monitoring_vars.copy()
    template = 'call_monitoring.html'
    context = {key: value for key, value in mh_vars.items()}
    breadcrumbs = [{
        'name': 'Виртуальная АТС',
        'link': 'javascript:void(0);',
    },
    {
        'name': mh_vars['singular_obj'],
        'link': 'javascript:void(0);',
    }]
    context.update({
        'breadcrumbs': breadcrumbs,
    })
    return render(request, template, context)

phones_white_list_vars = {
    'singular_obj': 'Телефон CRM',
    'plural_obj': 'Телефоны CRM',
    'rp_singular_obj': 'телефона CRM',
    'rp_plural_obj': 'телефонов CRM',
    'template_prefix': 'phones_white_list_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'freeswitch',
    'submenu': 'phones_white_list',
    'show_urla': 'show_phones_white_list',
    'create_urla': 'create_phones_white_list',
    'edit_urla': 'edit_phones_white_list',
    'model': PhonesWhiteList,
}

@login_required
def show_phones_white_list(request, *args, **kwargs):
    """Вывод белого списка телефонов для динамического диалплана"""
    return show_view(request,
                     model_vars = phones_white_list_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_phones_white_list(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование белого списка телефонов
       для динамического диалплана
    """
    return edit_view(request,
                     model_vars = phones_white_list_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def phones_white_list_positions(request, *args, **kwargs):
    """Изменение позиций телефонов из CRM"""
    result = {}
    mh_vars = phones_white_list_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)


personal_users_vars = {
    'singular_obj': 'Пользователь сайта',
    'plural_obj': 'Пользователи сайта',
    'rp_singular_obj': 'пользователя сайта',
    'rp_plural_obj': 'пользователей сайта',
    'template_prefix': 'personal_users_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'freeswitch',
    'submenu': 'personal_users',
    'show_urla': 'show_personal_users',
    'create_urla': 'create_personal_user',
    'edit_urla': 'edit_personal_user',
    'model': PersonalUsers,
}

@login_required
def show_personal_users(request, *args, **kwargs):
    """Вывод белого списка телефонов для динамического диалплана"""
    return show_view(request,
                     model_vars = personal_users_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_personal_user(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование пользвателей
       с сайта для динамического диалплана
       Они загружаются автоматом,
       поэтому вьюха декоративная"""
    return edit_view(request,
                     model_vars = personal_users_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def personal_users_positions(request, *args, **kwargs):
    """Изменение позиций пользователей с сайта
       Они загружаются автоматом, поэтому смысла мало"""
    result = {}
    mh_vars = personal_users_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_personal_users(request, *args, **kwargs):
    """Поиск пользователей сайта"""
    return search_view(request,
                       model_vars = personal_users_vars,
                       cur_app = CUR_APP,
                       sfields = ('username', 'userid', 'userkey'), )

def is_phone_in_white_list(request):
    """Апи-метод, чтобы узнать,
       находится ли телефон в белом списке
       для динамического диалплана"""
    result = {}
    phone = request.GET.get('phone', '')
    if not phone:
        return JsonResponse({'error': 'phone absent'})

    if phone.startswith('83952') or phone.startswith('8800'):
        result['success'] = True

    user_key = request.GET.get('user_key')
    if user_key:
        analog = PersonalUsers.objects.select_related('personal_fs_user').filter(userkey=user_key).first()
        if analog:
            cid = None
            if hasattr(analog, 'personal_fs_user') and analog.personal_fs_user.is_active:
                result['success'] = True
                cid = analog.personal_fs_user.cid
            elif analog.phone_confirmed and analog.phone:
                cid = analog.phone
            if cid:
                if len(cid) == 11 and cid.startswith('8'):
                    result['cid'] = '7%s' % (cid[1:], )
    # ---------------------
    # user_id is DEPRICATED
    # ---------------------
    user_id = request.GET.get('user_id')
    if user_id and not user_key:
        try:
            user_id = int(user_id)
        except ValueError:
            user_id = None
        if user_id:
            analog = PersonalUsers.objects.select_related('personal_fs_user').filter(userid=user_id).first()
            if analog:
                cid = None
                if hasattr(analog, 'personal_fs_user') and analog.personal_fs_user.is_active:
                    result['success'] = True
                    cid = analog.personal_fs_user.cid
                elif analog.phone_confirmed and analog.phone:
                    cid = analog.phone
                if cid:
                    if len(cid) == 11 and cid.startswith('8'):
                        result['cid'] = '7%s' % (cid[1:], )
    if not 'success' in result:
        analog = PhonesWhiteList.objects.filter(phone=phone).first()
        if analog:
            result['success'] = True
    return JsonResponse(result, safe=False)

def send_sms(request):
    """Апи-метод, чтобы отправить sms через spamcha,
       1) достаем из spamcha телефоны для рассылки,
          смотрим по лимитам кто может отправить смс,
          следим за балансировкой - кто сколько отправил
       2) у нас должен работать sms_hub.py на порту (5009)
          подключаемся в него и отправляем смс на телефон
    """
    from apps.spamcha.sms_helper import send_sms_helper
    result = send_sms_helper(request)

    return JsonResponse(result, safe=False)

def say_code(request):
    """Апи-метод, чтобы позвонить на телефон и продиктовать код
       :param dest: номер назначение
       :param digit: число, которое сообщаем в назначение
       Вызывается скрипт hello/say_digit.py
    """
    result = {}
    dest = request.GET.get('phone')
    digit = request.GET.get('digit')
    result['result'] = voice_code(dest=dest, digit=digit)
    return JsonResponse(result, safe=False)

@csrf_exempt
def sync_personal_users(request):
    """Апи-метод, чтобы синхронизировать пользователя
       В настройках ставим токен, чтобы никто не абибал нас
    """
    result = {}
    token = settings.FS_TOKEN
    if not request.headers.get('token') == token:
        return JsonResponse(result, safe=False)

    if request.method == 'POST':
        userkey = request.POST.get('userkey')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        phone_confirmed = request.POST.get('phone_confirmed')

        userkey = request.POST.get('userkey')
        if userkey:
            analog = PersonalUsers.objects.filter(userkey=userkey).first()
            if not analog:
                analog = PersonalUsers(userkey=userkey)
            analog.username = username
            analog.phone = phone
            analog.phone_confirmed = phone_confirmed
            analog.save()

        # user_id is DEPRICATED
        userid = request.POST.get('userid')
        if userid and not userkey:
            analog = PersonalUsers.objects.filter(userid=userid).first()
            if not analog:
                analog = PersonalUsers(userid=userid)
            analog.username = username
            analog.phone = phone
            analog.phone_confirmed = phone_confirmed
            analog.save()
    return JsonResponse(result, safe=False)
