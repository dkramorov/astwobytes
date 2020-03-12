# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'catalogue'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>rubrics)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_rubrics, name='show_rubrics'),
    url('^admin/(?P<action>create)/$', views.edit_rubric, name='create_rubric'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_rubric, name='edit_rubric'),
    path('admin/positions/', views.rubrics_positions, name='rubrics_positions'),
    # аякс-поиск
    path('rubrics/search/', views.search_rubrics, name='search_rubrics'),
]
