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
    # Каталог
    url('^cat/$', views.cat_on_site, name='cat_on_site'),
    url('^cat/(?P<link>.+)/$', views.cat_on_site, name='cat_on_site'),
    url('^product/(?P<product_id>[0-9]+)/$', views.product_on_site, name='product_on_site'),
    url('^product/(?P<link>[a-z0-9_-]+)/$', views.product_by_link, name='product_by_link'),
    # feedback
    path('feedback/', views.feedback, name='feedback'),
    # registration
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout'),
    # Оформление заказа
    path('shop/cart/', views.show_cart, name='show_cart'),
    path('shop/checkout/', views.checkout, name='checkout'),
]
