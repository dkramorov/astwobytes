# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'shop'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>orders)/api/$', views.api, name='api'),
    url('^(?P<action>promocodes)/import_xlsx/$', views.import_xlsx, name='import_xlsx'),

    # Заказы
    path('admin/orders/', views.show_orders, name='show_orders'),
    url('^admin/orders/(?P<action>create)/$', views.edit_order, name='create_order'),
    url('^admin/orders/(?P<action>edit|drop|img|view)/(?P<row_id>[0-9]{1,11})/$', views.edit_order, name='edit_order'),
    path('admin/orders/positions/', views.orders_positions, name='orders_positions'),
    # аякс-поиск
    path('shop/search/orders/', views.search_orders, name='search_orders'),

    # Незавершенные покупки
    path('admin/purchases/', views.show_purchases, name='show_purchases'),
    url('^admin/purchases/(?P<action>create)/$', views.edit_purchase, name='create_purchase'),
    url('^admin/purchases/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_purchase, name='edit_purchase'),
    path('admin/purchases/positions/', views.purchases_positions, name='purchases_positions'),
    # аякс-поиск
    path('shop/search/purchases/', views.search_purchases, name='search_purchases'),
    # корзинка пользователя
    url('^cart/(?P<action>show|add|quantity|drop|promocode)/', views.cart, name='cart'),

    # Транзакции
    path('admin/transactions/', views.show_transactions, name='show_transactions'),
    url('^admin/transactions/(?P<action>create)/$', views.edit_transaction, name='create_transaction'),
    url('^admin/transactions/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_transaction, name='edit_transaction'),
    path('admin/transactions/positions/', views.transactions_positions, name='transactions_positions'),
    # аякс-поиск
    path('shop/search/transactions/', views.search_transactions, name='search_transactions'),

    # Промокоды
    path('admin/promocodes/', views.show_promocodes, name='show_promocodes'),
    url('^admin/promocodes/(?P<action>create)/$', views.edit_promocode, name='create_promocode'),
    url('^admin/promocodes/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_promocode, name='edit_promocode'),
    path('admin/promocodes/positions/', views.promocodes_positions, name='promocodes_positions'),
    # аякс-поиск
    path('shop/search/promocodes/', views.search_promocodes, name='search_promocodes'),
]
