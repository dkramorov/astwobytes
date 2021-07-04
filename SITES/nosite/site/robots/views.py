# -*- coding:utf-8 -*-
import os
import json
import logging

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
from apps.main_functions.api_helper import ApiHelper, XlsxHelper
from apps.main_functions.string_parser import get_request_ip

from apps.main_functions.views_helper import (
    show_view,
    edit_view,
    search_view,
)
from apps.site.robots.models import (
    Robots,
    RobotProfiles,
    SearchQueries,
    Sites,
    TestScenarios,
    TEST_COMMANDS,
)

logger = logging.getLogger('main')

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
    'search_result_format': ('{} - {}', 'server_name ip'),
}

def api(request, action: str = 'robots'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    if action == 'test_scenarios':
        result = ApiHelper(request, test_scenarios_vars, CUR_APP)
    elif action == 'search_queries':
        result = ApiHelper(request, search_queries_vars, CUR_APP)
    elif action == 'sites':
        result = ApiHelper(request, sites_vars, CUR_APP)
    else:
        result = ApiHelper(request, robots_vars, CUR_APP)
    return result

def import_xlsx(request, action: str = 'search_queries'):
    """Апи-метод для сохранения данных из excel-файла
                     удаления данных по excel-файлу
       :param request: HttpRequest
       :param action: какую модель использовать
    """
    #if action == 'search_queries':
    #    result = XlsxHelper(request, search_queries_vars, CUR_APP)
    result = XlsxHelper(request, search_queries_vars, CUR_APP,
                        cond_fields = ['name', 'site__url'])
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
    """Поиск роботов
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = robots_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

test_scenarios_vars = {
    'singular_obj': 'Сценарий',
    'plural_obj': 'Сценарии',
    'rp_singular_obj': 'сценария',
    'rp_plural_obj': 'сценариев',
    'template_prefix': 'test_scenarios/test_scenarios_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'robots',
    'submenu': 'test_scenarios',
    'show_urla': 'show_test_scenarios',
    'create_urla': 'create_test_scenario',
    'edit_urla': 'edit_test_scenario',
    'model': TestScenarios,
    #'custom_model_permissions': TestScenarios,
    'select_related_list': ('robot', 'site'),
}

@login_required
def show_test_scenarios(request, *args, **kwargs):
    """Вывод сценариев
       :param request: HttpRequest
    """
    mh_vars = test_scenarios_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('robot')
    mh.select_related_add('site')
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
def edit_test_scenario(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование сценария
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = test_scenarios_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('robot')
    mh.select_related_add('site')
    row = mh.get_row(row_id)
    context = mh.context
    if row:
        try:
            context['commands'] = json.loads(row.commands)
        except Exception as e:
            logger.error(e)
    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    context['test_commands'] = TEST_COMMANDS

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
def test_scenarios_positions(request, *args, **kwargs):
    """Изменение позиций сценариев
       :param request: HttpRequest
    """
    result = {}
    mh_vars = test_scenarios_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_test_scenarios(request, *args, **kwargs):
    """Поиск сценариев
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = test_scenarios_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

sites_vars = {
    'singular_obj': 'Сайт',
    'plural_obj': 'Сайты',
    'rp_singular_obj': 'сайта',
    'rp_plural_obj': 'сайтов',
    'template_prefix': 'sites/sites_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'robots',
    'submenu': 'sites',
    'show_urla': 'show_sites',
    'create_urla': 'create_site',
    'edit_urla': 'edit_site',
    'model': Sites,
    #'custom_model_permissions': Sites,
}

@login_required
def show_sites(request, *args, **kwargs):
    """Вывод сайтов
       :param request: HttpRequest
    """
    mh_vars = sites_vars.copy()
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
def edit_site(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование сайта
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = sites_vars.copy()
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
        context['row'] = object_fields(mh.row)
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.get_url_edit()

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def sites_positions(request, *args, **kwargs):
    """Изменение позиций сайтов
       :param request: HttpRequest
    """
    result = {}
    mh_vars = sites_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_sites(request, *args, **kwargs):
    """Поиск сайтов
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = sites_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

robot_profiles_vars = {
    'singular_obj': 'Профиль робота',
    'plural_obj': 'Профили роботов',
    'rp_singular_obj': 'профиля робота',
    'rp_plural_obj': 'профилей роботов',
    'template_prefix': 'robot_profiles/robot_profiles_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'robots',
    'submenu': 'robot_profiles',
    'show_urla': 'show_robot_profiles',
    'create_urla': 'create_robot_profile',
    'edit_urla': 'edit_robot_profile',
    'model': RobotProfiles,
    #'custom_model_permissions': RobotProfiles,
    'select_related_list': ('robot', ),
}

@login_required
def show_robot_profiles(request, *args, **kwargs):
    """Вывод профилей роботов
       :param request: HttpRequest
    """
    mh_vars = robot_profiles_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('robot')
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
def edit_robot_profile(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование профиля робота
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = robot_profiles_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('robot')
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
def robot_profiles_positions(request, *args, **kwargs):
    """Изменение профиля робота
       :param request: HttpRequest
    """
    result = {}
    mh_vars = robot_profiles_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_robot_profiles(request, *args, **kwargs):
    """Поиск профиля робота
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = robot_profiles_vars,
                       cur_app = CUR_APP,
                       sfields = None, )


search_queries_vars = {
    'singular_obj': 'Поисковый запрос',
    'plural_obj': 'Поисковые запросы',
    'rp_singular_obj': 'поискового запроса',
    'rp_plural_obj': 'поисковых запросов',
    'template_prefix': 'search_queries/search_queries_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'robots',
    'submenu': 'search_queries',
    'show_urla': 'show_search_queries',
    'create_urla': 'create_search_query',
    'edit_urla': 'edit_search_query',
    'model': SearchQueries,
    #'custom_model_permissions': SearchQueries,
    'select_related_list': ('site', ),
}

@login_required
def show_search_queries(request, *args, **kwargs):
    """Вывод поисковых запросов
       :param request: HttpRequest
    """
    mh_vars = search_queries_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('site')
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

    context['import_xlsx_url'] = reverse(
        '%s:%s' % (CUR_APP, 'import_xlsx'),
        kwargs={'action': 'search_queries'}
    )

    template = '%stable.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def edit_search_query(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование поискового запроса
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = search_queries_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('site')
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
def search_queries_positions(request, *args, **kwargs):
    """Изменение поискового запроса
       :param request: HttpRequest
    """
    result = {}
    mh_vars = search_queries_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_search_queries(request, *args, **kwargs):
    """Поиск поисковых запросов
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = search_queries_vars,
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
    robot = Robots.objects.filter(server_name=hostname).first()
    if not robot:
        robot = Robots(server_name=hostname)
    robot.ip = get_request_ip(request)
    robot.selenium_version = versions.get('selenium')
    robot.chrome_version = versions.get('chrome')
    robot.server_free_space = int(free_space.get('free', 0)) / 1024
    robot.save()
    profile = body.get('profile')
    if profile and profile.get('name'):
        robot_profile = RobotProfiles.objects.filter(robot=robot, name=profile['name']).first()
        if not robot_profile:
            robot_profile = RobotProfiles(robot=robot, name=profile['name'])
        profile_fields = (
            'user_agent',
            'resolution',
            'yandex_login',
            'yandex_passwd',
        )
        needSave = False
        for field in profile_fields:
            if not getattr(robot_profile, field) == profile.get(field):
                setattr(robot_profile, field, profile.get(field))
                needSave = True
        if needSave:
            robot_profile.save()

    result['success'] = True
    result['robot'] = object_fields(robot)
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
            if '.DS_Store' in dest:
                continue
            with open(dest, 'r', encoding='utf-8') as f:
                content = f.read()
                result[item] = content
        elif os.path.isdir(dest):
            if '__pycache__' in dest:
                continue
            result[item] = {}
            updater_helper(dest, result[item])

def updater(request):
    """Апи-метод для обновления робота
       :param request: HttpRequest
    """
    result = {}
    source_folder = '%s/apps/site/%s/source/' % (settings.BASE_DIR, CUR_APP)

    version = request.GET.get('version', '0')
    # Если версия как у нас, то не обновляем
    from apps.site.robots.source.plugins.version import VERSION
    if version == VERSION:
        result['update_not_needed'] = 'Already updated up to date, v=%s' % VERSION
        return JsonResponse(result, safe=False)
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
