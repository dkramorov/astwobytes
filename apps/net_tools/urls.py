# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'net_tools'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>ip_address)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_ip_address, name='show_ip_address'),
    url('^admin/(?P<action>create)/$', views.edit_ip_address, name='create_ip_address'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_ip_address, name='edit_ip_address'),
    path('admin/positions/', views.ip_address_positions, name='ip_address_positions'),
    # аякс-поиск
    path('ip_address/search/', views.search_ip_address, name='search_ip_address'),

    # админка
    path('admin/ip_range/', views.show_ip_range, name='show_ip_range'),
    url('^admin/ip_range/(?P<action>create)/$', views.edit_ip_range, name='create_ip_range'),
    url('^admin/ip_range/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_ip_range, name='edit_ip_range'),
    path('admin/ip_range/positions/', views.ip_range_positions, name='ip_range_positions'),
    # аякс-поиск
    path('ip_range/search/', views.search_ip_range, name='search_ip_range'),
]
