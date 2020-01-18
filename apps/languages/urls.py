# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'languages'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>lanuages)/api/$', views.api, name='api'),

    path('admin/', views.show_translates, name='show_translates'),
    url('^admin/(?P<action>create)/$', views.edit_translate, name='create_translate'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_translate, name='edit_translate'),
    path('admin/positions/', views.translates_positions, name='translates_positions'),
]
