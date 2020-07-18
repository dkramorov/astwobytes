# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group, Permission
#from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from apps.main_functions.catcher import defiz_phone
from apps.main_functions.functions import object_fields
from apps.main_functions.api_helper import ApiHelper, XlsxHelper
from apps.main_functions.model_helper import create_model_helper, ModelHelper
from apps.main_functions.string_parser import analyze_digit
from apps.main_functions.tabulator import tabulator_filters_and_sorters
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )
from apps.login.models import customUser, ExtraFields

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

@login_required
def api(request, action: str = 'users'):
    """Апи-метод для получения всех данных"""
    mh_vars = users_vars.copy()
    #if action == 'users':
    #    mh_vars = users_vars.copy()

    mh = create_model_helper(mh_vars, request, CUR_APP)
    # Принудительные права на просмотр
    #mh.permissions['view'] = True
    mh.select_related_add('customuser')
    context = mh.context

    rows = mh.standard_show()

    result = []
    for row in rows:
        item = object_fields(row, pass_fields=('password', ))
        item['folder'] = row.customuser.get_folder()
        item['thumb'] = row.customuser.thumb()
        item['name'] = str(row.customuser)
        item['phone'] = row.customuser.phone
        result.append(item)

    result = {'data': result,
              'last_page': mh.raw_paginator['total_pages'],
              'total_records': mh.raw_paginator['total_records'],
              'cur_page': mh.raw_paginator['cur_page'],
              'by': mh.raw_paginator['by'], }
    return JsonResponse(result, safe=False)

def import_xlsx(request, action: str = 'user'):
    """Апи-метод для сохранения данных из excel-файла
                     удаления данных по excel-файлу
       :param request: HttpRequest
       :param action: какую модель использовать
    """
    #if action == 'user':
    #    result = XlsxHelper(request, users_vars, CUR_APP)
    result = XlsxHelper(request, users_vars, CUR_APP,
                        cond_fields = ['username'])
    return result

def welcome(request, *args, **kwargs):
    """Страничка входа в админку - авторизация или приветствие"""
    if not request.user.is_authenticated:
        urla = reverse('%s:login_view' % (CUR_APP, ))
        return redirect(urla)
    context = {}
    return render(request, 'core/welcome.html', context)

