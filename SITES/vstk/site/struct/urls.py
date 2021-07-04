# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'struct'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>struct)/api/$', views.api, name='api'),
    # Структура - Объект
    path('admin/', views.show_struct, name='show_struct'),
    url('^admin/(?P<action>create)/$', views.edit_struct, name='create_struct'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_struct, name='edit_struct'),
    path('admin/positions/', views.struct_positions, name='struct_positions'),
    # аякс-поиск
    path('struct/search/', views.search_struct, name='search_struct'),

    # Исходные данные
    path('admin/source_data/', views.show_source_data, name='show_source_data'),
    url('^admin/source_data/(?P<action>create)/$', views.edit_source_data, name='create_source_data'),
    url('^admin/source_data/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_source_data, name='edit_source_data'),
    path('admin/source_data/positions/', views.source_data_positions, name='source_data_positions'),
    # аякс-поиск
    path('struct/source_data/search/', views.search_source_data, name='search_source_data'),
]
