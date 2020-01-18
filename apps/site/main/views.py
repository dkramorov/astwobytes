# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect

from apps.flatcontent.views import SearchLink

CUR_APP = 'main'
main_vars = {
    'singular_obj': 'Главная',
    'template_prefix': 'main_',
    'show_urla': 'home',
}

def home(request):
    """Главная страничка сайта"""
    mh_vars = main_vars.copy()
    context = {}
    q_string = {}
    containers = {}

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/main.html'

    urla = reverse('%s:%s' % (CUR_APP, 'home'))
    page = SearchLink(urla, q_string, request, containers)
    context['page'] = page
    context['containers'] = containers

    return render(request, template, context)

demo_vars = {
    'singular_obj': 'Демо-страничка',
    'template_prefix': 'demo_',
    'show_urla': 'demo',
}

def demo(request):
    """Страничка для разработки"""
    mh_vars = demo_vars.copy()
    context = {}
    q_string = {}
    containers = {}

    if request.is_ajax():
        return JsonResponse(context, safe=False)
    template = 'web/demo.html'

    urla = reverse('%s:%s' % (CUR_APP, 'home'))
    page = SearchLink(urla, q_string, request, containers)
    context['page'] = page
    context['containers'] = containers

    return render(request, template, context)

