# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'robots'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>robots|test_scenarios)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_robots, name='show_robots'),
    url('^admin/(?P<action>create)/$', views.edit_robot, name='create_robot'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_robot, name='edit_robot'),
    path('admin/positions/', views.robots_positions, name='robots_positions'),
    # аякс-поиск
    path('robots/search/', views.search_robots, name='search_robots'),

    path('admin/test_scenarios/', views.show_test_scenarios, name='show_test_scenarios'),
    url('^admin/test_scenarios/(?P<action>create)/$', views.edit_test_scenario, name='create_test_scenario'),
    url('^admin/test_scenarios/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_test_scenario, name='edit_test_scenario'),
    path('admin/test_scenarios/positions/', views.test_scenarios_positions, name='test_scenarios_positions'),
    # аякс-поиск
    path('test_scenarios/search/', views.search_test_scenarios, name='search_test_scenarios'),

    # получить информацию от робота
    path('inform_server/', views.inform_server, name='inform_server'),
    # обновление робота
    path('updater/', views.updater, name='updater'),
]
