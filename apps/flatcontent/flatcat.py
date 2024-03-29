# -*- coding:utf-8 -*-
from django.db.models import Count, Q, Max, Min
from django.conf import settings
from django.core.cache import cache

from apps.main_functions.functions import recursive_fill, sort_voca, object_fields
from apps.main_functions.paginator import myPaginator, navigator
from apps.main_functions.string_parser import q_string_fill

from apps.flatcontent.models import (
    Containers,
    Blocks,
    get_ftype,
    prepare_jstree,
    FAT_HIER,
)

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
    from apps.products.strategy import get_search_strategy


def get_costs_types(products):
    """Разные типы цен
       :param products: Товары/услуги
    """
    costs_types = CostsTypes.objects.filter(is_active=1).order_by('position')
    if not costs_types:
        return
    ids_costs_types = {cost_type.id: cost_type for cost_type in costs_types}

    ids_products = [product.id for product in products]
    costs_values = Costs.objects.filter(product__in=ids_products)
    ids_costs_values = {}
    for cost_value in costs_values:
        if not cost_value.cost_type_id in ids_costs_types:
            continue

        cost_type = ids_costs_types[cost_value.cost_type_id]
        product_id = cost_value.product_id

        if not product_id in ids_costs_values:
            ids_costs_values[product_id] = {}
        if not cost_type.id in ids_costs_values[product_id]:
            ids_costs_values[product_id][cost_type.id] = {
                'cost_type': cost_type,
                #'measure': cost_value.get_measure_display(),
                'cost': cost_value.cost,
            }
    for product in products:
        if not product.id in ids_costs_values:
            continue
        product.costs = []
        product.costs_by_tag = {}
        for cost_type in costs_types:
            if not cost_type.id in ids_costs_values[product.id]:
                continue
            cost = ids_costs_values[product.id][cost_type.id]
            product.costs.append(cost)
            if cost_type.tag:
                if not cost_type.tag in product.costs_by_tag:
                    product.costs_by_tag[cost_type.tag] = cost

