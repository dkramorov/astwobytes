# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'login'
urlpatterns = [
    # получение по апи всех данных
    url('^(?P<action>users)/api/$', views.api, name='api'),

    # Авторизация/ПНХ(выход)
    path('', views.welcome, name='welcome'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    # Пользователи
    path('users/', views.show_users, name='show_users'),
    url('^users/(?P<action>create)/$', views.edit_user, name='create_user'),
    url('^users/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_user, name='edit_user'),
    url('^users/check_username/$', views.check_username, name='check_username'),
    path('users/positions/', views.users_positions, name='users_positions'),
    path('users/search/', views.search_users, name='search_users'),
    url('^users/perms/(?P<row_id>[0-9]{1,11})/$', views.user_perms, name='user_perms'),
    # Группы
    path('groups/', views.show_groups, name='show_groups'),
    url('^groups/(?P<action>create)/$', views.edit_group, name='create_group'),
    url('^groups/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_group, name='edit_group'),
    url('^groups/perms/(?P<row_id>[0-9]{1,11})/$', views.group_perms, name='group_perms'),
    # Демо-странички
    url('^demo/(?P<action>[a-z_]{1,20})/$', views.demo, name='demo'),
    # Проверка сентряка
    path('check_sentry/', views.check_sentry, name='check_sentry'),
]