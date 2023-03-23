# -*- coding:utf-8 -*-
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.conf import settings

from apps.telegram.telegram import TelegramBot

def send_message(request, *args, **kwargs):
    """Отправка сообщения"""
    result = {'action': 'send_message'}
    method = request.GET
    if request.method == 'POST':
        method = request.POST
    result['method'] = 'GET' if request.method == 'GET' else 'POST'
    token = ''
    chat_id = ''
    msg = ''
    if method.get('token'):
        token = method['token']
        result['token'] = token
    if method.get('chat_id'):
        chat_id = method['chat_id']
        result['chat_id'] = chat_id
    if method.get('msg'):
        msg = method['msg']
        result['msg'] = msg
    if token and chat_id and msg:
        result['result'] = TelegramBot(token=token, chat_id=chat_id).send_message(msg)
    return JsonResponse(result, safe=False)

