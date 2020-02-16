# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'demonology'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>daemon)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_daemon, name='show_daemon'),
    url('^admin/(?P<action>create)/$', views.edit_daemon, name='create_daemon'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_daemon, name='edit_daemon'),
    path('admin/positions/', views.daemon_positions, name='daemon_positions'),
    # аякс-поиск
    path('daemon/search/', views.search_daemon, name='search_daemon'),
]