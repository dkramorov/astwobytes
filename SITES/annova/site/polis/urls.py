# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'polis'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>polis)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_polises, name='show_polises'),
    url('^admin/(?P<action>create)/$', views.edit_polis, name='create_polis'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_polis, name='edit_polis'),
    path('admin/positions/', views.polis_positions, name='polis_positions'),
    # аякс-поиск
    path('polis/search/', views.search_polises, name='search_polises'),
]
