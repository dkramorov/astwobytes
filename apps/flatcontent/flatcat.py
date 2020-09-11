# -*- coding:utf-8 -*-
from django.db.models import Count, Q, Max, Min
from django.conf import settings
from django.core.cache import cache

from apps.main_functions.functions import recursive_fill, sort_voca
from apps.main_functions.paginator import myPaginator, navigator
from apps.main_functions.string_parser import q_string_fill
from .models import Containers, Blocks, get_ftype

is_products = False
if 'apps.products' in settings.INSTALLED_APPS:
    is_products = True
    from apps.products.models import (Products,
                                      ProductsCats,
                                      ProductsPhotos,
                                      Property,
                                      PropertiesValues,
                                      ProductsProperties,
                                      CostsTypes,
                                      Costs, )

def get_costs_types(products):
    """Разные типы цен
       :param products: Товары/услуги
    """
    costs_types = CostsTypes.objects.filter(is_active=1)
    if not costs_types:
        return
    ids_costs_types = {}
    for cost_type in costs_types:
        ids_costs_types[cost_type.id] = cost_type

    ids_products = {product.id: product for product in products}
    costs_values = Costs.objects.filter(product__in=[product.id for product in products]).order_by('cost_type__position')

    for cost_value in costs_values:
        cost_type = ids_costs_types.get(cost_value.cost_type_id)

        if not cost_type:
            continue
        if not cost_type.is_active:
            continue

        if not hasattr(ids_products[cost_value.product_id], 'costs'):
            ids_products[cost_value.product_id].costs = []

        cost = {
            'cost_type': cost_type,
            'measure': cost_value.get_measure_display(),
            'cost': cost_value.cost,
        }

        if cost_type.tag:
            if not hasattr(ids_products[cost_value.product_id], 'costs_by_tag'):
                ids_products[cost_value.product_id].costs_by_tag = {}
            ids_products[cost_value.product_id].costs_by_tag[cost_type.tag] = cost
        ids_products[cost_value.product_id].costs.append(cost)

def get_product_for_site(request, price_id: int):
    """Получить товар/услугу для сайта"""
    page = None
    photos = None
    rubric = None
    breadcrumbs = []
    product = Products.objects.filter(pk=price_id).first()
    if product:
        page = Blocks(name=product.name)
        photos = product.productsphotos_set.all()
        # ---------------------------
        # достаем рубрики товара
        # рассчитываем хлебные крошки
        # ---------------------------
        pcat = product.productscats_set.all().values_list('cat', 'cat__parents').first()
        if pcat:
            cond = Q()
            cond.add(Q(pk=pcat[0]), Q.OR)
            parents = []
            if pcat[1]:
                parents_arr = pcat[1].split('_')
                for parent in parents_arr:
                    if not parent:
                        continue
                    cond.add(Q(pk=parent), Q.OR)
                    parents.append(int(parent))

            cats = Blocks.objects.filter(cond)
            ids_cats = {cat.id: cat for cat in cats}
            for parent in parents:
                if not parent in ids_cats:
                    continue
                cat = ids_cats[parent]
                breadcrumbs.append({
                    'name': cat.name,
                    'link': cat.link,
                })
            cat = ids_cats.get(pcat[0])
            if cat:
                rubric = cat
                breadcrumbs.append({
                    'name': cat.name,
                    'link': cat.link,
                })
        breadcrumbs.append({
            'name': product.name,
            'link': product.link(),
        })
    get_props_for_products([product])
    get_costs_types([product])
    result = {
        'breadcrumbs': breadcrumbs,
        'cat': rubric,
        'photos': photos,
        'page': page,
        'product': product,
    }
    return result

def get_catalogue_products_count(tag: str,
                                 cache_time: int = 300,
                                 force_new: bool = False):
    """Получение кол-ва товара по каждой из рубрик контейнера
       :param tag: тег контейнера с рубриками
       :param cache_time: кэш
       :param force_new: получить каталог без кэша
    """
    cache_var = '%s_%s_pcats' % (
        settings.DATABASES['default']['NAME'],
        tag,
    )
    inCache = cache.get(cache_var)
    if inCache and not force_new:
        return inCache

    # получаем список из (ид категории, кол-во товаров)
    # <QuerySet [(53, 42), (54, 7), (55, 7)]>
    pcats = ProductsCats.objects.filter(container__tag=tag).values_list('cat').annotate(products_count=Count('product', distinct=True))
    pcats = list(pcats)
    cache.set(cache_var, pcats, cache_time)
    return pcats

