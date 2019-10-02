# -*- coding: utf-8 -*-
#from django.http import HttpResponse
from django.shortcuts import render

def index(request, *args, **kwargs):
    """Фронтовый робот"""
    context = {}
    template = 'binary_com_index.html'
    return render(request, template, context)
