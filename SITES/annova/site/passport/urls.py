# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from apps.site.passport import views

app_name = 'passport'
urlpatterns = [
    # получение по апи всех данных (секретно)
    #url('^(?P<action>passport)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_passports, name='show_passports'),
    url('^admin/(?P<action>create)/$', views.edit_passport, name='create_passport'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_passport, name='edit_passport'),
    path('admin/positions/', views.passports_positions, name='passports_positions'),
    # аякс-поиск
    path('passports/search/', views.search_passports, name='search_passports'),
]
