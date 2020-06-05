# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'personal'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>shoppers)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_shoppers, name='show_shoppers'),
    url('^admin/(?P<action>create)/$', views.edit_shopper, name='create_shopper'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_shopper, name='edit_shopper'),
    path('admin/positions/', views.shoppers_positions, name='shoppers_positions'),
    # аякс-поиск
    path('shoppers/search/', views.search_shoppers, name='search_shoppers'),
    # OAuth авторизация пользователей
    path('oauth/test/', views.oauth_test, name='oauth_test'),
    path('oauth/vk/', views.oauth_vk, name='oauth_vk'),
    path('oauth/yandex/', views.oauth_yandex, name='oauth_yandex'),
]
