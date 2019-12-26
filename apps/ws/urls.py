# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'ws'
urlpatterns = [
    # Получение/сохранение сообщений с ws
    path('messages/api/', views.messages_api, name='messages_api'),
    path('admin/', views.show_chat, name='show_chat'),
]
