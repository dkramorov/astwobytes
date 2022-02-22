# -*- coding:utf-8 -*-
import json
import time
import datetime

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

CUR_APP = 'main'
main_vars = {
    'singular_obj': 'Главная',
    'template_prefix': 'main_',
    'show_urla': 'home',
}

TASKS_POOL = {
    'finished': False,
    'count': 151,
    'sent': 0,
    'price_seg': 18,
    'companies': [2426, 2425],
}

# DEBUG: ubrr_client.py (getClaims) self.client.SI_CLAIM_REQ(xml)
# client
#   clients
#     SI_CLAIM_REQ
#       wsdl
#         bindings
#           '{URN:TRIGGER_MARKETING}SI_CLAIM_REQBinding'
#             wsdl
#               port_types
#                 '{URN:TRIGGER_MARKETING}SI_CLAIM_REQ'
#                   operations
#                     SI_CLAIM_REQ
#                       output_message
#                         parts
#                           MT_CLAIM_RES
#                             0
#                               type
#                                 elements
#                                   1 -> CLAIMS...
# в wsdl важен порядок полей - нельзя после PRICE_SEG, PHONE_NUMBER1, только до

def demo(request):
    """DEMO"""
    template = 'web/demo.html'
    context = {}
    return render(request, template, context, content_type='application/xhtml+xml')

@csrf_exempt
def pip_si_claim_count_req(request):
    """/PIP_SI_CLAIM_COUNT_REQ/v20190705"""
    # сегменты с компаниями
    context = {
        'price_seg': TASKS_POOL['price_seg'],
        'companies': TASKS_POOL['companies'],
        'count': TASKS_POOL['count'],
    }
    if TASKS_POOL['finished']:
        context['finished'] = True
    template = 'web/pip_si_claim_count_req.html'
    return render(request, template, context, content_type='application/xhtml+xml')

@csrf_exempt
def pip_si_claim_req_(request):
    """/PIP_SI_CLAIM_REQ_/v1.0.0"""
    global TASKS_POOL
    template = 'web/pip_si_claim_req_.html'
    by = 90
    price_seg = TASKS_POOL['price_seg']
    zero_id = 350317
    task_id = zero_id + TASKS_POOL['sent']
    print(
        'start_task_id=', task_id,
        'sent before=', TASKS_POOL['sent'],
    )
    # задания
    context = {
        'tasks': []
    }
    for i in range(task_id, task_id + by):
        if i >= TASKS_POOL['count'] + zero_id:
            # выключаем отдавание заданий pip_si_claim_count_req
            TASKS_POOL['finished'] = True
            break
        context['tasks'].append({
            'id': '%s|44503|ind' % i,
            'price_seg': price_seg,
        })

    TASKS_POOL['sent'] += len(context['tasks'])
    print(
        'cur sent=', len(context['tasks']),
        'total_tasks=', TASKS_POOL['count'],
    )
    return render(request, template, context, content_type='application/xhtml+xml')
