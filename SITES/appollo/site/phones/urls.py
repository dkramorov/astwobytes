# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from apps.site.phones import views

app_name = 'phones'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>phones)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_phones, name='show_phones'),
    url('^admin/(?P<action>create)/$', views.edit_phone, name='create_phone'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_phone, name='edit_phone'),
    path('admin/positions/', views.phones_positions, name='phones_positions'),
    # аякс-поиск
    path('phones/search/', views.search_phones, name='search_phones'),
]
