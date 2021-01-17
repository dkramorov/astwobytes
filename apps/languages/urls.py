# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'languages'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>lanuages)/api/$', views.api, name='api'),
    path('admin/select_language/', views.select_language, name='select_language'),
    url('^admin/select_language/(?P<lang>[a-z]{3})/$', views.select_language, name='select_language'),

    path('admin/', views.show_translates, name='show_translates'),
    url('^admin/(?P<action>create)/$', views.edit_translate, name='create_translate'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_translate, name='edit_translate'),
    path('admin/positions/', views.translates_positions, name='translates_positions'),
    # выбор языка
    url('^pick/(?P<lang>[a-z]{3})/$', views.pick_language, name='pick_language'),
]
