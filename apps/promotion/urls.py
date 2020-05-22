# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'promotion'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>promotion|vocabulary)/api/$', views.api, name='api'),
    url('^(?P<action>promotion|vocabulary)/import_xlsx/$', views.import_xlsx, name='import_xlsx'),

    # админка отчета по посещению сайтов
    path('admin/svisits/', views.show_svisits, name='show_svisits'),
    url('^admin/svisits/(?P<action>create)/$', views.edit_svisit, name='create_svisit'),
    url('^admin/svisits/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_svisit, name='edit_svisit'),
    path('admin/svisits/positions/', views.svisits_positions, name='svisits_positions'),
    # импорт данных
    path('svisits/import/', views.svisits_import, name='svisits_import'),

    # админка словаря
    path('admin/vocabulary/', views.show_vocabulary, name='show_vocabulary'),
    url('^admin/vocabulary/(?P<action>create)/$', views.edit_vocabulary, name='create_vocabulary'),
    url('^admin/vocabulary/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_vocabulary, name='edit_vocabulary'),
    path('admin/vocabulary/positions/', views.vocabulary_positions, name='vocabulary_positions'),
    # аякс-поиск
    path('vocabulary/search/', views.search_vocabulary, name='search_vocabulary'),

    # сео-отчет
    path('admin/seo_report/', views.show_seo_report, name='show_seo_report'),
]
