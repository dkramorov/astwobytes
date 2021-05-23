# -*- coding:utf-8 -*-
from django.urls import path, re_path

from apps.files import views

urlpatterns = [
    # сайт (карта сайта)
    path('sitemap/', views.show_sitemap, name='show_sitemap'),
    # статические файлы
    re_path('^(?P<link>[^\./]{1,250}\.[a-z4]{1,5})$', views.ReturnFile, name='return_file'),
    re_path('^(?P<link>sitemap/[a-z]{2,10}\.xml)$', views.ReturnFile, name='return_file'),
]
