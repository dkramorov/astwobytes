# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'miners'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>comp)/api/$', views.api, name='api'),
    # админка - comp
    path('admin/', views.show_comps, name='show_comps'),
    url('^admin/(?P<action>create)/$', views.edit_comp, name='create_comp'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_comp, name='edit_comp'),
    path('admin/positions/', views.comps_positions, name='comps_positions'),
    path('comps/search/', views.search_comps, name='search_comps'),
    path('scan_ips/', views.scan_ips, name='scan_ips'),

    # сайт - comp
    path('comps/', views.miners_show_comps, name='miners_show_comps'),
    url('^comps/(?P<action>create)/$', views.miners_edit_comp, name='miners_create_comp'),
    url('^comps/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.miners_edit_comp, name='miners_edit_comp'),

    # сайт - диапазоны ip адресов
    path('miners/ip_range/', views.miners_show_ip_range, name='miners_show_ip_range'),
    url('^miners/ip_range/(?P<action>create)/$', views.miners_edit_ip_range, name='miners_create_ip_range'),
    url('^miners/ip_range/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.miners_edit_ip_range, name='miners_edit_ip_range'),
]
