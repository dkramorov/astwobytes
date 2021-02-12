# -*- coding:utf-8 -*-
from django import template
from django.conf import settings
from django.core.cache import cache

from apps.flatcontent.flatcat import get_catalogue, search_alt_catalogue
from apps.products.models import Products, ProductsCats
from apps.shop.cart import calc_cart, get_shopper

register = template.Library()

@register.simple_tag
def test_tag():
    return "test_tag"

@register.inclusion_tag('web/order/ajax_cart.html')
def ajax_cart(request):
    """Аякс-корзинка"""
    result = {}
    shopper = get_shopper(request)
    result['cart'] = calc_cart(shopper, min_info=False)
    result['request'] = request
    return result

@register.inclusion_tag('web/tags/catalogue_home.html')
def catalogue_home(request):
    """Каталог в виде меню на главной страничке
       левый блок
    """
    result = get_catalogue(
        request,
        tag = settings.DEFAULT_CATALOGUE_TAG,
        cache_time = 60,
        force_new = False)
    result['request'] = request
    return result

@register.inclusion_tag('web/tags/catalogue.html')
def catalogue(request, with_count: bool = False):
    """Каталог в виде меню - левый блок"""
    result = get_catalogue(
        request,
        tag = settings.DEFAULT_CATALOGUE_TAG,
        cache_time = 60,
        force_new = False,
        with_count = with_count)
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
def sidebar_cats(request, tag: str = None):
    """Каталог в сайдбаре"""
    if not tag:
        tag = settings.DEFAULT_CATALOGUE_TAG
        # Ищем альтернативные каталоги
        link = request.META.get('PATH_INFO')
        catalogue_tag, is_root_level = search_alt_catalogue(link)
        if catalogue_tag:
            tag = catalogue_tag
    result = get_catalogue(
        request,
        tag = tag,
        cache_time = 60,
        force_new = True if request.GET.get('force_new') else False, )
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
        settings.PROJECT_NAME,
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

@register.inclusion_tag('web/containers/products_sidebar_slider.html')
def products_sidebar_slider(product, limit: int = 12):
    """Вывод на страничке товара других товаров из той же рубрики
       :param product: товар
       :param limit: количество аналогов
    """
    cat_id = ProductsCats.objects.filter(product=product).values_list('cat', flat=True)
    products = ProductsCats.objects.select_related('product').filter(cat__in=cat_id).exclude(product=product)[:limit]
    result = {
        'container': {'name': 'Похожие товары'},
        'products': [product.product for product in products],
    }
    return result
