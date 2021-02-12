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

from apps.main_functions.files import check_path, full_path, file_size, make_folder, catch_file, ListDir, isForD, extension
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper, get_user_permissions
from apps.main_functions.api_helper import ApiHelper, XlsxHelper

from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view,
                                              special_model_vars, )
from apps.spamcha.imap import ImapProvider
from apps.spamcha.models import (SpamTable,
                                 SpamRow,
                                 EmailAccount,
                                 EmailBlackList,
                                 SMSPhone,
                                 SpamRedirect,
                                 SpamRedirectStata, )

# Локальный .env из папки
from envparse import env
env.read_envfile()
TOKEN = env('TOKEN', default='')
API_URL = env('API_URL', default='')
PORT = env('PORT', default='', cast=int)
HOST = env('HOST', default='')
CERT_PATH = env('CERT_PATH', default='')

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

def api(request, action: str = 'spam_tables'):
    """Апи-метод для получения всех данных"""
    if action == 'spam_rows':
        result = ApiHelper(request, spam_rows_vars, CUR_APP)
    elif action == 'email_accounts':
        result = ApiHelper(request, email_accounts_vars, CUR_APP)
    elif action == 'black_list':
        result = ApiHelper(request, black_list_vars, CUR_APP)
    else:
        result = ApiHelper(request, spam_tables_vars, CUR_APP)
    return result

def import_xlsx(request, action: str = 'email_accounts'):
    """Апи-метод для сохранения данных из excel-файла
                     удаления данных по excel-файлу
       :param request: HttpRequest
       :param action: какую модель использовать
    """
    if action == 'spam_rows':
        spam_table_id = request.GET.get('row_id')
        result = XlsxHelper(request, spam_rows_vars, CUR_APP,
                            cond_fields = ['dest', 'spam_table_id'],
                            reverse_params = {
                                'spam_table_id': spam_table_id,
                            })
    else:
        result = XlsxHelper(request, email_accounts_vars, CUR_APP,
                            cond_fields = ['email'])
    return result

@login_required
def show_spam_tables(request, *args, **kwargs):
    """Вывод таблиц рассылок"""
    mh_vars = spam_tables_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.breadcrumbs.insert(0, root_breadcrumbs)
    context = mh.context

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
        context['row'] = object_fields(mh.row, pass_fields=('html_msg', ))
        context['row']['folder'] = mh.row.get_folder()
        context['redirect'] = mh.get_url_edit()
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

@login_required
def spam_tables_images(request, *args, **kwargs):
    """Работа с изображениями через redactor"""
    result = {}
    folder = 'sp-images' # Чтобы не фигурировало spam
    make_folder(folder)
    mh_vars = spam_tables_vars.copy()
    # Список изображений:
    #[{ "thumb": "/img/1m.jpg", "image": "/img/1.jpg", "title": "Image 1", "folder": "Folder 1" }, ... ]
    # Ответ по загрузке:
    # { "filelink": "/images/img.jpg" }
    perms = get_user_permissions(request.user, mh_vars['model'])
    if request.FILES and perms['edit']:
        result['filelink'] = '/static/img/ups.png'
        f = request.FILES.get('file')
        if f:
            dest = os.path.join(folder, f.name)
            if catch_file(f, dest):
                result['filelink'] = '/media/%s' % dest
    elif request.method == 'GET':
        result = []
        items = ListDir(folder)
        for item in items:
            path = os.path.join(folder, item)
            img = '/media/%s' % path
            if isForD(path) == 'file' and extension(item):
                result.append({
                    'thumb': img,
                    'image': img,
                    'title': '',
                    'folder': folder,
                })
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

    mh = create_model_helper(mh_vars, request, CUR_APP, reverse_params={
        'spam_table_id': spam_table_id
    })
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
    context['spam_table'] = mh_spam_tables.row
    mh.filter_add({'spam_table__id': mh_spam_tables.row.id})

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

    context['import_xlsx_url'] = reverse('%s:%s' % (CUR_APP, 'import_xlsx'),
                                         kwargs={'action': 'spam_rows'})
    # Дополняем GET параметром url загрузки эксельки
    context['import_xlsx_url'] += '?row_id=%s' % spam_table_id

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
    mh_spam_tables.url_edit = mh_spam_tables.get_url_edit()

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
    mh.filter_add({'spam_table__id': mh_spam_tables.row.id})
    row = mh.get_row(row_id)
    context = mh.context
    context['spam_table'] = object_fields(mh_spam_tables.row)

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
        elif action in ('send', 'send_html') and row:
            accounts = list(EmailAccount.objects.filter(is_active=True))
            if accounts and row.dest:
                random.shuffle(accounts)
                account = accounts[0]
                if action == 'send':
                    msg = mh_spam_tables.row.get_text_msg(msg_type='html')
                    account.send_email(msg, row.dest)
            kwargs = {
                'action': 'edit',
                'spam_table_id': mh_spam_tables.row.id,
                'row_id': row.id,
            }
            return redirect(reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                                    kwargs=kwargs))

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
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['row']['folder'] = mh.row.get_folder()
        context['row']['spam_table_name'] = mh_spam_tables.row.name
        context['redirect'] = mh.get_url_edit()

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
    context['import_xlsx_url'] = reverse('%s:%s' % (CUR_APP, 'import_xlsx'),
                                         kwargs={'action': 'email_accounts'})
    template = '%stable.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def edit_email_account(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование Email аккаунтов"""
    mh_vars = email_accounts_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.breadcrumbs.insert(0, root_breadcrumbs)
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
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.get_url_edit()

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
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['redirect'] = mh.get_url_edit()

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

