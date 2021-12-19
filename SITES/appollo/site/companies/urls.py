# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'companies'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>companies)/api/$', views.api, name='api'),

    path('admin/companies/update_app/', views.update_app, name='update_app'),

    # админка филиалы
    path('admin/companies/', views.show_companies, name='show_companies'),
    url('^admin/companies/(?P<action>create)/$', views.edit_company, name='create_company'),
    url('^admin/companies/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_company, name='edit_company'),
    path('admin/companies/positions/', views.companies_positions, name='companies_positions'),
    # аякс-поиск
    path('companies/search/', views.search_companies, name='search_companies'),

    # админка компании
    path('admin/main_companies/', views.show_main_companies, name='show_main_companies'),
    url('^admin/main_companies/(?P<action>create)/$', views.edit_main_company, name='create_main_company'),
    url('^admin/main_companies/(?P<action>edit|drop|img|img_view)/(?P<row_id>[0-9]{1,11})/$', views.edit_main_company, name='edit_main_company'),
    path('admin/main_companies/positions/', views.main_companies_positions, name='main_companies_positions'),
    # аякс-поиск
    path('main_companies/search/', views.search_main_companies, name='search_main_companies'),

    # админка контактов
    path('admin/contacts/', views.show_contacts, name='show_contacts'),
    url('^admin/contacts/(?P<action>create)/$', views.edit_contact, name='create_contact'),
    url('^admin/contacts/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_contact, name='edit_contact'),
    path('admin/contacts/positions/', views.contacts_positions, name='contacts_positions'),
    # аякс-поиск
    path('contacts/search/', views.search_contacts, name='search_contacts'),
]
