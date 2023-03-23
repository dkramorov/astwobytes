# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.conf import settings

from apps.login.views import login_view, logout_view
from apps.main_functions.views import DefaultFeedback

CUR_APP = 'main'
main_vars = {
    'singular_obj': 'Главная',
    'template_prefix': 'main_',
    'show_urla': 'home',
}

def home(request):
    """Страничка входа в админку - авторизация или приветствие"""
    if not request.user.is_authenticated:
        urla = reverse('%s:login' % (CUR_APP, ))
        return redirect(urla)
    context = {
        'singular_obj': 'Добро пожаловать',
        'plural_obj': 'Панель управления',
    }
    return render(request, 'web/main.html', context)

def login(request, *args, **kwargs):
    """Страничка авторизации"""
    return login_view(request, *args, **{
        'template': 'web/login.html',
        'redirect': '/',
    })

def logout(request, *args, **kwargs):
    """Выход пользователя из админки"""
    logout_view(request)
    return redirect('/')

def demo_ui(request, action='profile'):
    """Демонстрация возможностей дизайна админки"""
    context = {
        'breadcrumbs': [
          {'name': 'Демо UI', 'link': '/'},
          {'name': action, 'link': '/demo_ui/%s/' % action},
        ],
        'singular_obj': 'Демо-страничка %s' % action,
        'plural_obj': 'Демо-странички',
        'menu': 'demo_ui',
        'submenu': action,
    }
    template = 'web/demo/%s.html' % action
    return render(request, template, context)
