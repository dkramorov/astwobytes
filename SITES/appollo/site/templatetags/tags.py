# -*- coding:utf-8 -*-
from django import template
from django.conf import settings
from django.core.cache import cache
from django.db.models import Count

from apps.main_functions.functions import recursive_fill, sort_voca
from apps.main_functions.models import Config
from apps.flatcontent.models import Containers, Blocks
from apps.personal.models import get_personal_user as get_shopper

from apps.site.phones.models import Phones

register = template.Library()

@register.filter(name = 'check_user_can_call')
def check_user_can_call(request):
    """Проверить, что есть регистрация и телефон подтвержден
    """
    result = {}
    shopper = get_shopper(request)
    if not shopper:
        result['not_registered'] = True
    elif not shopper.phone_confirmed:
        result['not_confirmed'] = True
    if not 'error' in result:
        result['success'] = True
    return result

@register.inclusion_tag('web/tags/sidebar_phones_catalogue.html')
def sidebar_phones_catalogue(request, tag: str = None):
    """Каталог телефонов в сайдбаре"""
    result = {}
    container = Containers.objects.filter(tag='phones8800').first()
    result['container'] = container
    result['blocks'] = container.blocks_set.all().order_by('position')
    result['request'] = request
    return result
