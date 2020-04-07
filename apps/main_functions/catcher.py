# -*- coding:utf-8 -*-
import re
import json
import datetime

from django.conf import settings

from apps.main_functions.models import Config
from apps.main_functions.string_parser import kill_quotes, translit

REGA_EMAIL = re.compile('^([a-z0-9\._-]{1,50})@([a-z0-9\._-]{1,50})\.([a-z]{2,4})$', re.I)

def json_pretty_print(json_obj):
    """Вывести json в человеческом виде"""
    return json.dumps(json_obj, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False)

def defiz_phone(phone):
    """Дефизы в телефоне
       :param phone: телефон 83952123321
    """
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

def check_email(email):
    """Проверка емайла на валидность
       :param email: email
    """
    if email:
        if REGA_EMAIL.match(email):
            return email
    return None

def feedback_emails():
    """Поиск emailов, разделенных пробелом
       для обратной связи, заполняется в Config"""
    emails = []
    conf = Config.objects.filter(name='feedback', attr='emails', value__isnull=False).first()
    if conf:
        emails_array = conf.value.replace(',', ' ').split(' ')
        for email in emails_array:
            if not email:
                continue
            if check_email(email):
                emails.append(email)
    else:
        emails.append('dkramorov@mail.ru', )
    return emails

def feedback_form(request, q_string: dict = None,
                  files: list = None, lang: str = 'ru',
                  fields: list = None):
    """Форма обратной связи
       q_string используем для дополнительных полей,
       которые хотим обработать аналогично fv
    """
    if not q_string:
        q_string = {}
    if not files:
        files = []
    if not fields:
        fields = []

    fv = {
        'ifuser': None,
        'phone': None,
        'name': None,
        'email': None,
        'address': None,
        'recall': None,
        'msg': None,
        'file': None,
    }
    # ----
    # POST
    # ----
    if request.method == 'POST':
        for key in fv:
            values = request.POST.getlist(key)
            items = [item.strip() for item in values if item.strip()]
            if len(items) == 1:
                items = items[0]
            fv[key] = items
            q_string[key] = items
        # --------------------------------
        # Заносим все отправленные данные,
        # которые еще не занесены
        # --------------------------------
        for key, value in request.POST.items():
            if not key in fv:
                fv[key] = value

        if request.FILES:
            if request.FILES:
                failo = request.FILES.get('file')
                if failo:
                    name = translit(failo.name)
                    ext = ''
                    if '.' in failo.name:
                        name = failo.name.split('.')[0]
                        ext = '.%s' % failo.name.split('.')[-1]
                    fname = name + ext
                    # ---------------------------------------------------
                    # mail.attach(fname, failo.read(), failo.content_type)
                    # ---------------------------------------------------
                    fv['file'] = {
                        'name': fname,
                        'content': failo.read(),
                        'content_type': failo.content_type,
                    }

    lang_vars = {
        'ru': [
            ('name', 'ФИО'),
            ('email', 'Email'),
            ('phone', 'Телефон'),
            ('address', 'Адрес'),
            ('recall', 'Пользователь хочет, чтобы вы ему перезвонили'),
            ('msg', 'Сообщение пользователя'),
        ],
        'en': [
            ('name', 'User Name'),
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('address', 'Address'),
            ('recall', 'User wait for you call him'),
            ('msg', 'Message'),
        ],
    }

    fv['result'] = '<br>\n'.join(['%s: %s' % (item[1], request.POST.get(item[0]))
        for item in lang_vars[lang] if request.POST.get(item[0])])

    # -------------------
    # Дополнительные поля
    # -------------------
    for field in fields:
        key = request.POST.get(field['name'])
        if key:
            fv['result'] += '%s: %s<br>\n' % (field['value'], request.POST[key])
    # --------------
    # Служебные поля
    # --------------
    sys_fields = (
        ('ip', request.META.get('REMOTE_ADDR')),
        ('referer', request.META.get('HTTP_REFERER')),
        ('browser', request.META.get('HTTP_USER_AGENT')),
    )
    fv_sys = '<br>\n'.join(['%s: %s' % (item[0], item[1])
        for item in sys_fields if item[1]])

    fv['result'] += '<br><br>\n\n%s' % fv_sys

    domain = request.META.get('HTTP_HOST', '')#.decode('idna')
    fv['domain'] = domain
    fv['title'] = '%s Пользователь оставил сообщение %s' % (domain, datetime.datetime.today().strftime('%d-%m-%Y %H:%M'))

    fv['emails'] = feedback_emails()
    fv['sender'] = settings.EMAIL_HOST_USER

    return fv
