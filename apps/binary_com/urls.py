# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'binary_com'
urlpatterns = [
    path('', views.index, name='index'),
]
