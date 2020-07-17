# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'welding'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>welding)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_welding, name='show_welding'),
    url('^admin/(?P<action>create)/$', views.edit_welding, name='create_welding'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_welding, name='edit_welding'),
    path('admin/positions/', views.welding_positions, name='welding_positions'),
    # аякс-поиск
    path('welding/search/', views.search_welding, name='search_welding'),

    # установки
    path('admin/bases/', views.show_bases, name='show_bases'),
    url('^admin/bases/(?P<action>create)/$', views.edit_base, name='create_base'),
    url('^admin/bases/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_base, name='edit_base'),
    path('admin/bases/positions/', views.bases_positions, name='bases_positions'),
    # аякс-поиск
    path('welding/bases/search/', views.search_bases, name='search_bases'),

    # договоры
    path('admin/contracts/', views.show_contracts, name='show_contracts'),
    url('^admin/contracts/(?P<action>create)/$', views.edit_contract, name='create_contract'),
    url('^admin/contracts/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_contract, name='edit_contract'),
    path('admin/contracts/positions/', views.contracts_positions, name='contracts_positions'),
    # аякс-поиск
    path('welding/contracts/search/', views.search_contracts, name='search_contracts'),

    # титулы
    path('admin/tituls/', views.show_tituls, name='show_tituls'),
    url('^admin/tituls/(?P<action>create)/$', views.edit_titul, name='create_titul'),
    url('^admin/tituls/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_titul, name='edit_titul'),
    path('admin/tituls/positions/', views.tituls_positions, name='tituls_positions'),
    # аякс-поиск
    path('welding/tituls/search/', views.search_tituls, name='search_tituls'),

    # линии
    path('admin/lines/', views.show_lines, name='show_lines'),
    url('^admin/lines/(?P<action>create)/$', views.edit_line, name='create_line'),
    url('^admin/lines/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_line, name='edit_line'),
    path('admin/lines/positions/', views.lines_positions, name='lines_positions'),
    # аякс-поиск
    path('welding/lines/search/', views.search_lines, name='search_lines'),

    # изометрические схемы
    path('admin/schemes/', views.show_schemes, name='show_schemes'),
    url('^admin/schemes/(?P<action>create)/$', views.edit_scheme, name='create_scheme'),
    url('^admin/schemes/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_scheme, name='edit_scheme'),
    path('admin/schemes/positions/', views.schemes_positions, name='schemes_positions'),
    # аякс-поиск
    path('welding/schemes/search/', views.search_schemes, name='search_schemes'),

    # стыки
    path('admin/joints/', views.show_joints, name='show_joints'),
    url('^admin/joints/(?P<action>create)/$', views.edit_joint, name='create_joint'),
    url('^admin/joints/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_joint, name='edit_joint'),
    path('admin/joints/positions/', views.joints_positions, name='joints_positions'),
    # аякс-поиск
    path('welding/joints/search/', views.search_joints, name='search_joints'),

    # материалы
    path('admin/materials/', views.show_materials, name='show_materials'),
    url('^admin/materials/(?P<action>create)/$', views.edit_material, name='create_material'),
    url('^admin/materials/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_material, name='edit_material'),
    path('admin/materials/positions/', views.materials_positions, name='materials_positions'),
    # аякс-поиск
    path('welding/materials/search/', views.search_materials, name='search_materials'),

    # типы соединений
    path('admin/join_types/', views.show_join_types, name='show_join_types'),
    url('^admin/join_types/(?P<action>create)/$', views.edit_join_type, name='create_join_type'),
    url('^admin/join_types/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_join_type, name='edit_join_type'),
    path('admin/join_types/positions/', views.join_types_positions, name='join_types_positions'),
    # аякс-поиск
    path('welding/join_types/search/', views.search_join_types, name='search_join_types'),

    # сварщики
    path('admin/welders/', views.show_welders, name='show_welders'),
    url('^admin/welders/(?P<action>create)/$', views.edit_welder, name='create_welder'),
    url('^admin/welders/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_welder, name='edit_welder'),
    path('admin/welders/positions/', views.welders_positions, name='welders_positions'),
    # аякс-поиск
    path('welding/welders/search/', views.search_welders, name='search_welders'),

]
