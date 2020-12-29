# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from .models import Translate, get_domains

CUR_APP = 'languages'
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

@login_required
def select_language(request, lang: str = None):
    """Выбор языка для заполнения в админке
       Также правильно было бы и язык самой админки переключать
    """
    result = {}
    mh_vars = languages_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'settings')
    context = mh.context

    if lang:
        request.session['lang'] = lang

    context['domains'] = get_domains()
    template = '%sselect_lang.html' % mh.template_prefix
    return render(request, template, context)