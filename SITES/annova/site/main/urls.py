# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    # Главная страничка сайта
    path('', views.home, name='home'),
    # demo
    path('demo/', views.demo, name='demo'),
    # feedback
    path('feedback/', views.feedback, name='feedback'),
    # Оформление заказа
    path('order_form/', views.order_form, name='order_form'),
    path('order_form_cruise/', views.order_form_cruise, name='order_form_cruise'),

    path('shop/cart/', views.show_cart, name='show_cart'),
    path('shop/checkout/', views.checkout, name='checkout'),
    url('^shop/order/(?P<order_id>[0-9]{1,11})/$', views.show_order, name='show_order'),
    url('payment/(?P<provider>sbrf)/(?P<action>success|fail)/$', views.payment, name='payment'),

    url('shop/order/(?P<order_id>[0-9]{1,11})/pdf/$', views.show_pdf_order, name='pdf_order'),

    # Переопределение вывода товаров
    path('products/admin/', views.custom_show_products, name='custom_show_products'),
    path('shop/orders_report/', views.orders_report, name='orders_report'),
]
