# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import ModelHelper, create_model_helper
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from .models import Rubrics, RGenres, REvents, Places, RSeances

CUR_APP = 'afisha'
rubrics_vars = {
    'singular_obj': 'Рубрика места Афиши',
    'plural_obj': 'Рубрики мест Афиши',
    'rp_singular_obj': 'рубрики',
    'rp_plural_obj': 'рубрик',
    'template_prefix': 'afisha_rubrics_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'afisha',
    'submenu': 'rubrics',
    'show_urla': 'show_rubrics',
    'create_urla': 'create_rubric',
    'edit_urla': 'edit_rubric',
    'model': Rubrics,
}

def api(request, action: str = 'rubrics'):
    """Апи-метод для получения всех данных"""
    if action == 'genres':
        result = ApiHelper(request, genres_vars, CUR_APP)
    elif action == 'events':
        result = ApiHelper(request, events_vars, CUR_APP)
    elif action == 'places':
        result = ApiHelper(request, places_vars, CUR_APP)
    elif action == 'seances':
        result = ApiHelper(request, seances_vars, CUR_APP)
    else:
        result = ApiHelper(request, rubrics_vars, CUR_APP)
    return result

@login_required
def show_rubrics(request, *args, **kwargs):
    """Вывод рубрик мест Афиши"""
    return show_view(request,
                     model_vars = rubrics_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_rubric(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование рубрики места Афиши"""
    return edit_view(request,
                     model_vars = rubrics_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

def search_rubrics(request, *args, **kwargs):
    """Поиск рубрик мест"""
    return search_view(request,
                       model_vars = rubrics_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

genres_vars = {
    'singular_obj': 'Жанр Афиши',
    'plural_obj': 'Жанры Афиши',
    'rp_singular_obj': 'жанра',
    'rp_plural_obj': 'жанров',
    'template_prefix': 'afisha_genres_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'afisha',
    'submenu': 'genres',
    'show_urla': 'show_genres',
    'create_urla': 'create_genre',
    'edit_urla': 'edit_genre',
    'model': RGenres,
}

@login_required
def show_genres(request, *args, **kwargs):
    """Вывод жанров"""
    return show_view(request,
                     model_vars = genres_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_genre(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование жанра Афиши"""
    return edit_view(request,
                     model_vars = genres_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

def search_genres(request, *args, **kwargs):
    """Поиск жанров"""
    return search_view(request,
                       model_vars = genres_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', 'altname'))

events_vars = {
    'singular_obj': 'События Афиши',
    'plural_obj': 'События Афиши',
    'rp_singular_obj': 'события',
    'rp_plural_obj': 'событий',
    'template_prefix': 'afisha_events_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'afisha',
    'submenu': 'events',
    'show_urla': 'show_events',
    'create_urla': 'create_event',
    'edit_urla': 'edit_event',
    'model': REvents,
}

@login_required
def show_events(request, *args, **kwargs):
    """Вывод событий"""
    mh_vars = events_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('rgenre')
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
            if row.rgenre:
                item['rgenre__name'] = item['rgenre']['name']
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
def edit_event(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование события Афиши"""
    mh_vars = events_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('rgenre')
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

def search_events(request, *args, **kwargs):
    """Поиск событий"""
    return search_view(request,
                       model_vars = events_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', ))

places_vars = {
    'singular_obj': 'Место для Афиши',
    'plural_obj': 'Места для Афиши',
    'rp_singular_obj': 'места',
    'rp_plural_obj': 'мест',
    'template_prefix': 'afisha_places_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'afisha',
    'submenu': 'places',
    'show_urla': 'show_places',
    'create_urla': 'create_place',
    'edit_urla': 'edit_place',
    'model': Places,
}

@login_required
def show_places(request, *args, **kwargs):
    """Вывод мест Афиши"""
    mh_vars = places_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('rubric')
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
            if row.rubric:
                item['rubric__name'] = row.rubric.name
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
def edit_place(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование места Афиши"""
    mh_vars = places_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('rubric')
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
                context['success'] = '%s удалено' % (mh.singular_obj, )
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
        context['row']['folder'] = mh.row.get_folder()
        context['redirect'] = mh.get_url_edit()

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

def search_places(request, *args, **kwargs):
    """Поиск мест событий"""
    return search_view(request,
                       model_vars = places_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', ))

seances_vars = {
    'singular_obj': 'Сеансы для Афиши',
    'plural_obj': 'Сеансы для Афиши',
    'rp_singular_obj': 'сеанса',
    'rp_plural_obj': 'сеансов',
    'template_prefix': 'afisha_seances_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'afisha',
    'submenu': 'seances',
    'show_urla': 'show_seances',
    'create_urla': 'create_seance',
    'edit_urla': 'edit_seance',
    'model': RSeances,
}

@login_required
def show_seances(request, *args, **kwargs):
    """Вывод сеансов для Афиши"""
    mh_vars = seances_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('place')
    mh.select_related_add('event')
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
            if row.place:
                item['place__name'] = row.place.name
            if row.event:
                item['event__name'] = row.event.name
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
def edit_seance(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование сеансов для Афиши"""
    mh_vars = seances_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('place')
    mh.select_related_add('event')
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
        context['row']['folder'] = mh.row.get_folder()
        context['redirect'] = mh.get_url_edit()

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def model_positions(request, action, *args, **kwargs):
    """Изменение позиций моделей Афиши"""
    result = {}
    actions = {
        'rubrics': rubrics_vars,
        'genres': genres_vars,
        'events': events_vars,
        'places': places_vars,
        'seances': seances_vars,
    }
    model_vars = actions.get(action)
    if not model_vars:
        result['error'] = 'Не указана модель для сортировки'
        return JsonResponse(result, safe=False)

    mh_vars = model_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()

    return JsonResponse(result, safe=False)
