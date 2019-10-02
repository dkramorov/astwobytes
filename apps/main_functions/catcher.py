# -*- coding:utf-8 -*-
import json

from django.conf import settings

from apps.main_functions.string_parser import kill_quotes

def json_pretty_print(json_obj):
    """Вывести json в человеческом виде"""
    return json.dumps(json_obj, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False)

def defiz_phone(phone):
    """Дефизы в телефоне"""
    if not phone:
        return phone

    if type(phone) == int:
        phone = str(phone)
    phone = kill_quotes(phone, 'int')
    phone_len = len(phone)

    if phone_len == 5:
        phone = '%s-%s' % (phone[:3], phone[3:])
    elif phone_len == 6:
        phone = '%s-%s' % (phone[:3], phone[3:])
    elif phone_len == 7:
        phone = '%s-%s-%s' % (phone[:1], phone[1:4], phone[4:])
    elif phone_len == 10:
        if phone.startswith('9'): # сотовые
            phone = '(%s) %s-%s-%s' % (phone[:3], phone[3], phone[4:7], phone[7:])
        else: # городские
            phone = '(%s) %s-%s' % (phone[:4], phone[4:7], phone[7:])
    elif phone_len == 11:
        if phone[1] == '9': # сотовые
            phone = '%s (%s) %s-%s-%s' % (phone[0], phone[1:4], phone[4], phone[5:8], phone[8:])
        else: # городские
            phone = '%s (%s) %s-%s' % (phone[0], phone[1:5], phone[5:8], phone[8:])
    return phone
