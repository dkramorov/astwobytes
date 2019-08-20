# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'flatcontent'
urlpatterns = [
    url('^admin/(?P<ftype>flatmenu|flatmain|flatpages|flattemplates)/$', views.show_containers, name='show_containers'),
    url('^admin/(?P<ftype>flatmenu|flatmain|flatpages|flattemplates)/(?P<action>create)/$', views.edit_container, name='create_container'),
    url('^admin/(?P<ftype>flatmenu|flatmain|flatpages|flattemplates)/(?P<action>edit|drop|copy|show|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_container, name='edit_container'),
    url('^admin/(?P<ftype>flatmenu|flatmain|flatpages|flattemplates)/positions/$', views.containers_positions, name='containers_positions'),
]
