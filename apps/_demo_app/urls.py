# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'demo_app'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>demo_model)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_demo_model, name='show_demo_model'),
    url('^admin/(?P<action>create)/$', views.edit_demo_model, name='create_demo_model'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_demo_model, name='edit_demo_model'),
    path('admin/positions/', views.demo_model_positions, name='demo_model_positions'),
    # аякс-поиск
    path('demo_model/search/', views.search_demo_model, name='search_demo_model'),
]
