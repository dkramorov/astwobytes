# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'login'
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('users/', views.show_users, name='show_users'),
    url('^users/(?P<action>create)/$', views.edit_user, name='create_user'),
    url('^users/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_user, name='edit_user'),
    url('^users/check_username/$', views.check_username, name='check_username'),
    url('^demo/(?P<action>[a-z_]{1,20})/$', views.demo, name='demo'),
]
