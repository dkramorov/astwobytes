# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.tabulator import tabulator_filters_and_sorters

from .models import Redirects, CdrCsv, FSUser, PhonesWhiteList

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
    mh_vars = redirects_vars.copy()
    #if action == 'files':
    #    mh_vars = files_vars.copy()

    mh = create_model_helper(mh_vars, request, CUR_APP)
    # Принудительные права на просмотр
    mh.permissions['view'] = True
    context = mh.context

    rows = mh.standard_show()

    result = []
    for row in rows:
        item = object_fields(row)
        item['folder'] = row.get_folder()
        result.append(item)

    result = {'data': result,
              'last_page': mh.raw_paginator['total_pages'],
              'total_records': mh.raw_paginator['total_records'],
              'cur_page': mh.raw_paginator['cur_page'],
              'by': mh.raw_paginator['by'], }
    return JsonResponse(result, safe=False)

@login_required
def show_redirects(request, *args, **kwargs):
    """Вывод переадресаций"""
    mh_vars = redirects_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    context = mh.context

    # -----------------------
    # Фильтрация и сортировка
    # -----------------------
    filters_and_sorters = tabulator_filters_and_sorters(request)
    for rfilter in filters_and_sorters['filters']:
        mh.filter_add(rfilter)
    for rsorter in filters_and_sorters['sorters']:
        mh.order_by_add(rsorter)
    context['fas'] = filters_and_sorters['params']

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        result = []
        for row in rows:
            item = object_fields(row)
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
def edit_redirect(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование переадресации"""
    mh_vars = redirects_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    context = mh.context

    row = mh.get_row(row_id)
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

        if action == 'create' or (action == 'edit' and row):
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
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['redirect'] = mh.url_edit

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

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
    filters_and_sorters = tabulator_filters_and_sorters(request)
    for rfilter in filters_and_sorters['filters']:
        mh.filter_add(rfilter)
    for rsorter in filters_and_sorters['sorters']:
        mh.order_by_add(rsorter)
    context['fas'] = filters_and_sorters['params']

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        result = []
        for row in rows:
            item = object_fields(row)
            item['folder'] = row.created.strftime('%Y-%m-%d')
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
    context = mh.context

    # -----------------------
    # Фильтрация и сортировка
    # -----------------------
    filters_and_sorters = tabulator_filters_and_sorters(request)
    for rfilter in filters_and_sorters['filters']:
        mh.filter_add(rfilter)
    for rsorter in filters_and_sorters['sorters']:
        mh.order_by_add(rsorter)
    context['fas'] = filters_and_sorters['params']

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        result = []
        for row in rows:
            item = object_fields(row)
            user = item['user']
            item['user'] = user.username
            item['user__username'] = user.username

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
    context = mh.context

    row = mh.get_row(row_id)
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
        mh.row_vars['user'] = User.objects.filter(pk=mh.row_vars['user']).first()

        if action == 'create' or (action == 'edit' and row):
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
        context['row'] = object_fields(mh.row, pass_fields=())
        context['redirect'] = mh.url_edit
        user = context['row']['user']
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
    'singular_obj': 'Белый список телефонов',
    'plural_obj': 'Белые списки телефонов',
    'rp_singular_obj': 'телефона',
    'rp_plural_obj': 'телефонов',
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
    mh_vars = phones_white_list_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    context = mh.context

    # -----------------------
    # Фильтрация и сортировка
    # -----------------------
    filters_and_sorters = tabulator_filters_and_sorters(request)
    for rfilter in filters_and_sorters['filters']:
        mh.filter_add(rfilter)
    for rsorter in filters_and_sorters['sorters']:
        mh.order_by_add(rsorter)
    context['fas'] = filters_and_sorters['params']

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        result = []
        for row in rows:
            item = object_fields(row)
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
def edit_phones_white_list(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование белого списка телефонов для динамического диалплана"""
    mh_vars = phones_white_list_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    context = mh.context

    row = mh.get_row(row_id)
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

        if action == 'create' or (action == 'edit' and row):
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
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['redirect'] = mh.url_edit

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def phones_white_list_positions(request, *args, **kwargs):
    """Изменение позиций файлов"""
    result = {}
    mh_vars = phones_white_list_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)
