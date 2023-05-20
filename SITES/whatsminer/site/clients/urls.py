# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'clients'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>clients)/api/$', views.api, name='api'),

    # сайт - clients
    path('clients/', views.show_clients, name='show_clients'),
    url('^clients/(?P<action>create)/$', views.edit_client, name='create_client'),
    url('^clients/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_client, name='edit_client'),
]
