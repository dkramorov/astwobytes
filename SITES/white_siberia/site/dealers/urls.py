# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'dealers'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>dealers)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_dealers, name='show_dealers'),
    url('^admin/(?P<action>create)/$', views.edit_dealer, name='create_dealer'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_dealer, name='edit_dealer'),
    path('admin/positions/', views.dealers_positions, name='dealers_positions'),
    # аякс-поиск
    path('dealers/search/', views.search_dealers, name='search_dealers'),
]
