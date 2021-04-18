# -*- coding:utf-8 -*-
import os
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.string_parser import get_request_ip

from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from .models import Robots

CUR_APP = 'robots'
robots_vars = {
    'singular_obj': 'Робот',
    'plural_obj': 'Роботы',
    'rp_singular_obj': 'робота',
    'rp_plural_obj': 'роботов',
    'template_prefix': 'robots_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'robots',
    'submenu': 'robots',
    'show_urla': 'show_robots',
    'create_urla': 'create_robot',
    'edit_urla': 'edit_robot',
    'model': Robots,
    #'custom_model_permissions': Robots,
    #'select_related_list': ('name', ),
}

def api(request, action: str = 'robots'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    #if action == 'robots':
    #    result = ApiHelper(request, robots, CUR_APP)
    result = ApiHelper(request, robots_vars, CUR_APP)
    return result

@login_required
def show_robots(request, *args, **kwargs):
    """Вывод роботов
       :param request: HttpRequest
    """
    mh_vars = robots_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
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
def edit_robot(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование роботов
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = robots_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
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
def robots_positions(request, *args, **kwargs):
    """Изменение позиций роботов
       :param request: HttpRequest
    """
    result = {}
    mh_vars = robots_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_robots(request, *args, **kwargs):
    """Поиск дилеров
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = robots_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

@csrf_exempt
def inform_server(request):
    """Апи-метод для получения всех данных по роботу
       :param request: HttpRequest
    """
    result = {}
    if not request.headers.get('token') == settings.FS_TOKEN:
        return JsonResponse(result, safe=False)
    body = json.loads(request.body)
    versions = body.get('versions', {})
    hostname = body.get('hostname')
    free_space = body.get('free_space', {})
    analog = Robots.objects.filter(server_name=hostname).first()
    if not analog:
        analog = Robots(server_name=hostname)
    analog.ip = get_request_ip(request)
    analog.selenium_version = versions.get('selenium')
    analog.chrome_version = versions.get('chrome')
    analog.server_free_space = int(free_space.get('free', 0)) / 1024
    analog.save()
    result['success'] = True
    result['robot'] = object_fields(analog)
    return JsonResponse(result, safe=False)

def updater_helper(folder: str, result: dict):
    """Помогает сформировать список файлов для обновления
       :param folder: папка
       :param result: аккумуляция результата
    """
    items = os.listdir(folder)
    for item in items:
        if item.startswith('.'):
            continue

        dest = os.path.join(folder, item)
        if not os.path.exists(dest):
            logger.error('file not exists')
            continue

        if os.path.isfile(dest):
            with open(dest, 'r', encoding='utf-8') as f:
                content = f.read()
                result[item] = content
        elif os.path.isdir(dest):
            result[item] = {}
            updater_helper(dest, result[item])

def updater(request):
    """Апи-метод для обновления робота
       :param request: HttpRequest
    """
    result = {}
    source_folder = '%s/apps/site/%s/source/' % (settings.BASE_DIR, CUR_APP)
    if not settings.DEBUG:
        if not request.headers.get('token') == settings.FS_TOKEN:
            return JsonResponse(result, safe=False)
    upd_self = request.GET.get('updater', False)
    upd_source = request.GET.get('source', False)
    upd_selenium = request.GET.get('selenium', False)

    if not os.path.exists(source_folder):
        return JsonResponse({'error': 'folder not exists'}, safe=False)

    if upd_source or upd_self:
        updater_helper(source_folder, result)

    return JsonResponse(result, safe=False)
