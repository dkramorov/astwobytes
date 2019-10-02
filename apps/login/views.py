# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from apps.main_functions.catcher import defiz_phone
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper, ModelHelper
from apps.main_functions.string_parser import analyze_digit
from apps.main_functions.tabulator import tabulator_filters_and_sorters
from apps.login.models import customUser

# Максимальное кол-во попыток ввести пароль без санкций
MAX_ATTEMPTS = 3
CUR_APP = 'login'
users_vars = {
    'singular_obj': 'Пользователь',
    'plural_obj': 'Пользователи',
    'rp_singular_obj': 'пользователя',
    'rp_plural_obj': 'пользователей',
    'template_prefix': 'users_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'users',
    'submenu': 'users',
    'show_urla': 'show_users',
    'create_urla': 'create_user',
    'edit_urla': 'edit_user',
    'model': User,
}

def welcome(request, *args, **kwargs):
    """Страничка входа в админку - авторизация или приветствие"""
    if not request.user.is_authenticated:
        urla = reverse('%s:login_view' % (CUR_APP, ))
        return redirect(urla)
    context = {}
    return render(request, 'core/base.html', context)

def login_view(request, *args, **kwargs):
    """Страничка авторизации"""
    if request.method == 'POST':
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')
        if username and passwd:
            user = authenticate(request, username=username, password=passwd)
            if user is not None:
                # TODO blink
                if user.is_active:
                    login(request, user)
                    next_page = request.POST.get('next')
                    if next_page:
                        return redirect(next_page)
                    urla = reverse('%s:welcome' % (CUR_APP, ))
                    return redirect(urla)

    attempts_elapsed = MAX_ATTEMPTS
    attempts_elapsed_end = analyze_digit(attempts_elapsed, end=('попытка', 'попыток', 'попытки'))
    next_page = request.GET.get('next')
    context = {'attempts_elapsed': '%s %s' % (attempts_elapsed, attempts_elapsed_end),
               'next': next_page}
    return render(request, 'core/auth_form.html', context)

def logout_view(request, *args, **kwargs):
    """Выход пользователя из админки"""
    urla = reverse('%s:login_view' % (CUR_APP, ))
    logout(request)
    return redirect(urla)

@login_required
def show_users(request, *args, **kwargs):
    """Вывод пользователей админки"""
    mh_vars = users_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('customuser')
    context = mh.context
    # -----------------------
    # Фильтрация и сортировка
    # -----------------------
    filters_and_sorters = tabulator_filters_and_sorters(request, custom_position_field='customuser__position')
    for rfilter in filters_and_sorters['filters']:
        mh.filter_add(rfilter)
    for rsorter in filters_and_sorters['sorters']:
        mh.order_by_add(rsorter)
    context['fas'] = filters_and_sorters['params']

    rows = mh.standard_show()
    # ------------------------
    # Для включения сортировки
    # ------------------------
    if rows:
        rows[0].position = True

    if request.is_ajax():
        result = []
        for row in rows:
            item = object_fields(row, pass_fields=('password', ))
            item['actions'] = row.id
            if row.customuser.phone:
                item['customuser__phone'] = defiz_phone(row.customuser.phone)
            # -------------------------------------
            # OneToOneField связь User с customUser
            # -------------------------------------
            item['customuser'] = object_fields(row.customuser, only_fields=('phone', ))
            item['thumb'] = row.customuser.thumb()
            item['position'] = row.customuser.position
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

def update_user_passwd(request, user):
    """Обновление пароля для пользователя"""
    passwd = request.POST.get('passwd')
    if passwd:
        user.set_password(passwd)
        user.save()

def update_customuser(request, user):
    """Обновление дополнительных полей User в customUser"""
    customuser_vars = {}
    for key, value in request.POST.items():
        if key.startswith('customuser.'):
            customuser_key = key.replace('customuser.', '')
            customuser_vars[customuser_key] = value
    for key, value in customuser_vars.items():
        setattr(user.customuser, key, value)
    user.customuser.save()

