# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    # Главная страничка сайта
    path('', views.home, name='home'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # Демо-странички
    url('^demo_ui/(?P<action>[a-z_]{3,30})/$', views.demo_ui, name='demo_ui'),
]
