# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    # Главная страничка сайта
    path('', views.home, name='home'),
    # demo
    path('demo/', views.demo, name='demo'),
    # Каталог
    url('^cat/$', views.cat_on_site, name='cat_on_site'),
    url('^cat/(?P<link>.+)/$', views.cat_on_site, name='cat_on_site'),
    url('^product/(?P<product_id>[0-9]+)/$', views.product_on_site, name='product_on_site'),
    # feedback
    path('feedback/', views.feedback, name='feedback'),
]
