# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'robots'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>robots)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_robots, name='show_robots'),
    url('^admin/(?P<action>create)/$', views.edit_robot, name='create_robot'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_robot, name='edit_robot'),
    path('admin/positions/', views.robots_positions, name='robots_positions'),
    # аякс-поиск
    path('robots/search/', views.search_robots, name='search_robots'),

    # получить информацию от робота
    path('inform_server/', views.inform_server, name='inform_server'),
    # обновление робота
    path('updater/', views.updater, name='updater'),
]
