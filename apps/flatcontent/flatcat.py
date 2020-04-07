# -*- coding:utf-8 -*-
from django.db.models import Count, Q
from django.conf import settings
from django.core.cache import cache

from apps.main_functions.functions import recursive_fill, sort_voca
from apps.main_functions.paginator import myPaginator, navigator
from apps.main_functions.string_parser import q_string_fill
from .models import Containers, Blocks, get_ftype

is_products = False
if 'apps.products' in settings.INSTALLED_APPS:
    is_products = True
    from apps.products.models import Products, ProductsCats

def get_product_for_site(request, price_id: int):
    """Получить товар/услугу для сайта"""
    page = None
    photos = None
    cat = None
    breadcrumbs = []
    product = Products.objects.filter(pk=price_id).first()
    if product:
        page = Blocks(name=product.name)
        photos = product.productsphotos_set.all()
        cat = ProductsCats.objects.select_related('cat').filter(product=product).first()
        if cat and cat.cat.parents:
            ids_parents = [int(parent) for parent in cat.cat.parents.split('_') if parent]
            cats = Blocks.objects.filter(pk__in=ids_parents)
            ids_cats = {cat.id: cat for cat in cats}
            for item in ids_parents:
                parent = ids_cats[item]
                breadcrumbs.append({'name': parent.name, 'link': parent.link})
        breadcrumbs.append({'name': product.name, 'link': '/product/%s/' % product.id})
    result = {
        'breadcrumbs': breadcrumbs,
        'cat': cat,
        'photos': photos,
        'page': page,
        'product': product,
    }
    return result

def get_catalogue(request, tag: str = 'catalogue',
                  cache_time: int = 300, force_new: bool = False):
    """Получить каталог для сайта"""
    cache_var = '%s_%s_catalogue' % (
        settings.DATABASES['default']['NAME'],
        tag,
    )
    inCache = cache.get(cache_var)
    if inCache and not force_new:
        return inCache
    container = Containers.objects.filter(
        tag = tag,
        state = 7,
        is_active = True
    ).first()
    menus = []
    if container:
        cats = container.blocks_set.filter(is_active=True)
        menu_queryset = []
        recursive_fill(cats, menu_queryset, '')
        menus = sort_voca(menu_queryset)
    result = {
        'container': container,
        'menus': menus,
    }
    cache.set(cache_var, result, cache_time)
    return result

def get_cat_for_site(request, link: str = None, **kwargs):
    """Для тображения каталога на сайте по link
       :param link: ссылка на рубрику (без /cat/ префикса)
    """
    cat_type = get_ftype('flatcat', False)
    page = Blocks(name='Каталог')
    containers = {}
    catalogue = None
    breadcrumbs = []
    q_string = {}

    if not link:
        link = '/cat/'
    else:
        link = '/cat/%s' % link
        if not link.endswith('/'):
            link = '%s/' % link

    if link == '/cat/':
        catalogue = Containers.objects.filter(tag='catalogue', state=cat_type).first()
        query = ProductsCats.objects.filter(product__isnull=False)
    else:
        page = Blocks.objects.select_related('container').filter(link=link, container__state=cat_type).first()
        if page:
            catalogue = page.container
        query = ProductsCats.objects.filter(cat__container=catalogue)
    if catalogue:
        breadcrumbs.append({'name': catalogue.name, 'link': '/cat/'})
        if page.link:
            if page.parents:
                cond = Q()
                cond.add(Q(cat=page), Q.OR)
                cond.add(Q(cat__parents='%s_%s' % (page.parents, page.id)), Q.OR)
                cond.add(Q(cat__parents__startswith='%s_%s_' % (page.parents.page.id)), Q.OR)
                query = query.filter(cond)

                ids_parents = [int(parent) for parent in page.parents.split('_') if parent]
                parents = {}
                search_parents = Blocks.objects.filter(pk__in=ids_parents)
                for parent in search_parents:
                    parents[parent.id] = parent
                for item in ids_parents:
                    parent = parents[item]
                    breadcrumbs.append({'name': parent.name, 'link': parent.link})
            else:
                cond = Q()
                cond.add(Q(cat=page), Q.OR)
                cond.add(Q(cat__parents='_%s' % page.id), Q.OR)
                query = query.filter(cond)

            breadcrumbs.append({'name': page.name, 'link': page.link})

    total_records = query.aggregate(Count('id'))['id__count']
    q_string_fill(request, q_string)
    paginator_template = 'web/paginator.html'
    my_paginator, records = myPaginator(total_records, q_string['page'], q_string['by'])
    paginator = navigator(my_paginator, q_string, paginator_template)

    products = query.select_related('product')[records['start']: records['end']]
    return {
        'page': page,
        'q_string': q_string,
        'breadcrumbs': breadcrumbs,
        'catalogue': catalogue,
        'paginator': paginator,
        'my_paginator': my_paginator,
        'products': [product.product for product in products],
    }
