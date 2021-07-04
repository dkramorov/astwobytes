# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from apps.jabber import views

app_name = 'jabber'
urlpatterns = [
    path('admin/', views.jabber_chat, name='show_jabber'),
    url('^admin/(?P<action>create)/$', views.jabber_chat, name='create_jabber'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.jabber_chat, name='edit_jabber'),
]
