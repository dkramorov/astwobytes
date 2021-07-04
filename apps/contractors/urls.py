# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from apps.contractors import views

app_name = 'contractors'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>contractors)/api/$', views.api, name='api'),
    url('^(?P<action>contractors)/import_xlsx/$', views.import_xlsx, name='import_xlsx'),
    # админка
    path('admin/', views.show_contractors, name='show_contractors'),
    url('^admin/(?P<action>create)/$', views.edit_contractor, name='create_contractor'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_contractor, name='edit_contractor'),
    path('admin/positions/', views.contractors_positions, name='contractors_positions'),
    # аякс-поиск
    path('contractors/search/', views.search_contractors, name='search_contractors'),
    path('info_by_inn/', views.info_by_inn, name='info_by_inn'),
]
