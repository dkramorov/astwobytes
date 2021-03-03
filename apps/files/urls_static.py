# -*- coding:utf-8 -*-
from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path('^(?P<link>[^\./]{1,250}\.[a-z4]{1,5})$', views.ReturnFile, name='return_file'),
]
