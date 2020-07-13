# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'binary_com'
urlpatterns = [
    path('', views.index, name='index'),
    path('generate_report/', views.generate_report, name='generate_report'),

    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>schedule)/api/$', views.api, name='api'),
    # админка - роботы
    path('admin/', views.show_robots, name='show_robots'),
    url('^admin/(?P<action>create)/$', views.edit_robot, name='create_robot'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_robot, name='edit_robot'),
    path('admin/positions/', views.robots_positions, name='robots_positions'),
    # аякс-поиск робота
    path('robots/search/', views.search_robots, name='search_robots'),

    # Апи для робота
    path('admin/schedule_constructor/', views.schedule_constructor, name='schedule_constructor'),
    path('get_schedule/', views.get_schedule, name='get_schedule'),
]
