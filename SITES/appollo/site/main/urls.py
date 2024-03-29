# -*- coding:utf-8 -*-
from django.urls import path, include, re_path
from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    # Главная страничка сайта
    path('', views.home, name='home'),
    # Настройки приложений (переопределяем)
    url('^(?P<app>[a-z_]{1,20})/admin/settings/$', views.site_settings, name='settings'),
    # demo
    path('demo/', views.demo, name='demo'),
    # Каталог
    url('^cat/$', views.cat_on_site, name='cat_on_site'),
    url('^cat/(?P<link>.+)/$', views.cat_on_site, name='cat_on_site'),
    url('^product/(?P<product_id>[0-9]+)/$', views.product_on_site, name='product_on_site'),
    url('^product/(?P<link>[a-z0-9_-]+)/$', views.product_by_link, name='product_by_link'),
    # feedback
    path('feedback/', views.feedback, name='feedback'),
    # Личный кабинет
    path('registration/', views.registration, name='registration'),
    path('profile/', views.show_profile, name='show_profile'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('confirm_phone/', views.confirm_phone, name='confirm_phone'),
    path('calls_history/', views.calls_history, name='calls_history'),

    # Оформление заказа
    path('shop/cart/', views.show_cart, name='show_cart'),
    path('shop/checkout/', views.checkout, name='checkout'),

    # Телефоны
    url('^phones/$', views.phones_cat, name='phones_cat'),
    url('^phones/(?P<link>.+)/$', views.phones_cat, name='phones_cat'),

]

