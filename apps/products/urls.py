# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'products'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>products)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_products, name='show_products'),
    url('^admin/(?P<action>create)/$', views.edit_product, name='create_product'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_product, name='edit_product'),
    path('admin/positions/', views.products_positions, name='products_positions'),
    # аякс-поиск
    path('products/search/', views.search_products, name='search_products'),
]