sms_phones_vars = {
    'singular_obj': 'Телефон для смс',
    'plural_obj': 'Телефоны для смс',
    'rp_singular_obj': 'телефона для смс',
    'rp_plural_obj': 'телефонов для смс',
    'template_prefix': 'sms_phones_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'spamcha',
    'submenu': 'sms_phones',
    'show_urla': 'show_sms_phones',
    'create_urla': 'create_sms_phone',
    'edit_urla': 'edit_sms_phone',
    'model': SMSPhone,
}

@login_required
def show_sms_phones(request, *args, **kwargs):
    """Вывод телефонов для смс"""
    extra_vars = {
        'token': TOKEN,
        'api_url': API_URL,
        'port': PORT,
        'host': '127.0.0.1' if settings.DEBUG else request.META['HTTP_HOST'],
        'cert_path': CERT_PATH,
    }
    return show_view(request,
                     model_vars = sms_phones_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

@login_required
def edit_sms_phone(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование телефонов для смс"""
    return edit_view(request,
                     model_vars = sms_phones_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def sms_phones_positions(request, *args, **kwargs):
    """Изменение позиций телефонов для смс"""
    result = {}
    mh_vars = sms_phones_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_sms_phones(request, *args, **kwargs):
    """Поиск телефонов для смс"""
    return search_view(request,
                       model_vars = sms_phones_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', 'phone', 'code'), )

redirects_vars = {
    'singular_obj': 'Переадресация рассылки',
    'plural_obj': 'Переадресации рассылок',
    'rp_singular_obj': 'переадресации рассылки',
    'rp_plural_obj': 'переадресаций рассылок',
    'template_prefix': 'spam_redirects_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'spamcha',
    'submenu': 'redirects',
    'show_urla': 'show_redirects',
    'create_urla': 'create_redirect',
    'edit_urla': 'edit_redirect',
    'model': SpamRedirect,
}

@login_required
def show_redirects(request, *args, **kwargs):
    """Вывод переадресаций рассылки"""
    return show_view(request,
                     model_vars = redirects_vars,
                     cur_app = CUR_APP, )

@login_required
def edit_redirect(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование переадресаций рассылки"""
    return edit_view(request,
                     model_vars = redirects_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def redirects_positions(request, *args, **kwargs):
    """Изменение переадресаций рассылки"""
    result = {}
    mh_vars = redirects_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_redirects(request, *args, **kwargs):
    """Поиск переадресаций рассылки"""
    return search_view(request,
                       model_vars = redirects_vars,
                       cur_app = CUR_APP,
                       sfields = ('our_link', 'ext_link'), )

def srdr_goto(request, our_link):
    """Переадресация для рассылки"""
    dest = 'https://223-223.ru'
    rdr = SpamRedirect.objects.filter(our_link=our_link).first()
    if rdr:
        dest = rdr.ext_link
        email = request.GET.get('email')
        try:
            client_id = int(request.GET.get('client_id'))
        except Exception:
            client_id = 0
        # Пишем в статистику
        SpamRedirectStata.objects.create(spam_redirect=rdr, email=email, client_id=client_id)
    return redirect(dest)

redirects_stata_vars = {
    'singular_obj': 'Статистика переадресации',
    'plural_obj': 'Статистика переадресаций',
    'rp_singular_obj': 'статистики переадресации',
    'rp_plural_obj': 'статистик переадресаций',
    'template_prefix': 'spam_redirects_stata_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'spamcha',
    'submenu': 'redirects_stata',
    'show_urla': 'show_redirects_stata',
    'create_urla': 'create_redirect_stata',
    'edit_urla': 'edit_redirect_stata',
    'model': SpamRedirectStata,
    'select_related_list': ('spam_redirect', ),
}

@login_required
def show_redirects_stata(request, *args, **kwargs):
    """Вывод статистики переадресаций рассылки"""
    return show_view(request,
                     model_vars = redirects_stata_vars,
                     cur_app = CUR_APP, )

@login_required
def edit_redirect_stata(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование статистики переадресаций рассылки"""
    return edit_view(request,
                     model_vars = redirects_stata_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def redirects_stata_positions(request, *args, **kwargs):
    """Изменение статистики переадресаций рассылки"""
    result = {}
    mh_vars = redirects_stata_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_redirects_stata(request, *args, **kwargs):
    """Поиск переадресаций рассылки"""
    return search_view(request,
                       model_vars = redirects_stata_vars,
                       cur_app = CUR_APP,
                       sfields = ('email', 'client_id'), )

mailbox_vars = {
    'singular_obj': 'Почтовый ящик',
    'plural_obj': 'Почтовые ящики',
    'rp_singular_obj': 'почтового ящика',
    'rp_plural_obj': 'почтовых ящиков',
    'template_prefix': 'spamcha_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'spamcha',
    'submenu': 'mailbox',
    'show_urla': 'show_mailbox',
}
@login_required
def show_mailbox(request, *args, **kwargs):
    """Почтовый ящик пользователя"""
    mh_vars = mailbox_vars.copy()
    context = mh_vars
    root_url = reverse('%s:%s' % (CUR_APP, mh_vars['show_urla']))
    context['root_url'] = root_url
    context['breadcrumbs'] = [{
        'name': mh_vars['singular_obj'],
        'link': root_url,
    }]

    imap = ImapProvider(request.user)
    if imap.authorized:
        if request.GET.get('folder') and request.is_ajax():
            result = imap.all_letters(request.GET['folder'], by=4)
            return JsonResponse(result, safe=False)
        else:
            context['mailbox'] = imap.get_folders()

    template = '%smailbox.html' % mh_vars['template_prefix']
    return render(request, template, context)
