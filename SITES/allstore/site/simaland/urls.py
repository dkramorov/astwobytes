# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'simaland'
urlpatterns = [
    # сайт
    path('cart/', views.simaland_cart, name='simaland_cart'),
    path('credentials/', views.simaland_credentials, name='simaland_credentials'),
    path('orders/', views.simaland_orders, name='simaland_orders'),
    path('set_pickup_point/', views.set_pickup_point, name='set_pickup_point'),
    path('get_pickup_point/', views.get_pickup_point, name='get_pickup_point'),

    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>pickup_points)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_pickup_points, name='show_pickup_points'),
    url('^admin/(?P<action>create)/$', views.edit_pickup_point, name='create_pickup_point'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_pickup_point, name='edit_pickup_point'),
]
