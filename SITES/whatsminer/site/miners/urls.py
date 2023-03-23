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
]
