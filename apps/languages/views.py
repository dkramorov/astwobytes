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
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

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

def api(request, action: str = 'languages'):
    """Апи-метод для получения всех данных"""
    #if action == 'languages':
    #    result = ApiHelper(request, languages_vars, CUR_APP)
    result = ApiHelper(request, languages_vars, CUR_APP)
    return result

@login_required
def show_translates(request, *args, **kwargs):
    """Вывод переводов"""
    return show_view(request,
                     model_vars = languages_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_translate(request, action:str, row_id:int = None, *args, **kwargs):
    """Создание/редактирование перевода"""
    return edit_view(request,
                     model_vars = languages_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

@login_required
def translates_positions(request, *args, **kwargs):
    """Изменение позиций переводов"""
    result = {}
    mh_vars = languages_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

