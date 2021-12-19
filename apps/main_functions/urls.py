# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'main_functions'
urlpatterns = [
    url('^my_ip/$', views.my_ip, name='my_ip'),
    url('^test_statuses/$', views.test_statuses, name='test_statuses'),
    url('^(?P<app>[a-z_]{1,20})/admin/settings/$', views.settings, name='settings'),
    path('tasks/admin/', views.show_tasks, name='show_tasks'),
    url('^tasks/admin/(?P<action>create)/$', views.edit_task, name='create_task'),
    url('^tasks/admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_task, name='edit_task'),
    path('get_captcha/', views.get_captcha, name='get_captcha'),
]
