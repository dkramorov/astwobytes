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

    # device contacts
    path('admin/device_contacts/', views.show_device_contacts, name='show_device_contacts'),
    url('^admin/device_contacts/(?P<action>create)/$', views.edit_device_contact, name='create_device_contact'),
    url('^admin/device_contacts/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_device_contact, name='edit_device_contact'),

    path('register_user/', views.register_user, name='register_user'),
    path('vcard/', views.vcard, name='vcard'),
    path('group_vcard/', views.group_vcard, name='group_vcard'),
    url('^notification/(?P<app_id>[0-9a-z-]{1,20})/$', views.notification, name='notification'),
    url('^notification_batch/(?P<app_id>[0-9a-z-]{1,20})/$', views.notification_batch, name='notification_batch'),
    url('^notification_from_bot/(?P<app_id>[0-9a-z-]{1,20})/$', views.notification_from_bot, name='notification_from_bot'),
    path('get_jabber_users/', views.get_jabber_users, name='get_jabber_users'),
    path('set_device_contacts/', views.set_device_contacts, name='set_device_contacts'),

    path('test_push/', views.test_push, name='test_push'),
]
