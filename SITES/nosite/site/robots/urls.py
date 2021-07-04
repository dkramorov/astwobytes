# -*- coding:utf-8 -*-
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'robots'
urlpatterns = [
    # получение по апи всех данных (т/к не секретно)
    url('^(?P<action>robots|test_scenarios|search_queries|sites)/api/$', views.api, name='api'),
    url('^(?P<action>search_queries)/import_xlsx/$', views.import_xlsx, name='import_xlsx'),
    # админка - роботы
    path('admin/', views.show_robots, name='show_robots'),
    url('^admin/(?P<action>create)/$', views.edit_robot, name='create_robot'),
    url('^admin/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_robot, name='edit_robot'),
    path('admin/positions/', views.robots_positions, name='robots_positions'),
    path('robots/search/', views.search_robots, name='search_robots'),
    # админка - сценарии
    path('admin/test_scenarios/', views.show_test_scenarios, name='show_test_scenarios'),
    url('^admin/test_scenarios/(?P<action>create)/$', views.edit_test_scenario, name='create_test_scenario'),
    url('^admin/test_scenarios/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_test_scenario, name='edit_test_scenario'),
    path('admin/test_scenarios/positions/', views.test_scenarios_positions, name='test_scenarios_positions'),
    path('test_scenarios/search/', views.search_test_scenarios, name='search_test_scenarios'),
    # админка - сайты
    path('admin/sites/', views.show_sites, name='show_sites'),
    url('^admin/sites/(?P<action>create)/$', views.edit_site, name='create_site'),
    url('^admin/sites/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_site, name='edit_site'),
    path('admin/sites/positions/', views.sites_positions, name='sites_positions'),
    path('sites/search/', views.search_sites, name='search_sites'),
    # админка - профили роботов
    path('admin/robot_profiles/', views.show_robot_profiles, name='show_robot_profiles'),
    url('^admin/robot_profiles/(?P<action>create)/$', views.edit_robot_profile, name='create_robot_profile'),
    url('^admin/robot_profiles/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_robot_profile, name='edit_robot_profile'),
    path('admin/robot_profiles/positions/', views.robot_profiles_positions, name='robot_profiles_positions'),
    path('robot_profiles/search/', views.search_robot_profiles, name='search_robot_profiles'),
    # админка - поисковые запросы
    path('admin/search_queries/', views.show_search_queries, name='show_search_queries'),
    url('^admin/search_queries/(?P<action>create)/$', views.edit_search_query, name='create_search_query'),
    url('^admin/search_queries/(?P<action>edit|drop|img)/(?P<row_id>[0-9]{1,11})/$', views.edit_search_query, name='edit_search_query'),
    path('admin/search_queries/positions/', views.search_queries_positions, name='search_queries_positions'),
    path('search_queries/search/', views.search_search_queries, name='search_search_queries'),

    # апи - информация от робота
    path('inform_server/', views.inform_server, name='inform_server'),
    # апи - обновление робота
    path('updater/', views.updater, name='updater'),
]