def get_catalogue(request,
                  tag: str = 'catalogue',
                  with_count: bool = False,
                  cache_time: int = 300,
                  force_new: bool = False):
    """Получить каталог для сайта
       :param request: HttpRequest
       :param tag: тег Containers с каталогом
       :param with_count: вытащить по каждой рубрике кол-во товара
       :param cache_time: кэш
       :param force_new: получить каталог без кэша
    """
    cache_var = '%s_%s_catalogue' % (
        settings.DATABASES['default']['NAME'],
        tag,
    )
    inCache = cache.get(cache_var)
    if inCache and not force_new:
        if with_count:
            inCache['products_count'] = get_catalogue_products_count(tag)
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
    if with_count:
        result['products_count'] = get_catalogue_products_count(tag)
    return result

def search_products(q: str):
    """Поиск товаров по запросу,
       возвращаем только id
       :param q: поисковая фраза
       :return: ид товаров и поисковые фразы
    """
    if not q:
        return []
    search_fields = ('name', 'altname', 'dj_info', 'code')
    cond = Q()
    q_arr = q.strip().split(' ')
    search_terms = []
    for item in q_arr:
        if not item:
            continue
        search_terms.append(item)
        search_cond = Q()
        for field in search_fields:
            scond = {'%s__icontains' % field: item}
            search_cond.add(Q(**scond), Q.OR)
        cond.add(Q(search_cond), Q.AND)
    return (Products.objects.filter(cond).filter(is_active=True).values_list('id', flat=True), search_terms)

def create_new_cat():
    """Создать контейнер каталога"""
    tag = 'catalogue'
    container = Containers.objects.create(
        name = 'Каталог товаров',
        tag = tag,
        state = 7,
        is_active = True,
    )
    return container

def get_cat_for_site(request, link: str = None,
                     with_props: bool = True,
                     with_filters: bool = True, **kwargs):
    """Для ображения каталога на сайте по link
       :param link: ссылка на рубрику (без /cat/ префикса)
       :param with_props: Вытащить свойства товаров
       :param with_filters: Вытащить свойства для фильтров,
                            максимальная и минимальная цена
    """
    cat_type = get_ftype('flatcat', False)
    page = Blocks(name='Каталог')
    containers = {}
    catalogue = None
    breadcrumbs = []
    q_string = kwargs.get('q_string', {})
    is_search = False
    search_terms = []

    if not link:
        link = '/cat/'
    else:
        link = '/cat/%s' % link
        if not link.endswith('/'):
            link = '%s/' % link

    q_string_fill(request, q_string)

    if link == '/cat/':
        # Поиск всегда идет на /cat/
        q = q_string['q'].get('q')
        catalogue = Containers.objects.filter(tag='catalogue', state=cat_type).first()
        if not catalogue:
            catalogue = create_new_cat()
        if q:
            page.name = 'Вы искали %s' % q
            ids_products, search_terms = search_products(q)
            is_search = True
            query = Products.objects.filter(pk__in=ids_products)
        else:
            query = ProductsCats.objects.filter(product__isnull=False, container=catalogue)
    else:
        page = Blocks.objects.select_related('container').filter(link=link, container__state=cat_type).first()
        if page:
            catalogue = page.container
        query = ProductsCats.objects.filter(cat__container=catalogue, product__is_active=True)

    if catalogue:
        breadcrumbs.append({'name': catalogue.name, 'link': '/cat/'})
        if page.link:
            if page.parents:
                cond = Q()
                cond.add(Q(cat=page), Q.OR)
                cond.add(Q(cat__parents='%s_%s' % (page.parents, page.id)), Q.OR)
                cond.add(Q(cat__parents__startswith='%s_%s_' % (page.parents, page.id)), Q.OR)
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
                cond.add(Q(cat__parents__startswith='%s_%s_' % (page.parents, page.id)), Q.OR)
                query = query.filter(cond)

            breadcrumbs.append({'name': page.name, 'link': page.link})

    total_records = query.aggregate(Count('id'))['id__count']

    prefix = 'product__'
    if is_search:
        prefix = ''

    # Сортировка
    sort = request.GET.get('sort')
    if sort == 'price':
        query = query.order_by('%smin_price' % prefix)
        q_string['q']['sort'] = 'price'
        q_string['sort_name_filter'] = 'Цена по возрастанию'
    elif sort == '-price':
        query = query.order_by('-%smax_price' % prefix)
        q_string['q']['sort'] = '-price'
        q_string['sort_name_filter'] = 'Цена по убыванию'

    paginator_template = 'web/paginator.html'
    my_paginator, records = myPaginator(total_records, q_string['page'], q_string['by'])
    paginator = navigator(my_paginator, q_string, paginator_template)

    # Фильтры по свойствам
    # Фильтр по цене
    cost_filter = None
    if with_filters:
        costs = query.aggregate(Max('%sprice' % prefix), Min('%sprice' % prefix))
        cost_filter = {
            'min': costs['%sprice__min' % prefix],
            'max': costs['%sprice__max' % prefix],
        }

    if is_search:
        products = query[records['start']:records['end']]
        breadcrumbs.append({'name': 'Вы искали %s' % q, 'link': '%s?q=%s' % (page.link, q)})
    else:
        query = query.select_related('product')
        cat_products = query[records['start']:records['end']]
        products = [product.product for product in cat_products]
    if with_props:
        get_props_for_products(products)
    get_costs_types(products)
    # TODO: кэшировать по ссылке
    return {
        'page': page,
        'q_string': q_string,
        'breadcrumbs': breadcrumbs,
        'catalogue': catalogue,
        'paginator': paginator,
        'my_paginator': my_paginator,
        'products': products,
        'cost_filter': cost_filter,
        'search_terms': search_terms,
    }

