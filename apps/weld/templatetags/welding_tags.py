# -*- coding:utf-8 -*-
from django import template
from django.conf import settings
from django.core.cache import cache
from django.utils.safestring import mark_safe

register = template.Library()

#@register.simple_tag
@register.filter(name='surname_and_initials')
def surname_and_initials(name: str):
    """Фамилия и инициалы
       :param name: полное имя
    """
    result = []
    if not name:
        return ''
    name_parts = name.split(' ')
    for i, name_part in enumerate(name_parts):
        if i == 0:
            result.append(name_part)
            continue
        try:
            result.append('%s.' % name_part[0].upper())
        except Exception:
            pass
    return ' '.join(result)
