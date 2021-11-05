# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'former'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>former)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_former, name='show_former'),
    url('^admin/(?P<action>create)/$', views.edit_former, name='create_former'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_former, name='edit_former'),
    path('admin/positions/', views.former_positions, name='former_positions'),
    # аякс-поиск
    path('former/search/', views.search_former, name='search_former'),
]
