# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect


CUR_APP = 'main'

def home(request):
    """Главная страничка сайта"""
    return redirect('/auth/')

