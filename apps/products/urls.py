# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'products'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>products|props|pvalues)/api/$', views.api, name='api'),
    url('^(?P<action>products|props|pvalues)/import_xlsx/$', views.import_xlsx, name='import_xlsx'),

    # админка
    path('admin/', views.show_products, name='show_products'),
    url('^admin/(?P<action>create)/$', views.edit_product, name='create_product'),
    url('^admin/(?P<action>edit|drop|img|copy)/(?P<row_id>[0-9]{1,11})/$', views.edit_product, name='edit_product'),
    path('admin/positions/', views.products_positions, name='products_positions'),

    # аякс-поиск товаров
    path('search/', views.search_products, name='search_products'),

    # фотки товаров/услуг
    path('admin/photos/', views.show_photos, name='show_photos'),
    url('^admin/photos/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_photo, name='edit_photo'),

    # товары по категории (блоку)
    url('^admin/show_cats_products/$', views.show_cats_products, name='show_cats_products'),
    url('^admin/edit_cat_product/(?P<action>create)/$', views.edit_cat_product, name='create_cat_product'),
    url('^admin/edit_cat_product/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_cat_product, name='edit_cat_product'),

    # свойства товаров/услуг
    path('admin/props/', views.show_props, name='show_props'),
    url('^admin/props/(?P<action>create)/$', views.edit_prop, name='create_prop'),
    url('^admin/props/(?P<action>edit|drop|img|pvalue)/(?P<row_id>[0-9]{1,11})/$', views.edit_prop, name='edit_prop'),
    # аякс-поиск свойств
    path('props/search/', views.search_props, name='search_props'),

    # значения свойств товаров/услуг
    path('admin/pvalues/', views.show_pvalues, name='show_pvalues'),
    path('admin/pvalues/positions/', views.pvalues_positions, name='pvalues_positions'),
    # аякс-поиск значений свойств
    path('pvalues/search/', views.search_pvalues, name='search_pvalues'),

    # привязка/удаление свойств к товару/услуге
    path('admin/product_pvalues/', views.show_product_pvalues, name='show_product_pvalues'),
    url('^admin/product_pvalues/(?P<action>create)/$', views.edit_product_pvalue, name='create_product_pvalue'),
    url('^admin/product_pvalues/(?P<action>edit|drop)/(?P<row_id>[0-9]{1,11})/$', views.edit_product_pvalue, name='edit_product_pvalue'),

    # типы цен товаров/услуг
    path('admin/costs/', views.show_costs, name='show_costs'),
    url('^admin/costs/(?P<action>create)/$', views.edit_cost, name='create_cost'),
    url('^admin/costs/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_cost, name='edit_cost'),
    path('admin/costs/positions/', views.costs_positions, name='costs_positions'),

    # аякс-поиск свойств
    path('costs/search/', views.search_costs, name='search_costs'),

    # получение фасетных фильтров по категории
    url('^facet_filters/(?P<cat_id>[0-9]{1,11})/$', views.facet_filters, name='facet_filters'),
]
