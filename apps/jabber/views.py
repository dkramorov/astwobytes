# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.api_helper import ApiHelper

from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )

from apps.jabber.models import Jabber

CUR_APP = 'jabber'
jabber_vars = {
    'singular_obj': 'Чат',
    'plural_obj': 'Чаты',
    'rp_singular_obj': 'чата',
    'rp_plural_obj': 'чатов',
    'template_prefix': 'jabber_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'jabber',
    'submenu': 'jabber',
    'show_urla': 'show_jabber',
    'create_urla': 'create_jabber',
    'edit_urla': 'edit_jabber',
    'model': Jabber,
    #'custom_model_permissions': Jabber,
}

@login_required
def jabber_chat(request, *args, **kwargs):
    """Чат
       :param request: HttpRequest
    """
    mh_vars = jabber_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    context = mh.context

    template = '%schat.html' % (mh.template_prefix, )
    return render(request, template, context)
