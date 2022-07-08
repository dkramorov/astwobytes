# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'freeswitch'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>redirects|phones_white_list|cdr_csv)/api/$', views.api, name='api'),
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
    # телефоны из CRM на них можно звонить по динамическому диалплану
    path('admin/phones_white_list/', views.show_phones_white_list, name='show_phones_white_list'),
    url('^admin/phones_white_list/(?P<action>create)/$', views.edit_phones_white_list, name='create_phones_white_list'),
    url('^admin/phones_white_list/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_phones_white_list, name='edit_phones_white_list'),
    path('admin/phones_white_list/positions/', views.phones_white_list_positions, name='phones_white_list_positions'),
    # пользователи из CRM, привязанным к FSUser можно звонить по динамическому диалплану
    path('admin/personal_users/', views.show_personal_users, name='show_personal_users'),
    url('^admin/personal_users/(?P<action>create)/$', views.edit_personal_user, name='create_personal_user'),
    url('^admin/personal_users/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_personal_user, name='edit_personal_user'),
    path('admin/personal_users/positions/', views.personal_users_positions, name='personal_users_positions'),
    path('personal_users/search/', views.search_personal_users, name='search_personal_users'),
    # api для проверки возможности звонка по динамическому диалплану
    path('is_phone_in_white_list/', views.is_phone_in_white_list, name='is_phone_in_white_list'),
    # api для отправки смски
    path('sms_service/send_sms/', views.send_sms, name='send_sms'),
    # api для звонка и диктовки кода голосом со свича
    path('sms_service/say_code/', views.say_code, name='say_code'),
    # api для синхронизации
    path('personal_users/sync/', views.sync_personal_users, name='sync_personal_users'),
    # Обновить пользователей fs из jabber (пользователи приложения)
    path('sync_jabber2fs/', views.sync_jabber2fs, name='sync_jabber2fs'),
]