def get_breadcrumbs_for_product(product, breadcrumbs: list):
    """Хлебные крошки для товара с кэшем
       :param product: экземпляр модели Products
       :param breadcrumbs: массив с хлебными крошками
    """
    cache_time = 600
    cache_var = '%s_product_breadcrumbs_%s' % (
        settings.PROJECT_NAME,
        product.id,
    )
    inCache = cache.get(cache_var)
    if inCache:
        for crumb in inCache.get('breadcrumbs', []):
            breadcrumbs.append(crumb)
        return inCache.get('rubric')

    rubric = None
    # Хлебные крошки по каталогу
    pcat = product.productscats_set.filter(cat__container__state=7).values('cat', 'cat__parents', 'cat__container').first()
    if not pcat:
        return []

    container = Containers.objects.filter(pk=pcat['cat__container']).values('name').first()
    if container:
        breadcrumbs.append({
            'name': container['name'],
            'link': '/cat/',
        })

    cond = Q()
    cond.add(Q(pk=pcat['cat']), Q.OR)
    parents = []
    if pcat['cat__parents']:
        parents_arr = pcat['cat__parents'].split('_')
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
    cat = ids_cats.get(pcat['cat'])
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
    result = {
        'rubric': rubric,
        'breadcrumbs': breadcrumbs,
    }
    cache.set(cache_var, result, cache_time)
    return rubric

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
        rubric = get_breadcrumbs_for_product(product, breadcrumbs)
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
       :param cache_time: время кэширования
       :param force_new: получить каталог без кэша
    """
    cache_var = '%s_%s_pcats' % (
        settings.PROJECT_NAME,
        tag,
    )
    inCache = cache.get(cache_var)
    if inCache and not force_new:
        return inCache
    # получаем список из (ид категории, кол-во товаров)
    # <QuerySet [(53, 42), (54, 7), (55, 7)]>
    pcats = ProductsCats.objects.filter(container__tag=tag, product__is_active=True, cat__is_active=True).values_list('cat').annotate(products_count=Count('product', distinct=True))
    pcats = list(pcats)
    cache.set(cache_var, pcats, cache_time)
    return pcats

def get_catalogue_lvl(request,
                      container_id: int,
                      cat_id: int = None,
                      pass_top_solo: bool = False,
                      cache_time: int = 300,
                      force_new: bool = False):
    """Вытаскиваем jstree категории (подкатегории)
       :param request: HttpRequest
       :param container_id: ид контейнера
       :param cat_id: ид категории
       :param pass_top_solo: пропускать верхний уровень
                             и отдавать следующий, если это одна категория
       :param cache_time: время кэширования
       :param force_new: получить каталог без кэша
    """
    cache_var = '%s_%s_%s_get_catalogue_lvl' % (
        settings.PROJECT_NAME,
        container_id,
        cat_id,
    )
    inCache = cache.get(cache_var)
    if inCache and not force_new:
        return inCache

    result = []
    if not container_id or not container_id.isdigit():
        return []

    query = Blocks.objects.filter(is_active=True,
                                  container=container_id)

    if not cat_id:
        menus = query.filter(parents='')
    else:
        if cat_id.isdigit():
            menus = query.filter(parents__endswith='_%s' % cat_id)
        else:
            menus = query.filter(parents='')

    menus = menus.order_by('position')

    # Если 1 рубрики выводить не надо, ищем ниже
    if pass_top_solo:
        while len(menus) == 1:
            new_parents = '%s_%s' % (menus[0].parents if menus[0].parents else '', menus[0].id)
            menus = query.filter(parents=new_parents).order_by('position')

    prepare_jstree(result, menus, lazy=True, fill_href=True)

    # Узнать есть ли вложенность в каждом из menus
    menus_parents = ['%s_%s' % (menu.parents or '', menu.id) for menu in menus]
    counts = Blocks.objects.filter(parents__in=menus_parents).values('parents').annotate(Count('parents'))

    ids_counts = {int(count['parents'].split('_')[-1]): count['parents__count'] for count in counts}
    for item in result:
        if not item['id'] in ids_counts:
            item['children'] = False

    cache.set(cache_var, result, cache_time)
    return result

def get_catalogue(request,
                  tag: str = None,
                  with_count: bool = False,
                  cache_time: int = 300,
                  force_new: bool = False,
                  fat_hier: int = None):
    """Получить каталог для сайта
       :param request: HttpRequest
       :param tag: тег Containers с каталогом
       :param with_count: вытащить по каждой рубрике кол-во товара
       :param cache_time: кэш
       :param force_new: получить каталог без кэша
       :param fat_hier: сколько рубрик считать жирной иерархией?
    """
    if not tag:
        tag = settings.DEFAULT_CATALOGUE_TAG

    MY_FAT_HIER = FAT_HIER
    if fat_hier:
        MY_FAT_HIER = fat_hier

    pass_cache = False
    cache_var = '%s_%s_%s_catalogue' % (
        settings.PROJECT_NAME,
        tag,
        fat_hier if fat_hier else 0,
    )
    if not force_new:
        if request.GET.get('force_new') or request.GET.get('ignore_cache'):
            force_new = True

    inCache = cache.get(cache_var)
    if inCache and not force_new:
        if with_count:
            inCache['products_count'] = get_catalogue_products_count(tag)
        return inCache

    container = Containers.objects.filter(
        tag = tag,
        state = 7,
        is_active = True,
    ).first()
    menus = []
    count = 0
    if container:
        # Если рубрик дохера, то будет больно, избегаем этого
        query = container.blocks_set.filter(is_active=True)
        count = query.aggregate(Count('id'))['id__count']

        new_parents = ''
        cats = query.filter(parents=new_parents).order_by('position')

        if count > MY_FAT_HIER:
            pass_cache = True
            while len(cats) == 1:
                new_parents = '%s_%s' % (cats[0].parents if cats[0].parents else '', cats[0].id)
                cats = query.filter(parents=new_parents).order_by('position')

        menu_queryset = []
        recursive_fill(cats, menu_queryset, '')
        menus = sort_voca(menu_queryset)
    result = {
        'container': container,
        'menus': menus,
        'fat_hier': count > MY_FAT_HIER,
    }

    if not pass_cache:
        cache.set(cache_var, result, cache_time)
    if with_count:
        result['products_count'] = get_catalogue_products_count(tag)
    return result

def search_products(q: str, search_fields: list = None):
    """Поиск товаров по запросу,
       возвращаем только id
       :param q: поисковая фраза
       :param search_fields: поисковые поля
       :return: ид товаров и поисковые фразы
    """
    if not q:
        return []
    if not search_fields:
        search_fields = ['name', 'altname', 'dj_info', 'code']
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
    tag = settings.DEFAULT_CATALOGUE_TAG
    container = Containers.objects.create(
        name = 'Каталог товаров',
        tag = tag,
        state = 7,
        is_active = True,
    )
    return container

def search_alt_catalogue(link: str, force_new: bool = False):
    """Ищем альтернативные каталоги
       :param link: ссылка на рубрику
       :param force_new: игнорировать кэш
       :return: список тег каталога и флаг, что это корень
    """
    if not link or not link.startswith('/cat/'):
        return None, None
    link_parts = link.split('/')
    # ссылка на корень каталога
    is_root_level = len(link_parts) == 4
    catalogue_tag = link_parts[2]

    cache_time = 300
    cache_var = '%s_%s_search_alt_catalogue' % (
        settings.PROJECT_NAME,
        catalogue_tag,
    )
    inCache = cache.get(cache_var)
    if inCache and not force_new:
        return inCache

    catalogue = Containers.objects.filter(
        tag = catalogue_tag,
        is_active = True,
        state = 7).aggregate(Count('id'))['id__count']
    if not catalogue:
        catalogue_tag, is_root_level = None, None
    cache.set(cache_var, [catalogue_tag, is_root_level], cache_time)
    return catalogue_tag, is_root_level

def filter_products(request, ids_cats: list = None):
    """Получаем фасетные фильтры из запроса,
       находим по ним товары, здесь нам не нужны сами фасеты,
       т/к фильтруем по товарам
       :param request: HttpRequest
       :param ids_cats: список ид категорий по которым собираем фасеты
    """
    strategy = get_search_strategy()
    facet_filters = strategy.get_facet_filters_from_request(request)
    return strategy.get_filters_for_search(facet_filters, ids_cats=ids_cats, without_spies=True)

def pick_root_catalogue(tag: str, state: int, force_new: bool = False):
    """Получение каталога (контейнера)
       :param tag: тег контейнера
       :param state: тип контейнера
       :param force_new: игнорировать кэш
    """
    cache_time = 300
    cache_var = '%s_%s_%s_pick_root_catalogue' % (
        settings.PROJECT_NAME,
        tag,
        state,
    )
    inCache = cache.get(cache_var)
    if inCache and not force_new:
        return inCache

    catalogue = Containers.objects.filter(tag=tag, state=state).first()
    if not catalogue:
        catalogue = create_new_cat()
    cache.set(cache_var, catalogue, cache_time)
    return catalogue

def get_cat_for_site(request,
                     link: str = None,
                     with_props: bool = True,
                     with_filters: bool = True, **kwargs):
    """Для отображения каталога на сайте по link
       :param link: ссылка на рубрику (без /cat/ префикса)
       :param with_props: Вытащить свойства товаров
       :param with_filters: Вытащить свойства для фильтров, например,
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

    # Поиск альтернативных каталогов
    tag = settings.DEFAULT_CATALOGUE_TAG
    catalogue_tag, is_root_level = search_alt_catalogue(link)
    if catalogue_tag:
        tag = catalogue_tag

    if link == '/cat/' or is_root_level:
        is_root_level = True
        # Поиск всегда идет на /cat/
        q = q_string['q'].get('q')
        catalogue = pick_root_catalogue(tag=tag, state=cat_type)

        page.name = catalogue.name
        page.link = link
        if q:
            page.name = 'Вы искали %s' % q
            ids_products, search_terms = search_products(q)
            is_search = True
            query = Products.objects.filter(pk__in=ids_products)
        else:
            query = ProductsCats.objects.filter(container=catalogue, product__is_active=True)
    else:
        page = Blocks.objects.select_related('container').filter(link=link, container__state=cat_type).first()
        if page:
            catalogue = page.container
        query = ProductsCats.objects.filter(cat__container=catalogue, product__is_active=True)

    if not catalogue:
        return {
            'page': page,
            'q_string': q_string,
            'breadcrumbs': breadcrumbs,
            'error': 404,
        }

    if not is_root_level:
        breadcrumbs.append({'name': catalogue.name, 'link': catalogue.cat_link()})
        page_parents = page.parents if page.parents else ''
        cond = Q()
        cond.add(Q(cat=page), Q.OR)
        cond.add(Q(cat__parents='%s_%s' % (page_parents, page.id)), Q.OR)
        cond.add(Q(cat__parents__startswith='%s_%s_' % (page_parents, page.id)), Q.OR)
        # Выбираем только активные
        pk_arr = ProductsCats.objects.filter(cond, cat__is_active=True).values_list('id', flat=True)
        pk_arr = list(pk_arr) # чтобы в subquery не уходило
        query = query.filter(pk__in=pk_arr, product__is_active=True)

    if page.parents:
        ids_parents = [int(parent) for parent in page.parents.split('_') if parent]
        parents = {}
        search_parents = Blocks.objects.filter(pk__in=ids_parents)
        for parent in search_parents:
            parents[parent.id] = parent
        for item in ids_parents:
            parent = parents[item]
            breadcrumbs.append({'name': parent.name, 'link': parent.link})

    prefix = 'product__'
    if is_search:
        prefix = ''

    # ----------
    # Фильтрация
    # ----------
    if with_filters:
        filtered = filter_products(request, ids_cats=[page.id, ])
        filtered_ids = filtered.get('ids_products')
        if filtered_ids:
            query = query.filter(**{'%sid__in' % (prefix, ): filtered_ids})

    breadcrumbs.append({'name': page.name, 'link': page.link})
    total_records = query.aggregate(Count('id'))['id__count']
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
    else:
        # По умолчанию сортировка по позиции
        query = query.order_by('%sposition'% prefix)

    paginator_template = 'web/paginator.html'
    my_paginator, records = myPaginator(total_records, q_string['page'], q_string['by'])
    paginator = navigator(my_paginator, q_string, paginator_template)

    # Фильтры по свойствам
    # Фильтр по цене, но только если не сильно много товаров
    # в противном случае это аяксом надо делать
    cost_filter = None
    if with_filters and total_records < FAT_HIER:
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
    pvalues = PropertiesValues.objects.filter(pk__in=ids_pvalues.keys(), is_active=True).values('id', 'prop', 'str_value', 'digit_value')
    for pvalue in pvalues:
        pvalue_id = pvalue['id']
        ids_pvalues[pvalue_id] = pvalue
    # Достаем свойства
    ids_props = {p['prop']: None for p in ids_pvalues.values()}
    props = Property.objects.filter(pk__in=ids_props.keys(), is_active=True).values('id', 'name', 'code', 'ptype', 'measure')
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
            # По товару фиксируем какие свойства заполняли,
            # чтобы если встретилось свойство уже заполненное, то дополнить его
            filled = {
                'cur_index': 0,
                'prop_id_index': -1, # код свойства: индекс
            }
            # Все свойства товара
            pvalues = ids_products_props[product.id].keys()
            props = [p['prop'] for p in ids_pvalues.values() if p['id'] in pvalues]
            for prop_id in props:
                # Если не заполнено свойство, то значит, оно было выключено (is_active=False)
                if not ids_props[prop_id]:
                    continue

                if prop_id not in filled:
                    product.props.append({
                        'prop': ids_props[prop_id],
                        'values': [{
                            'id': p['id'],
                            'str_value': p['str_value'],
                            'digit_value': p['digit_value'],
                        } for p in ids_pvalues.values()
                            if p['id'] in pvalues and p['prop'] == prop_id]
                    })
                    filled[prop_id] = filled['cur_index']
                    filled['cur_index'] += 1
