# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views, welder_views, company_views

app_name = 'welding'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>welding)/api/$', views.api, name='api'),
    # Документация PDF
    url('^manual/(?P<action>welder)/$', views.manual, name='manual'),
    # ---------------
    # заявки на стыки
    # ---------------
    path('admin/', views.show_welding, name='show_welding'),
    url('^admin/(?P<state>new|in_progress|complete|in_repair)/$', views.show_welding, name='show_welding'),
    url('^admin/(?P<action>create|form)/$', views.edit_welding, name='create_welding'),
    url('^admin/(?P<action>edit|drop|img|form|pdf|file|state)/(?P<row_id>[0-9]{1,11})/$', views.edit_welding, name='edit_welding'),
    path('admin/positions/', views.welding_positions, name='welding_positions'),
    # аякс-поиск
    path('welding/search/', views.search_welding, name='search_welding'),

    # файлы заявок на стык
    path('admin/welding_files/', views.show_welding_files, name='show_welding_files'),
    url('^admin/welding_files/(?P<action>edit|drop|download)/(?P<row_id>[0-9]{1,11})/$', views.edit_welding_file, name='edit_welding_file'),

    # заключения на заявки на стыки
    path('admin/conclusions/', views.show_conclusions, name='show_conclusions'),
    url('^admin/conclusions/(?P<action>create)/$', views.edit_conclusion, name='create_conclusion'),
    url('^admin/conclusions/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_conclusion, name='edit_conclusion'),

    # ------------------------
    # компании (company_views)
    # ------------------------
    path('admin/companies/', company_views.show_companies, name='show_companies'),
    url('^admin/companies/(?P<action>create)/$', company_views.edit_company, name='create_company'),
    url('^admin/companies/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', company_views.edit_company, name='edit_company'),
    path('admin/companies/positions/', company_views.companies_positions, name='companies_positions'),
    # аякс-поиск
    path('welding/companies/search/', company_views.search_companies, name='search_companies'),

    # объекты
    path('admin/subjects/', company_views.show_subjects, name='show_subjects'),
    url('^admin/subjects/(?P<action>create)/$', company_views.edit_subject, name='create_subject'),
    url('^admin/subjects/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', company_views.edit_subject, name='edit_subject'),
    path('admin/subjects/positions/', company_views.subjects_positions, name='subjects_positions'),
    # аякс-поиск
    path('welding/subjects/search/', company_views.search_subjects, name='search_subjects'),

    # титулы
    path('admin/tituls/', company_views.show_tituls, name='show_tituls'),
    url('^admin/tituls/(?P<action>create)/$', company_views.edit_titul, name='create_titul'),
    url('^admin/tituls/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', company_views.edit_titul, name='edit_titul'),
    path('admin/tituls/positions/', company_views.tituls_positions, name='tituls_positions'),
    # аякс-поиск
    path('welding/tituls/search/', company_views.search_tituls, name='search_tituls'),

    # установки
    path('admin/bases/', company_views.show_bases, name='show_bases'),
    url('^admin/bases/(?P<action>create)/$', company_views.edit_base, name='create_base'),
    url('^admin/bases/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', company_views.edit_base, name='edit_base'),
    path('admin/bases/positions/', company_views.bases_positions, name='bases_positions'),
    # аякс-поиск
    path('welding/bases/search/', company_views.search_bases, name='search_bases'),

    # линии
    path('admin/lines/', company_views.show_lines, name='show_lines'),
    url('^admin/lines/(?P<action>create)/$', company_views.edit_line, name='create_line'),
    url('^admin/lines/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', company_views.edit_line, name='edit_line'),
    path('admin/lines/positions/', company_views.lines_positions, name='lines_positions'),
    # аякс-поиск
    path('welding/lines/search/', company_views.search_lines, name='search_lines'),

    # стыки
    path('admin/joints/', company_views.show_joints, name='show_joints'),
    url('^admin/joints/(?P<action>create)/$', company_views.edit_joint, name='create_joint'),
    url('^admin/joints/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', company_views.edit_joint, name='edit_joint'),
    path('admin/joints/positions/', company_views.joints_positions, name='joints_positions'),
    # аякс-поиск
    path('welding/joints/search/', company_views.search_joints, name='search_joints'),

    # -----------------------
    # сварщики (welder_views)
    # -----------------------
    path('admin/welders/', welder_views.show_welders, name='show_welders'),
    url('^admin/welders/(?P<action>create)/$', welder_views.edit_welder, name='create_welder'),
    url('^admin/welders/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', welder_views.edit_welder, name='edit_welder'),
    path('admin/welders/positions/', welder_views.welders_positions, name='welders_positions'),
    # аякс-поиск
    path('welding/welders/search/', welder_views.search_welders, name='search_welders'),

    # сварщики - гарантийные письма (welder_views)
    path('admin/letters_of_guarantee/', welder_views.show_letters_of_guarantee, name='show_letters_of_guarantee'),
    url('^admin/letters_of_guarantee/(?P<action>create)/$', welder_views.edit_letter_of_guarantee, name='create_letter_of_guarantee'),
    url('^admin/letters_of_guarantee/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', welder_views.edit_letter_of_guarantee, name='edit_letter_of_guarantee'),
    path('admin/letters_of_guarantee/positions/', welder_views.letters_of_guarantee_positions, name='letters_of_guarantee_positions'),
    # аякс-поиск
    path('welding/letters_of_guarantee/search/', welder_views.search_letters_of_guarantee, name='search_letters_of_guarantee'),

    # сварщики - акты ВИК (welder_views)
    path('admin/viks/', welder_views.show_viks, name='show_viks'),
    url('^admin/viks/(?P<action>create)/$', welder_views.edit_vik, name='create_vik'),
    url('^admin/viks/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', welder_views.edit_vik, name='edit_vik'),
    path('admin/viks/positions/', welder_views.viks_positions, name='viks_positions'),
    # аякс-поиск
    path('welding/viks/search/', welder_views.search_viks, name='search_viks'),

    # сварщики - УЗК/РК контроль (welder_views)
    path('admin/controlk/', welder_views.show_controlk, name='show_controlk'),
    url('^admin/controlk/(?P<action>create)/$', welder_views.edit_controlk, name='create_controlk'),
    url('^admin/controlk/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', welder_views.edit_controlk, name='edit_controlk'),
    path('admin/controlk/positions/', welder_views.controlk_positions, name='controlk_positions'),
    # аякс-поиск
    path('welding/controlk/search/', welder_views.search_controlk, name='search_controlk'),

    # сварщики - проведение КСС (welder_views)
    path('admin/holding_kss/', welder_views.show_holding_kss, name='show_holding_kss'),
    url('^admin/holding_kss/(?P<action>create)/$', welder_views.edit_holding_kss, name='create_holding_kss'),
    url('^admin/holding_kss/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', welder_views.edit_holding_kss, name='edit_holding_kss'),
    path('admin/holding_kss/positions/', welder_views.holding_kss_positions, name='holding_kss_positions'),
    # аякс-поиск
    path('welding/holding_kss/search/', welder_views.search_holding_kss, name='search_holding_kss'),

    # сварщики - Мехиспытание (welder_views)
    path('admin/mechtest/', welder_views.show_mechtest, name='show_mechtest'),
    url('^admin/mechtest/(?P<action>create)/$', welder_views.edit_mechtest, name='create_mechtest'),
    url('^admin/mechtest/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', welder_views.edit_mechtest, name='edit_mechtest'),
    path('admin/mechtest/positions/', welder_views.mechtest_positions, name='mechtest_positions'),
    # аякс-поиск
    path('welding/mechtest/search/', welder_views.search_mechtest, name='search_mechtest'),

    # сварщики - НАКС (welder_views)
    path('admin/nax/', welder_views.show_nax, name='show_nax'),
    url('^admin/nax/(?P<action>create)/$', welder_views.edit_nax, name='create_nax'),
    url('^admin/nax/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', welder_views.edit_nax, name='edit_nax'),
    path('admin/nax/positions/', welder_views.nax_positions, name='nax_positions'),
    # аякс-поиск
    path('welding/nax/search/', welder_views.search_nax, name='search_nax'),

    # сварщики - Лист допуска (welder_views)
    path('admin/admission_sheet/', welder_views.show_admission_sheet, name='show_admission_sheet'),
    url('^admin/admission_sheet/(?P<action>create)/$', welder_views.edit_admission_sheet, name='create_admission_sheet'),
    url('^admin/admission_sheet/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', welder_views.edit_admission_sheet, name='edit_admission_sheet'),
    path('admin/admission_sheet/positions/', welder_views.admission_sheet_positions, name='admission_sheet_positions'),
    # аякс-поиск
    path('welding/admission_sheet/search/', welder_views.search_admission_sheet, name='search_admission_sheet'),

    # -----------
    # логирование
    # -----------
    path('admin/logs/welding_joint_state/', views.show_welding_joint_state, name='show_welding_joint_state'),
    url('^admin/logs/welding_joint_state/(?P<action>create)/$', views.edit_welding_joint_state, name='create_welding_joint_state'),
    url('^admin/logs/welding_joint_state/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_welding_joint_state, name='edit_welding_joint_state'),
]
