# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'product_colors'
urlpatterns = [
    # Получение/сохранение цвета для товара
    url('^get_color/$', views.get_color, name='get_color'),
    url('^set_color/$', views.set_color, name='set_color'),
]
