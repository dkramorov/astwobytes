# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def my_ip(request):
    """Апи-метод для получения ip-адреса"""
    result = {
        'ip': request.META.get('REMOTE_ADDR'),
        'ip_forwarded': request.META.get('HTTP_X_FORWARDED_FOR'),
    }
    return JsonResponse(result, safe=False)

