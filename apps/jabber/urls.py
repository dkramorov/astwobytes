# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from apps.jabber import views

app_name = 'jabber'
urlpatterns = [
    #path('admin/', views.jabber_chat, name='show_jabber'),
    #url('^admin/(?P<action>create)/$', views.jabber_chat, name='create_jabber'),
    #url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.jabber_chat, name='edit_jabber'),

    # register user
    path('admin/registrations/', views.show_registrations, name='show_registrations'),
    url('^admin/registrations/(?P<action>create)/$', views.edit_registration, name='create_registration'),
    url('^admin/registrations/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_registration, name='edit_registration'),

    # tokens
    path('admin/tokens/', views.show_tokens, name='show_tokens'),
    url('^admin/tokens/(?P<action>create)/$', views.edit_token, name='create_token'),
    url('^admin/tokens/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_token, name='edit_token'),

    path('register_user/', views.register_user, name='register_user'),
    path('test_notification/', views.test_notification, name='test_notification'),
    path('vcard/', views.vcard, name='vcard'),
    url('^notification/(?P<app_id>[0-9]{1,11})/$', views.notification, name='notification'),

    path('get_jabber_users/', views.get_jabber_users, name='get_jabber_users'),
]
