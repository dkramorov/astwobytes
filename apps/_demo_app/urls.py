# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'demo_app'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>demo_app)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_demo_app, name='show_demo_app'),
    url('^admin/(?P<action>create)/$', views.edit_demo_app, name='create_demo_app'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_demo_app, name='edit_demo_app'),
    path('admin/positions/', views.demo_app_positions, name='demo_app_positions'),
    # аякс-поиск
    path('demo_app/search/', views.search_demo_app, name='search_demo_app'),
]
