# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'freeswitch'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>redirects)/api/$', views.api, name='api'),
    # переадресации
    path('admin/redirects/', views.show_redirects, name='show_redirects'),
    url('^admin/redirects/(?P<action>create)/$', views.edit_redirect, name='create_redirect'),
    url('^admin/redirects/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_redirect, name='edit_redirect'),
    path('admin/redirects/positions/', views.redirects_positions, name='redirects_positions'),
    # звонки
    path('admin/cdrcsv/', views.show_cdrcsv, name='show_cdrcsv'),
    path('admin/call_from_site/', views.call_from_site, name='call_from_site'),
    path('admin/callcenter/', views.callcenter, name='callcenter'),
    # мониторинг
    path('admin/monitoring/', views.monitoring, name='monitoring'),
    # пользователи
    path('admin/', views.show_users, name='show_users'),
    url('^admin/(?P<action>create)/$', views.edit_user, name='create_user'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_user, name='edit_user'),
    path('admin/positions/', views.users_positions, name='users_positions'),
    # белый список телефонов, на которые можно звонить по динамическому диалплану
    path('admin/phones_white_list/', views.show_phones_white_list, name='show_phones_white_list'),
    url('^admin/phones_white_list/(?P<action>create)/$', views.edit_phones_white_list, name='create_phones_white_list'),
    url('^admin/phones_white_list/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_phones_white_list, name='edit_phones_white_list'),
    path('admin/phones_white_list/positions/', views.phones_white_list_positions, name='phones_white_list_positions'),
]
