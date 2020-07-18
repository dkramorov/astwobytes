# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views, welder_views, company_views, material_views

app_name = 'welding'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>welding)/api/$', views.api, name='api'),
    # админка
    path('admin/', views.show_welding, name='show_welding'),
    url('^admin/(?P<action>create)/$', views.edit_welding, name='create_welding'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_welding, name='edit_welding'),
    path('admin/positions/', views.welding_positions, name='welding_positions'),
    # аякс-поиск
    path('welding/search/', views.search_welding, name='search_welding'),

    # компании (company_views)
    path('admin/companies/', company_views.show_companies, name='show_companies'),
    url('^admin/companies/(?P<action>create)/$', company_views.edit_company, name='create_company'),
    url('^admin/companies/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', company_views.edit_company, name='edit_company'),
    path('admin/companies/positions/', company_views.companies_positions, name='companies_positions'),
    # аякс-поиск
    path('welding/companies/search/', company_views.search_companies, name='search_companies'),

    # установки
    path('admin/bases/', views.show_bases, name='show_bases'),
    url('^admin/bases/(?P<action>create)/$', views.edit_base, name='create_base'),
    url('^admin/bases/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_base, name='edit_base'),
    path('admin/bases/positions/', views.bases_positions, name='bases_positions'),
    # аякс-поиск
    path('welding/bases/search/', views.search_bases, name='search_bases'),

    # договоры
    path('admin/contracts/', views.show_contracts, name='show_contracts'),
    url('^admin/contracts/(?P<action>create)/$', views.edit_contract, name='create_contract'),
    url('^admin/contracts/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_contract, name='edit_contract'),
    path('admin/contracts/positions/', views.contracts_positions, name='contracts_positions'),
    # аякс-поиск
    path('welding/contracts/search/', views.search_contracts, name='search_contracts'),

    # титулы
    path('admin/tituls/', views.show_tituls, name='show_tituls'),
    url('^admin/tituls/(?P<action>create)/$', views.edit_titul, name='create_titul'),
    url('^admin/tituls/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_titul, name='edit_titul'),
    path('admin/tituls/positions/', views.tituls_positions, name='tituls_positions'),
    # аякс-поиск
    path('welding/tituls/search/', views.search_tituls, name='search_tituls'),

    # линии
    path('admin/lines/', views.show_lines, name='show_lines'),
    url('^admin/lines/(?P<action>create)/$', views.edit_line, name='create_line'),
    url('^admin/lines/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_line, name='edit_line'),
    path('admin/lines/positions/', views.lines_positions, name='lines_positions'),
    # аякс-поиск
    path('welding/lines/search/', views.search_lines, name='search_lines'),

    # изометрические схемы
    path('admin/schemes/', views.show_schemes, name='show_schemes'),
    url('^admin/schemes/(?P<action>create)/$', views.edit_scheme, name='create_scheme'),
    url('^admin/schemes/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_scheme, name='edit_scheme'),
    path('admin/schemes/positions/', views.schemes_positions, name='schemes_positions'),
    # аякс-поиск
    path('welding/schemes/search/', views.search_schemes, name='search_schemes'),

    # стыки
    path('admin/joints/', views.show_joints, name='show_joints'),
    url('^admin/joints/(?P<action>create)/$', views.edit_joint, name='create_joint'),
    url('^admin/joints/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_joint, name='edit_joint'),
    path('admin/joints/positions/', views.joints_positions, name='joints_positions'),
    # аякс-поиск
    path('welding/joints/search/', views.search_joints, name='search_joints'),

    # материалы (material_views)
    path('admin/materials/', material_views.show_materials, name='show_materials'),
    url('^admin/materials/(?P<action>create)/$', material_views.edit_material, name='create_material'),
    url('^admin/materials/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', material_views.edit_material, name='edit_material'),
    path('admin/materials/positions/', material_views.materials_positions, name='materials_positions'),
    # аякс-поиск
    path('welding/materials/search/', material_views.search_materials, name='search_materials'),

    # типы соединений
    path('admin/join_types/', views.show_join_types, name='show_join_types'),
    url('^admin/join_types/(?P<action>create)/$', views.edit_join_type, name='create_join_type'),
    url('^admin/join_types/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_join_type, name='edit_join_type'),
    path('admin/join_types/positions/', views.join_types_positions, name='join_types_positions'),
    # аякс-поиск
    path('welding/join_types/search/', views.search_join_types, name='search_join_types'),

    # сварщики (welder_views)
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
]
