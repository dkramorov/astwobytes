# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'flatcontent'
urlpatterns = [
    # ----------
    # containers
    # ----------
    url('^admin/tree_co/$', views.tree_co, name='tree_co'),
    url('^admin/(?P<ftype>flatmenu|flatmain|flatpages|flattemplates|flatcat)/$', views.show_containers, name='show_containers'),
    url('^admin/(?P<ftype>flatmenu|flatmain|flatpages|flattemplates|flatcat)/(?P<action>create)/$', views.edit_container, name='create_container'),
    url('^admin/(?P<ftype>flatmenu|flatmain|flatpages|flattemplates|flatcat)/(?P<action>edit|drop|copy|show|img|tree)/(?P<row_id>[0-9]{1,11})/$', views.edit_container, name='edit_container'),
    url('^admin/(?P<ftype>flatmenu|flatmain|flatpages|flattemplates|flatcat)/positions/$', views.containers_positions, name='containers_positions'),
    url('^search_containers/$', views.search_containers, name='search_containers'),
    # --------------------------------------------
    # blocks and blocks children inside containers
    # --------------------------------------------
    url('^admin/(?P<ftype>flatmenu|flatmain|flatpages|flattemplates|flatcat)/(?P<container_id>[0-9]{1,11})/$', views.show_blocks, name='show_blocks'),
    url('^admin/(?P<ftype>flatmenu|flatmain|flatpages|flattemplates|flatcat)/(?P<container_id>[0-9]{1,11})/(?P<action>create)/$', views.edit_block, name='create_block'),
    url('^admin/(?P<ftype>flatmenu|flatmain|flatpages|flattemplates|flatcat)/(?P<container_id>[0-9]{1,11})/(?P<action>edit|drop|copy|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_block, name='edit_block'),
    url('^admin/(?P<ftype>flatmenu|flatmain|flatpages|flattemplates|flatcat)/(?P<container_id>[0-9]{1,11})/positions/$', views.blocks_positions, name='blocks_positions'),
    url('^search_blocks/$', views.search_blocks, name='search_blocks'),
]
