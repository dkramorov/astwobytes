# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from apps.main_functions.files import check_path, full_path, file_size
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.tabulator import tabulator_filters_and_sorters

from .models import Translate

CUR_APP = 'lanuages'
languages_vars = {
    'singular_obj': 'Перевод',
    'plural_obj': 'Переводы',
    'rp_singular_obj': 'перевода',
    'rp_plural_obj': 'переводов',
    'template_prefix': 'languages_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'languages',
    'submenu': 'lanuages',
    'show_urla': 'show_translates',
    'create_urla': 'create_translate',
    'edit_urla': 'edit_translate',
    'model': Translate,
}

def get_domain(request):
    """Получить текущий домен для правильного перевода"""
    domain = None
    if not hasattr(settings, "DOMAINS") or not hasattr(request, "META"):
        return domain
    if "HTTP_HOST" in request.META:
        domains = settings.DOMAINS
        domain = request.META['HTTP_HOST']
        # ----------------------------------------
        # На localhost:8000 надо эмулировать домен
        # то есть получать его по сессии
        # ----------------------------------------
        if settings.DEBUG:
            domains = request.session.get('domain') or domains[0]['domain']
    return domain

def translate_rows(rows: list, request):
    """Заполняем переводы для queryset rows
       domains = settings.DOMAINS
       :param rows: объекты queryset/list которые надо перевести
       :param request: запрос"""
    domain = get_domain(request)
    for row in rows:
        if hasattr(row, 'translations'):
            if domain in row.translations:
                for key, value in row.translations[domain].items():
                    setattr(row, key, value)

def get_translations(rows, ct):
    """Вытаскиваем переводы для queryset/list
       :param rows: объекты queryset/list которые надо перевести
       :param ct: ContentType модели"""
    domains = []
    if hasattr(settings, 'DOMAINS'):
        d = settings.DOMAINS
        domains = [{
            'pk':item['pk'],
            'name':item['name'],
            'domain': item['domain'],
            'translations':{},
        } for item in d if item['pk']]

    ids = {}
    for row in rows:
        row.translations = {}
        for item in domains:
            row.translations[item['domain']] = {}
        ids[row.id] = row

    translations = Translate.objects.filter(content_type=ct, model_pk__in=ids.keys())
    for translate in translations:
        for item in domains:
            if item['pk'] == translate.domain_pk:
                ids[translate.model_pk].translations[item['domain']][translate.field] = translate.text

def get_referer_path(referer):
    """Получение ссылки без домена от реферера
       :param referer: ссылка с которой пришел пользователь"""
    if not referer:
        return referer
    referer = referer.replace('http://', '')
    referer = referer.replace('https://', '')
    referer = referer.replace('www.', '')
    referer = referer.replace(request.META.get('HTTP_HOST', ''), '')
    return referer

def PickLanguage(request, lang):
    """Переключение языка
       :param lang: язык (домен) на который переключаемся"""
    goto = None
    referer = None
    if hasattr(request, 'META'):
        referer = get_referer_path(request.META.get('HTTP_REFERER'))
        if not referer:
            return redirect('/')
    if hasattr(settings, 'DOMAINS'):
        domains = settings.DOMAINS
        for domain in domains:
            if domain['domain'].startswith("%s." % lang):
                if settings.DEBUG:
                    request.session['domain'] = domain['domain']
                    return redirect(referer)
                return redirect("http://%s%s" % (domain['domain'], referer))
    return redirect("/")

def api(request, action: str = 'files'):
    """Апи-метод для получения всех данных"""
    mh_vars = languages_vars.copy()
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
def show_translates(request, *args, **kwargs):
    """Вывод Переводов"""
    mh_vars = languages_vars.copy()
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
def edit_translate(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование файла"""
    mh_vars = languages_vars.copy()
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
        # -------------------------------------------
        # Нужно обновить ссылку на файл, если ее нету
        # Если есть файл, нужно обновить mimetype
        # -------------------------------------------
        elif action == 'img' and request.FILES:
            mh.uploads()

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
def translates_positions(request, *args, **kwargs):
    """Изменение позиций переводов"""
    result = {}
    mh_vars = languages_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)



