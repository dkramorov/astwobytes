# -*- coding:utf-8 -*-
import json
import time
import random
import os

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, Template
from django.conf import settings

from apps.main_functions.files import check_path, full_path, file_size
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.tabulator import tabulator_filters_and_sorters

from .models import (SpamTable,
                     SpamRow,
                     EmailAccount,
                     EmailBlackList, )

CUR_APP = 'spamcha'
root_breadcrumbs = {'name': 'Email-рассылка', 'link': ''}
spam_tables_vars = {
    'singular_obj': 'Таблица рассылки',
    'plural_obj': 'Таблицы рассылки',
    'rp_singular_obj': 'таблицы рассылки',
    'rp_plural_obj': 'таблиц рассылки',
    'template_prefix': 'spam_tables_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'spamcha',
    'submenu': 'spam_tables',
    'show_urla': 'show_spam_tables',
    'create_urla': 'create_spam_table',
    'edit_urla': 'edit_spam_table',
    'model': SpamTable,
}

def api(request, action: str = 'spam_tables_vars'):
    """Апи-метод для получения всех данных"""
    mh_vars = spam_tables_vars.copy()
    if action == 'spam_tables':
        mh_vars = spam_tables_vars.copy()
    elif action == 'spam_rows':
        mh_vars = spam_rows_vars.copy()
    elif action == 'email_accounts':
        mh_vars = email_accounts_vars.copy()
    elif action == 'black_list':
        mh_vars = black_list_vars.copy()

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
def show_spam_tables(request, *args, **kwargs):
    """Вывод таблиц рассылок"""
    mh_vars = spam_tables_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.breadcrumbs.insert(0, root_breadcrumbs)
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
def edit_spam_table(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование файла"""
    mh_vars = spam_tables_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.breadcrumbs.insert(0, root_breadcrumbs)
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
        elif action == 'html':
            context = {'row': mh.row}
            template = 'spam_constructor.html'
            return render(request, template, context)
        elif action == 'html_result':
            html = mh.row.html_msg
            if not html:
                with open(os.path.join(settings.STATIC_ROOT, 'constructor', 'default', 'index.html')) as f:
                    html = f.read()
            context = RequestContext(request, {})
            template = Template(html)
            return HttpResponse(template.render(context))

    elif request.method == 'POST':
        pass_fields = ('html_msg', )
        mh.post_vars(pass_fields=pass_fields)

        if action == 'create' or (action == 'edit' and row):
            if action == 'create':
                if mh.permissions['create']:
                    mh.row = mh.model()
                    mh.save_row()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            else:
                if mh.permissions['edit']:
                    mh.save_row()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
        elif action == 'html':
            if mh.permissions['edit']:
                mh.row.html_msg = request.POST.get('html_msg')
                mh.row.save()
            return redirect(reverse('%s:%s' % (CUR_APP, 'edit_spam_table'),
                                    kwargs={'action': 'html', 'row_id': mh.row.id}))

    if mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        context['row'] = object_fields(mh.row, pass_fields=('html_msg', ))
        context['row']['folder'] = mh.row.get_folder()
        context['redirect'] = mh.url_edit
        context['time'] = time.time()

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def spam_tables_positions(request, *args, **kwargs):
    """Изменение позиций файлов"""
    result = {}
    mh_vars = spam_tables_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)


spam_rows_vars = {
    'singular_obj': 'Получатель',
    'plural_obj': 'Получатели',
    'rp_singular_obj': 'получателя',
    'rp_plural_obj': 'получателей',
    'template_prefix': 'spam_rows/spam_rows_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'spamcha',
    'submenu': 'spam_rows',
    'show_urla': 'show_spam_rows',
    'create_urla': 'create_spam_row',
    'edit_urla': 'edit_spam_row',
    'model': SpamRow,
}

@login_required
def show_spam_rows(request, spam_table_id: int, *args, **kwargs):
    """Вывод получателей таблиц рассылок"""
    mh_vars = spam_rows_vars.copy()

    # -------------------
    # Родительская модель
    # -------------------
    mh_vars_spam_tables = spam_tables_vars.copy()
    mh_spam_tables = create_model_helper(mh_vars_spam_tables, request, CUR_APP)
    spam_table = mh_spam_tables.get_row(spam_table_id)
    if mh_spam_tables.error:
        return redirect('%s?error=not_found' % (mh_spam_tables.root_url, ))
    mh_spam_tables.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars_spam_tables['edit_urla']),
                                      kwargs={'action': 'edit', 'row_id': mh_spam_tables.row.id})

    mh = create_model_helper(mh_vars, request, CUR_APP, reverse_params={'spam_table_id': spam_table_id})
    mh.select_related_add('spam_table')

    # ---------------------------
    # Родительские хлебные крошки
    # ---------------------------
    for i, crumb in enumerate(mh_spam_tables.breadcrumbs):
        mh.breadcrumbs.insert(i, crumb)
    mh.breadcrumbs.insert(0, root_breadcrumbs)

    # ----------------------------
    # Редактирование родительского
    # контейнера в хлебных крошках
    # ----------------------------
    mh.breadcrumbs.insert(-1, {
        'link': mh_spam_tables.url_edit,
        'name': mh_spam_tables.row.name or '%s %s' % (mh_spam_tables.action_edit, mh_spam_tables.rp_singular_obj),
    })

    context = mh.context

    mh.filter_add({'spam_table__id': mh_spam_tables.row.id})

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
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
            item['folder'] = row.get_folder()
            item['spam_table_name'] = mh_spam_tables.row.name
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
def edit_spam_row(request, action: str, spam_table_id: int, row_id: int = None, *args, **kwargs):
    """Создание/редактирование получателя из таблицы рассылки"""
    mh_vars = spam_rows_vars.copy()

    # -------------------------------
    # Родительская модель (контейнер)
    # -------------------------------
    mh_vars_spam_tables = spam_tables_vars.copy()
    mh_spam_tables = create_model_helper(mh_vars_spam_tables, request, CUR_APP)
    spam_table = mh_spam_tables.get_row(spam_table_id)
    if mh_spam_tables.error:
        return redirect('%s?error=not_found' % (mh_spam_tables.root_url, ))
    mh_spam_tables.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars_spam_tables['edit_urla']),
                                      kwargs={'action': 'edit', 'row_id': mh_spam_tables.row.id})

    mh = create_model_helper(mh_vars, request, CUR_APP, action, reverse_params={'spam_table_id': spam_table_id})
    mh.select_related_add('spam_table')

    # ---------------------------
    # Родительские хлебные крошки
    # ---------------------------
    for i, crumb in enumerate(mh_spam_tables.breadcrumbs):
        mh.breadcrumbs.insert(i, crumb)
    mh.breadcrumbs.insert(0, root_breadcrumbs)

    # ----------------------------
    # Редактирование родительского
    # контейнера в хлебных крошках
    # ----------------------------
    mh.breadcrumbs.insert(-1, {
        'link': mh_spam_tables.url_edit,
        'name': mh_spam_tables.row.name or '%s %s' % (mh_spam_tables.action_edit, mh_spam_tables.rp_singular_obj),
    })

    context = mh.context
    context['spam_table'] = object_fields(mh_spam_tables.row)
    mh.filter_add({'spam_table__id': mh_spam_tables.row.id})

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
        # --------------------------
        # Отправка письма получателю
        # --------------------------
        elif action == 'send' and row:
            accounts = list(EmailAccount.objects.filter(is_active=True))
            random.shuffle(accounts)
            account = accounts[0]
            if account and row.dest:
                msg = mh_spam_tables.row.get_text_msg(msg_type='html')
                account.send_email(msg, row.dest)
            return redirect(reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                                    kwargs={'action': 'edit',
                                            'spam_table_id': mh_spam_tables.row.id,
                                            'row_id': row.id}))

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
                              kwargs={'action': 'edit',
                                      'spam_table_id': mh_spam_tables.row.id,
                                      'row_id': mh.row.id})
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['row']['folder'] = mh.row.get_folder()
        context['row']['spam_table_name'] = mh_spam_tables.row.name
        context['redirect'] = mh.url_edit

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def spam_rows_positions(request, spam_table_id: int, *args, **kwargs):
    """Изменение позиций получателей в таблице рассылки"""
    result = {}
    mh_vars = spam_rows_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions', reverse_params={'spam_table_id': spam_table_id})
    mh.filter_add({'spam_table__id': spam_table_id})
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

email_accounts_vars = {
    'singular_obj': 'Email аккаунт',
    'plural_obj': 'Email аккаунты',
    'rp_singular_obj': 'email аккаунта',
    'rp_plural_obj': 'email аккаунтов',
    'template_prefix': 'email_accounts_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'spamcha',
    'submenu': 'email_accounts',
    'show_urla': 'show_email_accounts',
    'create_urla': 'create_email_account',
    'edit_urla': 'edit_email_account',
    'model': EmailAccount,
}

@login_required
def show_email_accounts(request, *args, **kwargs):
    """Вывод Email аккаунтов"""
    mh_vars = email_accounts_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.breadcrumbs.insert(0, root_breadcrumbs)
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
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
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
def edit_email_account(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование Email аккаунтов"""
    mh_vars = email_accounts_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.breadcrumbs.insert(0, root_breadcrumbs)
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
        # --------------------
        # Загрузка изображения
        # --------------------
        elif action == 'img' and request.FILES:
            mh.uploads()

    if mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.url_edit

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def email_accounts_positions(request, *args, **kwargs):
    """Изменение позиций Email аккаунтов"""
    result = {}
    mh_vars = email_accounts_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_email_accounts(request, *args, **kwargs):
    """Поиск Email аккаунтов"""
    result = {'results': []}

    mh = ModelHelper(EmailAccounts, request)
    mh_vars = email_accounts_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)

    mh.search_fields = ('email', 'smtp_server', 'smtp_port')
    rows = mh.standard_show()

    for row in rows:
        result['results'].append({'text': row.email, 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}

    return JsonResponse(result, safe=False)

black_list_vars = {
    'singular_obj': 'Черный список',
    'plural_obj': 'Черные списки',
    'rp_singular_obj': 'черного списка',
    'rp_plural_obj': 'черных списков',
    'template_prefix': 'black_list_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'spamcha',
    'submenu': 'black_list',
    'show_urla': 'show_black_list',
    'create_urla': 'create_black_list',
    'edit_urla': 'edit_black_list',
    'model': EmailBlackList,
}

@login_required
def show_black_list(request, *args, **kwargs):
    """Вывод Черного списка emails"""
    mh_vars = black_list_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.breadcrumbs.insert(0, root_breadcrumbs)
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
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
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
def edit_black_list(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование Черного списка emails"""
    mh_vars = black_list_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.breadcrumbs.insert(0, root_breadcrumbs)
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
        context['redirect'] = mh.url_edit

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def black_list_positions(request, *args, **kwargs):
    """Изменение позиций в черном списке"""
    result = {}
    mh_vars = black_list_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)
