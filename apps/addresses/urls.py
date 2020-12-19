# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'addresses'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>addresses)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_addresses, name='show_addresses'),
    url('^admin/(?P<action>create)/$', views.edit_address, name='create_address'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_address, name='edit_address'),
    path('admin/positions/', views.addresses_positions, name='addresses_positions'),
    # аякс-поиск
    path('addresses/search/', views.search_addresses, name='search_addresses'),
]
