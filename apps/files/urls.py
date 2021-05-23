# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from apps.files import views

app_name = 'files'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>files)/api/$', views.api, name='api'),

    path('admin/', views.show_files, name='show_files'),
    url('^admin/(?P<action>create)/$', views.edit_file, name='create_file'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_file, name='edit_file'),
    path('admin/positions/', views.files_positions, name='files_positions'),
]