def get_props_for_products(products: list, only_props: list = None):
    """Получение свойств к товарам
       :param products: список товаров
       :param only_props: список кодов свойств, которые будем доставать
    """
    # Находим привязки свойств к товарам
    ids_products = [product.id for product in products]
    products_props = ProductsProperties.objects.filter(product__in=ids_products).values('product', 'prop')
    if not products_props:
        return
    # Строим словарь по товарам
    # {ид_товара: {ид_значения_свойства:None}}
    # Запоминаем все ид_значения_свойства,
    # чтобы вытащить их и дописать в словарь
    ids_pvalues = {}
    ids_products_props = {}
    for product_prop in products_props:
        product_id = product_prop['product']
        pvalue_id = product_prop['prop']
        if not product_id in ids_products_props:
            ids_products_props[product_id] = {}
        if not pvalue_id in ids_products_props[product_id]:
            ids_products_props[product_id][pvalue_id] = None
            ids_pvalues[pvalue_id] = None
    # Достаем значения свойств
    pvalues = PropertiesValues.objects.filter(pk__in=ids_pvalues.keys()).values('id', 'prop', 'str_value', 'digit_value')
    for pvalue in pvalues:
        pvalue_id = pvalue['id']
        ids_pvalues[pvalue_id] = pvalue
    # Достаем свойства
    ids_props = {p['prop']: None for p in ids_pvalues.values()}
    props = Property.objects.filter(pk__in=ids_props.keys()).values('id', 'name', 'code', 'ptype', 'measure')
    for prop in props:
        ids_props[prop['id']] = prop
        # Доливаем свойство к значению свойства
        for pvalue_id, pvalue in ids_pvalues.items():
            prop_id = pvalue['prop']
            if prop_id in ids_props:
                pvalue['property'] = ids_props[prop_id]
    # Дополняем товары найдеными свойствами
    for product in products:
        product.props = []
        if product.id in ids_products_props:

            # Все свойства товара
            pvalues = ids_products_props[product.id].keys()
            props = [p['prop'] for p in ids_pvalues.values() if p['id'] in pvalues]
            for prop_id in props:
                product.props.append({
                    'prop': ids_props[prop_id],
                    'values': [{
                        'id': p['id'],
                        'str_value': p['str_value'],
                        'digit_value': p['digit_value'],
                    } for p in ids_pvalues.values()
                        if p['id'] in pvalues and p['prop'] == prop_id]
                })