@login_required
def edit_user(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование пользователя админки"""
    mh_vars = users_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    context = mh.context
    mh.select_related_add('customuser')

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
                if row.is_superuser:
                    context['error'] = 'Нельзя удалить суперпользователя'
                else:
                    row.delete()
                    mh.row = None
                    context['success'] = '%s удален' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'

    elif request.method == 'POST':
        pass_fields = ('password', )
        mh.post_vars(pass_fields=pass_fields)

        if action == 'create' or (action == 'edit' and row):
            if action == 'create':
                if mh.permissions['create']:
                    analogs = User.objects.filter(username=mh.row_vars['username'])
                    if not analogs:
                        mh.row = mh.model()
                        mh.save_row()
                        update_user_passwd(request, mh.row)
                        update_customuser(request, mh.row)
                        context['success'] = 'Данные успешно записаны'
                    else:
                        context['error'] = 'Логин занят'
                else:
                    context['error'] = 'Недостаточно прав'
            if action == 'edit':
                if mh.permissions['edit']:
                    mh.save_row(pass_fields=('username', ))
                    update_user_passwd(request, mh.row)
                    update_customuser(request, mh.row)
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            # ------------------------------
            # Загрузка изображения по ссылке
            # ------------------------------
            if hasattr(mh.row, 'customuser'):
                mh.uploads(row = mh.row.customuser)
        # --------------------
        # Загрузка изображения
        # --------------------
        elif action == 'img' and request.FILES and mh.row:
            if hasattr(mh.row, 'customuser'):
                mh.uploads(mh.row.customuser)

    if mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['redirect'] = mh.url_edit
        # -------------------------------------
        # OneToOneField связь User с customUser
        # -------------------------------------
        if hasattr(mh.row, 'customuser'):
            context['row']['customuser'] = object_fields(mh.row.customuser, pass_fields=('user', ))
            context['row']['customuser']['thumb'] = mh.row.customuser.thumb()

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def check_username(request, *args, **kwargs):
    """Проверка на занятость логина
       (например, при создании/редактировании пользователя)"""
    context = {}
    username = request.GET.get('username')
    if not username:
        context['error'] = 'Пустое имя пользователя'
    else:
        analogs = User.objects.filter(username=username)
        if analogs:
            context['error'] = 'Имя пользователя занято'
        else:
            context['success'] = 1
    return JsonResponse(context, safe=False)

@login_required
def users_positions(request, *args, **kwargs):
    """Изменение позиций пользователей"""
    result = {}
    mh_vars = users_vars.copy()
    # -----------------------------------------
    # Нестандартная сортировка, т/к сортировать
    # нужно связную модель user.customuser
    # -----------------------------------------
    positions = []
    if request.method == 'POST':
        positions = request.POST.getlist('positions[]')
    elif request.method == 'GET':
        positions = request.GET.getlist('positions[]')
    ids_customuser = dict(User.objects.filter(pk__in=positions).values_list('id', 'customuser__id'))
    ids = []
    for position in positions:
        position = int(position)
        if position in ids_customuser:
            ids.append(ids_customuser[position])
    mh_vars['model'] = customUser
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions(custom_positions = ids)
    return JsonResponse(result, safe=False)

def search_users(request, *args, **kwargs):
    """Поиск пользователей"""
    result = {'results': []}

    mh = ModelHelper(User, request)
    mh_vars = users_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)

    mh.search_fields = ('first_name', 'last_name', 'username', 'customuser__phone')
    rows = mh.standard_show()

    for row in rows:
        result['results'].append({'text': '%s' % (row, ), 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}

    return JsonResponse(result, safe=False)

groups_vars = {
    'singular_obj': 'Группа',
    'plural_obj': 'Группы',
    'rp_singular_obj': 'группу',
    'rp_plural_obj': 'групп',
    'template_prefix': 'groups_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'users',
    'submenu': 'groups',
    'show_urla': 'show_groups',
    'create_urla': 'create_group',
    'edit_urla': 'edit_group',
    'model': Group,
}

@login_required
def show_groups(request, *args, **kwargs):
    """Вывод групп пользователей админки"""
    mh_vars = groups_vars.copy()
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

    rows = mh.standard_show()

    if request.is_ajax():
        result = []
        for row in rows:
            item = object_fields(row)
            item['actions'] = row.id
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
def edit_group(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование группы пользователей админки"""
    mh_vars = groups_vars.copy()
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
        pass_fields = ('password', )
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
            #mh.row.user_set.set([request.user, ])
            if mh.row:
                # -------------------------------
                # Сохранение пользователей группы
                # -------------------------------
                group_users = request.POST.getlist('group_users')
                users = User.objects.filter(pk__in=group_users)
                mh.row.user_set.set(users)
    if mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        context['row'] = object_fields(mh.row)
        users = mh.row.user_set.select_related('customuser').all()
        pass_fields = ('password', 'customuser')
        context['row']['users'] = [{
            'user': '%s' % (customUser.get_name(user), ),
            'id': user.id,
        } for user in users]
        context['redirect'] = mh.url_edit

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def demo(request, action='panels'):
    """Демонстрация возможностей дизайна админки"""
    demos = {
        'dashboard': 'demo/demo_dashboard.html',

        'panels': 'demo/demo_panels.html',
        'portlets': 'demo/demo_portlets.html',
        'buttons': 'demo/demo_buttons.html',
        'icons': 'demo/demo_icons.html',
        'notifications': 'demo/demo_notifications.html',
        'typo': 'demo/demo_typo.html',
        'grid': 'demo/demo_grid.html',
        'grid_mansory': 'demo/demo_grid_mansory.html',
        'animations': 'demo/demo_animations.html',
        'dropdown_animations': 'demo/demo_dropdown_animations.html',
        'widgets': 'demo/demo_widgets.html',
        'spinners': 'demo/demo_spinners.html',

        'tables': 'demo/demo_tables.html',

        'standard_forms': 'demo/demo_standard_forms.html',
        'form_wizards': 'demo/demo_form_wizards.html',
        'form_validation': 'demo/demo_form_validation.html',
        'extended_forms': 'demo/demo_extended_forms.html',

        'calendar': 'demo/demo_calendar.html',
    }
    context = {}
    context['menu'] = 'demo'
    context['submenu'] = action
    # Шаблон по-умолчанию panels
    template = demos.get(action, demos['dashboard'])

    return render(request, template, context)
