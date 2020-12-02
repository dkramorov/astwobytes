# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'spamcha'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>spam_tables|spam_rows|email_accounts|black_list)/api/$', views.api, name='api'),
    # ----------------
    # Таблицы рассылок
    # ----------------
    path('admin/', views.show_spam_tables, name='show_spam_tables'),
    url('^admin/(?P<action>create)/$', views.edit_spam_table, name='create_spam_table'),
    url('^admin/(?P<action>edit|drop|img|html|html_result)/(?P<row_id>[0-9]{1,11})/$', views.edit_spam_table, name='edit_spam_table'),
    path('admin/positions/', views.spam_tables_positions, name='spam_tables_positions'),
    path('images/', views.spam_tables_images, name='spam_tables_images'),
    # --------------------------
    # Получатели таблиц рассылок
    # --------------------------
    url('^admin/spam_table/(?P<spam_table_id>[0-9]{1,11})/$', views.show_spam_rows, name='show_spam_rows'),
    url('^admin/spam_table/(?P<spam_table_id>[0-9]{1,11})/(?P<action>create)/$', views.edit_spam_row, name='create_spam_row'),
    url('^admin/spam_table/(?P<spam_table_id>[0-9]{1,11})/(?P<action>edit|drop|send|send_html)/(?P<row_id>[0-9]{1,11})/$', views.edit_spam_row, name='edit_spam_row'),
    url('^admin/spam_table/(?P<spam_table_id>[0-9]{1,11})/positions/$', views.spam_rows_positions, name='spam_rows_positions'),
    # --------------
    # Email аккаунты
    # --------------
    path('admin/email_accounts/', views.show_email_accounts, name='show_email_accounts'),
    url('^admin/email_accounts/(?P<action>create)/$', views.edit_email_account, name='create_email_account'),
    url('^admin/email_accounts/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_email_account, name='edit_email_account'),
    path('admin/email_accounts/positions/', views.email_accounts_positions, name='email_accounts_positions'),
    path('admin/email_accounts/search/', views.search_email_accounts, name='search_email_accounts'),
    # --------------------
    # Черный список emails
    # --------------------
    path('admin/black_list/', views.show_black_list, name='show_black_list'),
    url('^admin/black_list/(?P<action>create)/$', views.edit_black_list, name='create_black_list'),
    url('^admin/black_list/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_black_list, name='edit_black_list'),
    path('admin/black_list/positions/', views.black_list_positions, name='black_list_positions'),
    # ------------
    # Смс телефоны
    # ------------
    path('admin/sms_phones/', views.show_sms_phones, name='show_sms_phones'),
    url('^admin/sms_phones/(?P<action>create)/$', views.edit_sms_phone, name='create_sms_phone'),
    url('^admin/sms_phones/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_sms_phone, name='edit_sms_phone'),
    path('admin/sms_phones/positions/', views.sms_phones_positions, name='sms_phones_positions'),
    # аякс-поиск
    path('sms_phones/search/', views.search_sms_phones, name='search_sms_phones'),
]
