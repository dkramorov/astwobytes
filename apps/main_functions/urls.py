# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'main_functions'
urlpatterns = [
    url('^my_ip/$', views.my_ip, name='my_ip'),
]