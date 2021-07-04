# -*- coding:utf-8 -*-
from django.db.models import Count, Q, Max, Min
from django.conf import settings
from django.core.cache import cache

from apps.main_functions.functions import recursive_fill, sort_voca, object_fields
from apps.main_functions.paginator import myPaginator, navigator
from apps.main_functions.string_parser import q_string_fill

from apps.flatcontent.models import Blocks, Containers
from apps.site.phones.models import Phones

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

def get_phones_for_site(request, link: str = None, **kwargs):
    """Для ображения телефонов на сайте по link
       :param link: ссылка на рубрику (без /phones/ префикса)
    """
    page = Blocks(name='Телефоны 8800')
    search_terms = []
    q_string = kwargs.get('q_string', {})
    q = request.GET.get('q', '').strip()

    q_string_fill(request, q_string)
    catalogue = Containers.objects.filter(tag='phones8800').first()
    if not catalogue:
        catalogue = Containers.objects.create(name='Категории 8800', tag='phones8800', state=1)

    breadcrumbs = [{
        'name': catalogue.name,
        'link': '/phones/',
    }]

    query = Phones.objects.all()

    cond = Q()
    # Выбираем только активные
    cond.add(Q(is_active=True), Q.AND)

    if link:
        link = '/phones/%s' % link
        if not link.endswith('/'):
            link = '%s/' % link
        menu = Blocks.objects.filter(link=link).first()
        if menu:
            cond.add(Q(menu=menu), Q.AND)
            breadcrumbs.append({
                'name': menu.name,
                'link': link,
            })

    query = query.filter(cond)

    if q:
        q_name = 'Вы искали "%s"' % q
        cond_q = Q()
        q_arr = q.split(' ')
        for item in q_arr:

            digit = item.strip().replace('-', '').replace('(', '').replace(')', '')
            if digit.isdigit():
                cond_q.add(Q(phone__contains=digit), Q.AND)
                search_terms.append(digit)
            else:
                cond_q.add(Q(name__icontains=item.strip()), Q.AND)
                search_terms.append(item)
        query = query.filter(cond_q)
        breadcrumbs.append({
            'name': q_name,
        })
        page.name = q_name

    total_records = query.aggregate(Count('id'))['id__count']

    paginator_template = 'web/paginator.html'
    my_paginator, records = myPaginator(total_records, q_string['page'], q_string['by'])
    paginator = navigator(my_paginator, q_string, paginator_template)

    phones = query[records['start']:records['end']]

    # TODO: кэшировать по ссылке
    return {
        'page': page,
        'breadcrumbs': breadcrumbs,
        'q_string': q_string,
        'catalogue': catalogue,
        'paginator': paginator,
        'my_paginator': my_paginator,
        'phones': phones,
        'search_terms': search_terms,
    }

