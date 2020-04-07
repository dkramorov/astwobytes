# -*- coding:utf-8 -*-
from django import template
from django.conf import settings
from django.core.cache import cache

register = template.Library()

@register.simple_tag
def test_tag():
    return "test_tag"

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

@register.inclusion_tag('web/tags/sidebar_cats.html')
def sidebar_cats(request, tag: str = 'catalogue'):
    """Каталог в сайдбаре"""
    result = get_catalogue(
        request,
        tag = tag,
        cache_time = 60,
        force_new = False)
    result['request'] = request
    return result

@register.inclusion_tag('web/tags/random_products.html')
def random_products(request,
                    tag: str = 'random_rpoducts',
                    name: str = 'Популярные товары',
                    size: int = 5,
                    cache_time: int = 120):
    """Случайные товары
       :param request: HttpRequest
       :param tag: тег для сохранения в кэше
       :param name: заголовок в блоке
       :param size: сколько вытащить товаров
       :param cache_time: время кэширования
    """
    cache_var = '%s_random_products_%s_%s' % (
        settings.DATABASES['default']['NAME'],
        tag,
        size,
    )
    inCache = cache.get(cache_var)
    if inCache:
        return inCache

    products = Products.objects.filter(img__isnull=False).order_by('?')[:size]
    result = {
        'name': name,
        'tag': tag,
        'products': list(products),
    }
    cache.set(cache_var, result, cache_time)

    result['request'] = request
    return result