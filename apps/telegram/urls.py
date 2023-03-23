# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from apps.telegram import views

app_name = 'telegram'
urlpatterns = [
    path('send_message/', views.send_message, name='send_message'),
]
