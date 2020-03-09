# -*- coding:utf-8 -*-
from django import template
from django.conf import settings
from django.core.cache import cache

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

@register.inclusion_tag('web/catalogue.html')
def catalogue(request):
    """Каталог в виде меню"""
    result = {}
    cache_time = 15
    # cache_var = "catalogue_%s" % settings.DATABASES['default']['NAME']
    #result['menus'] = cache_catalogue(cache_time)
    result['request'] = request
    return result
