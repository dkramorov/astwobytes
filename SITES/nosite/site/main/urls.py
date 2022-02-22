# -*- coding:utf-8 -*-
from django.urls import path, include, re_path
from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.demo, name='demo'),
    path('PIP_SI_CLAIM_COUNT_REQ/v20190705', views.pip_si_claim_count_req, name='pip_si_claim_count_req'),
    path('PIP_SI_CLAIM_REQ_/v1.0.0', views.pip_si_claim_req_, name='pip_si_claim_req_'),
]

