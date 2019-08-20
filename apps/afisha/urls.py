# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'afisha'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>rubrics|genres|events|places|seances)/api/$', views.api, name='api'),
    # сортировка для всех моделей
    url('^admin/(?P<action>rubrics|genres|events|places|seances)/positions/$', views.model_positions, name='model_positions'),
    # рубрики мест Афиши
    path('admin/rubrics/', views.show_rubrics, name='show_rubrics'),
    url('^admin/rubrics/(?P<action>create)/$', views.edit_rubric, name='create_rubric'),
    url('^admin/rubrics/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_rubric, name='edit_rubric'),
    path('admin/rubrics/search/', views.search_rubrics, name='search_rubrics'),
    # жанры Афиши
    path('admin/genres/', views.show_genres, name='show_genres'),
    url('^admin/genres/(?P<action>create)/$', views.edit_genre, name='create_genre'),
    url('^admin/genres/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_genre, name='edit_genre'),
    path('admin/genres/search/', views.search_genres, name='search_genres'),
    # события Афиши
    path('admin/events/', views.show_events, name='show_events'),
    url('^admin/events/(?P<action>create)/$', views.edit_event, name='create_event'),
    url('^admin/events/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_event, name='edit_event'),
    path('admin/events/search/', views.search_events, name='search_events'),
    # места Афиши
    path('admin/places/', views.show_places, name='show_places'),
    url('^admin/places/(?P<action>create)/$', views.edit_place, name='create_place'),
    url('^admin/places/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_place, name='edit_place'),
    path('admin/places/search/', views.search_places, name='search_places'),
    # сенасы для Афиши
    path('admin/seances/', views.show_seances, name='show_seances'),
    url('^admin/seances/(?P<action>create)/$', views.edit_seance, name='create_seance'),
    url('^admin/seances/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_seance, name='edit_seance'),
]
