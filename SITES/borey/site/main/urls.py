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
    # feedback
    path('feedback/', views.feedback, name='feedback'),
]
