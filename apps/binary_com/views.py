# -*- coding: utf-8 -*-
import json
import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect

def index(request, *args, **kwargs):
    """Фронтовый робот"""
    context = {}
    template = 'binary_com_index.html'
    return render(request, template, context)

@csrf_exempt
def generate_report(request, *args, **kwargs):
    """Создание отчета plotly по полученным данным"""
    result = {}

    now = datetime.datetime.today()

    if request.body:
      body = json.loads(request.body)
      token = body.get('token', '')
      ticks_data = body.get('ticks_data', [])
      deals_data = body.get('deals_data', [])

    # Нихрена не пашет
    #from django.core import management
    #management.call_command('test_plotly', image=True)

    return JsonResponse(result, safe=False)