def login_view(request, *args, **kwargs):
    """Страничка авторизации"""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
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
    mh = create_model_helper(mh_vars, request, CUR_APP, disable_fas=True)
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

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
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
    context['import_xlsx_url'] = reverse('%s:%s' % (CUR_APP, 'import_xlsx'),
                                         kwargs={'action': 'users'})
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

        # ---------------------------------------
        # Исключение, когда редактируешь сам себя
        # ---------------------------------------
        if action == 'edit' and not mh.permissions['edit']:
            mh.permissions['edit'] = True
            pass_fields = ('password', 'is_active', 'is_staff', 'is_superuser', 'position', )

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
            context['row']['thumb'] = mh.row.customuser.thumb()
            context['row']['imagine'] = mh.row.customuser.imagine()

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def user_perms(request, row_id: int):
    """Права пользователя"""
    mh_vars = users_vars.copy()

    mh = create_model_helper(mh_vars, request, CUR_APP, 'perms')
    context = mh.context
    mh.select_related_add('customuser')

    row = mh.get_row(row_id)
    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                          kwargs={'action': 'edit', 'row_id': mh.row.id})
    # ----
    # POST
    # ----
    if request.method == 'POST':
        result = {}
        if request.user.has_perm('auth.change_user'):
            result['success'] = 'Права обновлены'
            #row.user_permissions.clear()
            perm_list = []
            perms_arr = request.POST.getlist('perm')
            if perms_arr:
                perm_list = Permission.objects.filter(pk__in=perms_arr)
            row.user_permissions.set(perm_list)
        else:
            result['error'] = 'Недостаточно прав'
        return JsonResponse(result, safe=False)

    mh.breadcrumbs_add({
        'link': mh.url_edit,
        'name': '%s %s' % (mh.action_edit, mh.rp_singular_obj),
    })
    edit_perms_link = reverse('%s:%s' % (CUR_APP, 'user_perms'), kwargs={'row_id': mh.row.id})
    mh.breadcrumbs_add({
        'link': edit_perms_link,
        'name': '%s %s' % ('Права', mh.rp_singular_obj),
    })
    context['url_edit'] = edit_perms_link
    context['row'] = mh.row

    user_perms = row.user_permissions.values_list('id', flat=True)
    context['permissions'] = prepare_perm_list(user_perms)

    template = '%sperms.html' % (mh.template_prefix, )
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
    mh.select_related_add('customuser')
    mh_vars = users_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)
    mh.search_fields = ('first_name', 'last_name', 'username', 'customuser__phone')
    rows = mh.standard_show()
    for row in rows:
        name = '%s (%s id=%s)' % (str(row.customuser), row.username, row.id)
        result['results'].append({'text': name, 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}
    return JsonResponse(result, safe=False)

groups_vars = {
    'singular_obj': 'Группа',
    'plural_obj': 'Группы',
    'rp_singular_obj': 'группы',
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

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        result = []
        ids_groups = {row.id: {} for row in rows}
        # Достаем пользователей групп
        users = User.objects.select_related('customuser').filter(groups__in=ids_groups.keys())
        for user in users:
            groups = user.groups.all().values_list('id', flat=True)
            for group in groups:
                if not user.id in ids_groups[group]:
                    ids_groups[group][user.id] = '%s (%s id=%s)' % (str(user.customuser), user.username, user.id)

        for row in rows:
            item = object_fields(row)
            item['actions'] = row.id
            item['users'] = '<br>'.join(ids_groups[row.id].values())
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
def group_perms(request, row_id: int):
    """Права группы пользователей"""
    mh_vars = groups_vars.copy()

    mh = create_model_helper(mh_vars, request, CUR_APP, 'perms')
    context = mh.context

    row = mh.get_row(row_id)
    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                          kwargs={'action': 'edit', 'row_id': mh.row.id})
    # ----
    # POST
    # ----
    if request.method == 'POST':
        result = {}
        if request.user.has_perm('auth.change_group'):
            result['success'] = 'Права обновлены'
            #row.permissions.clear()
            perm_list = []
            perms_arr = request.POST.getlist('perm')
            if perms_arr:
                perm_list = Permission.objects.filter(pk__in=perms_arr)
            row.permissions.set(perm_list)
        else:
            result['error'] = 'Недостаточно прав'
        return JsonResponse(result, safe=False)

    mh.breadcrumbs_add({
        'link': mh.url_edit,
        'name': '%s %s' % (mh.action_edit, mh.rp_singular_obj),
    })
    edit_perms_link = reverse('%s:%s' % (CUR_APP, 'group_perms'), kwargs={'row_id': mh.row.id})
    mh.breadcrumbs_add({
        'link': edit_perms_link,
        'name': '%s %s' % ('Права', mh.rp_singular_obj),
    })
    context['url_edit'] = edit_perms_link
    context['row'] = mh.row

    group_perms = row.permissions.values_list('id', flat=True)
    context['permissions'] = prepare_perm_list(group_perms)

    mh.template_prefix = users_vars['template_prefix']
    template = '%sperms.html' % (mh.template_prefix, )
    return render(request, template, context)

def search_groups(request, *args, **kwargs):
    """Поиск групп пользователей"""
    return search_view(request,
                       model_vars = groups_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', ), )

def prepare_perm_list(cur_perms):
    """Подготовить список всех разрешений,
       проставить имеющиеся разрешения для пользователя/группы
       :param cur_perms: список id разрешений
    """
    perms = {}
    pass_perms = ('content type', 'session', 'custom user', 'permission')
    permissions = Permission.objects.select_related('content_type').all()
    for perm in permissions:
        if not perm.content_type.model_class()._meta.default_permissions:
            continue

        if not perm.content_type.id in perms:
            perms[perm.content_type.id] = {'content_type': perm.content_type, 'perms': []}
        perms[perm.content_type.id]['perms'].append(perm)

    perm_list = [
        {
            'id': perms[perm]['content_type'].id,
            'name': perms[perm]['content_type'].name,
            'perms': perms[perm]['perms'],
        } for perm in sorted(perms.keys())
          if not perms[perm]['content_type'].name in pass_perms]
    for perm in perm_list:
        if perm['name'] == 'group':
            perm['name'] = 'Админка - Группы пользователей'
        elif perm['name'] == 'user':
            perm['name'] = 'Админка - Пользователи'
        perms = []
        for item in perm['perms']:
            if item.codename.startswith('add_'):
                perms.append({
                    'name': 'Добавление',
                    'code': 'create',
                    'id': item.id,
                    'access': item.id in cur_perms,
                })
            elif item.codename.startswith('change_'):
                perms.append({
                    'name': 'Изменение',
                    'code': 'edit',
                    'id': item.id,
                    'access': item.id in cur_perms,
                })
            elif item.codename.startswith('delete_'):
                perms.append({
                    'name': 'Удаление',
                    'code': 'drop',
                    'id': item.id,
                    'access': item.id in cur_perms,
                })
            elif item.codename.startswith('view_'):
                perms.append({
                    'name': 'Просмотр',
                    'code': 'view',
                    # просто, чтобы в шаблоне знать как права называются
                    'codename': item.codename,
                    'id': item.id,
                    'access': item.id in cur_perms,
                })
        perm['perms'] = perms
    perm_list.sort(key=lambda x:x['name'])
    return perm_list

extra_fields_vars = {
    'singular_obj': 'Доп. поле пользователя',
    'plural_obj': 'Доп. поля пользователя',
    'rp_singular_obj': 'доп. поля пользователя',
    'rp_plural_obj': 'доп. полей пользователей',
    'template_prefix': 'extra_fields_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'users',
    'submenu': 'extra_fields',
    'show_urla': 'show_extra_fields',
    'create_urla': 'create_extra_field',
    'edit_urla': 'edit_extra_field',
    'model': ExtraFields,
    'custom_model_permissions': User,
    'select_related_list': ('group', ),
}

@login_required
def show_extra_fields(request, *args, **kwargs):
    """Вывод дополнительных полей пользователя/группы"""
    extra_vars = {}
    return show_view(request,
                     model_vars = extra_fields_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

@login_required
def edit_extra_field(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование дополнительного поля пользователя/группы"""
    return edit_view(request,
                     model_vars = extra_fields_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def extra_fields_positions(request, *args, **kwargs):
    """Изменение позиций доп. полей пользователей/групп"""
    result = {}
    mh_vars = extra_fields_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_extra_fields(request, *args, **kwargs):
    """Поиск в доп. полей пользователей/групп"""
    return search_view(request,
                       model_vars = extra_fields_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', 'field'), )


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
        'chat': 'demo/demo_chat.html',
    }
    context = {}
    context['menu'] = 'demo'
    context['submenu'] = action
    # Шаблон по-умолчанию panels
    template = demos.get(action, demos['dashboard'])

    return render(request, template, context)


