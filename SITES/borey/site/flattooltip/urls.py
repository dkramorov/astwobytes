# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'flattooltip'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>flattooltip)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_flattooltip, name='show_flattooltip'),
    url('^admin/(?P<action>create)/$', views.edit_flattooltip, name='create_flattooltip'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_flattooltip, name='edit_flattooltip'),
    path('admin/positions/', views.flattooltip_positions, name='flattooltip_positions'),
    # аякс-поиск
    path('flattooltip/search/', views.search_flattooltip, name='search_flattooltip'),
]
