# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'yandex'
urlpatterns = [
    path('metrika/', views.metrika, name='metrika'),
    #url('^cat/$', views.cat_on_site, name='cat_on_site'),
]
