# -*- coding:utf-8 -*-
from django import template
from django.conf import settings
from django.core.cache import cache

from apps.flatcontent.views import get_catalogue

register = template.Library()

@register.inclusion_tag('web/ajax_cart.html')
def ajax_cart(request):
    """Аякс-корзинка"""
    result = {}
    if request.session.get("shopper"):
      shopper = request.session['shopper']
      #result['cart'] = CalcCart(shopper, 1)
    result['request'] = request
    return result

@register.inclusion_tag('web/tags/catalogue.html')
def catalogue(request):
    """Каталог в виде меню - левый блок"""
    result = get_catalogue(
        request,
        tag = 'catalogue',
        cache_time = 60,
        force_new = False)
    result['request'] = request
    return result

@register.inclusion_tag('web/tags/best_cats.html')
def best_cats(request):
    """Каталог в виде слайдера - центральный блок"""
    result = get_catalogue(
        request,
        tag = 'best_cats',
        cache_time = 60,
        force_new = False)
    result['request'] = request
    return result

