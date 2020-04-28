# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'promotion'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>promotion|vocabulary)/api/$', views.api, name='api'),
    # админка
    #path('admin/', views.show_promotion, name='show_promotion'),
    #url('^admin/(?P<action>create)/$', views.edit_promotion, name='create_promotion'),
    #url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_promotion, name='edit_promotion'),
    #path('admin/positions/', views.promotion_positions, name='promotion_positions'),
    # аякс-поиск
    #path('promotion/search/', views.search_promotion, name='search_promotion'),

    # админка
    path('admin/vocabulary/', views.show_vocabulary, name='show_vocabulary'),
    url('^admin/vocabulary/(?P<action>create)/$', views.edit_vocabulary, name='create_vocabulary'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_vocabulary, name='edit_vocabulary'),
    path('admin/positions/', views.vocabulary_positions, name='vocabulary_positions'),
    # аякс-поиск
    path('promotion/vocabulary/search/', views.search_vocabulary, name='search_vocabulary'),

]
