# -*- coding:utf-8 -*-
from django import template
from django.conf import settings
from django.core.cache import cache
from django.db.models import Count, Q

from apps.main_functions.functions import recursive_fill, sort_voca
from apps.main_functions.models import Config
from apps.flatcontent.models import Containers, Blocks, LinkContainer

from apps.languages.models import (
    get_domain,
    get_domains,
    get_translate,
    get_content_type,
    translate_rows, )

register = template.Library()

@register.filter(name = 'dynamic_portfolio')
def dynamic_portfolio(request):
    cache_time = 300
    cache_var = '%s_dynamic_portfolio' % (settings.PROJECT_NAME, )
    domains = get_domains()
    domain = get_domain(request, domains)
    if domain:
        cache_var += '_%s' % domain['pk']

    inCache = cache.get(cache_var)
    if inCache and not request.GET.get('force_new'):
        return inCache

    # Вытаскиваем менюшку portfolio
    # Там лежат верхние разделы Identity, Illustration, Toys
    portfolio_menu = Blocks.objects.filter(tag='portfolio', link='/portfolio/', state=4).first()
    if not portfolio_menu:
        return {}

    parents = '%s_%s' % (portfolio_menu.parents, portfolio_menu.id)
    all_blocks = Blocks.objects.filter(state=4, is_active=True).filter(Q(parents=parents)|Q(parents__startswith='%s_' % parents))

    # Тут вытаскиваем все вложенные блоки, кроме All projects /portfolio/
    all_blocks = [block for block in all_blocks if not block.link == '/portfolio/']
    if domain:
        domains = [domain]
        get_translate(all_blocks, domains)
        translate_rows(all_blocks, domain)

    menu_queryset = []
    recursive_fill(all_blocks, menu_queryset, parents)
    blocks = sort_voca(menu_queryset)

    # К каждому блоку надо достать описание по сссылке
    descriptions = []

    # К каждому блоку надо достать кол-во фоток
    # привязанных к подблокам, и из каждого подблока
    # первую фотку надо еще и выводить
    for block in blocks:
        if not hasattr(block, 'sub'):
            continue
        block.count = 0
        block.images = []

        ids_subblocks = {subblock.id: subblock.link for subblock in block.sub}
        # Для описания надо узнать какая стат.страничка
        # ссылается на subblock.link и взять от нее описание
        related_by_link = []
        related_containers = block.linkcontainer_set.select_related('container').all()
        if related_containers:
            related_by_link = related_containers[0].container.blocks_set.filter(link__in=ids_subblocks.values())

        ids_desc = {related.link: related for related in related_by_link}

        # К каждому subblock надо докинуть описалово, чтобы получить его в картинках
        desc_arr = {}
        subblock_sorting = []
        for subblock in block.sub:
            subblock_sorting.append(subblock.id)
            if subblock.link in ids_desc:
                desc_block = ids_desc[subblock.link]
                descriptions.append(desc_block)
                desc_arr[subblock.id] = desc_block
        links = LinkContainer.objects.filter(block__in=ids_subblocks.keys()).values('container', 'block')
        ids_links = {
            link['container']: {
                'block_id': link['block'],
                'position': subblock_sorting.index(link['block']),
            }
            for link in links
        }

        imgas = Blocks.objects.filter(container__in=ids_links.keys(), img__isnull=False).order_by('position')
        block.count += len(links)
        analogs = []
        for imga in imgas:
            if imga.container_id in analogs:
                continue

            if imga.container_id in ids_links:
                block_id = ids_links[imga.container_id]['block_id']
                # Нашли block_id надо взять его описание для этой фотки
                if block_id in desc_arr:
                    imga.custom_block = desc_arr[block_id]
                    imga.custom_pos = ids_links[imga.container_id]['position']

            analogs.append(imga.container_id)
            block.images.append(imga)

        # Правильная сортировка изображений так как они в админке
        block.images.sort(key=lambda x:x.custom_pos if hasattr(x, 'custom_pos') else 0, reverse=True)

    # Перевод описаний вытащенных по ссылкам
    if domain:
        domains = [domain]
        get_translate(descriptions, domains)
        translate_rows(descriptions, domain)

    main_block = Blocks(name='All',
                        title=blocks[0].title,
                        class_name=blocks[0].class_name)
    main_block.images = []
    main_block.count = 0
    max_size = max([len(block.images) for block in blocks])

    for i in range(max_size):
        for block in blocks:
            if len(block.images) > i:
                main_block.images.append(block.images[-(i+1)])
                main_block.count += 1

    blocks.insert(0, main_block)

    result = {
        'blocks': blocks,
    }
    cache.set(cache_var, result, cache_time)
    return result

@register.inclusion_tag('web/tags/portfolio_menu.html')
def portfolio_menu(request):
    """Портфолио менюшка"""
    result = {}
    all_blocks = [] # Для перевода

    cache_time = 60 # 60 секунд
    cache_var = '%s_portfolio_menu' % (settings.PROJECT_NAME, )
    if settings.IS_DOMAINS:
        domain = get_domain(request)
        if domain:
            cache_var += '_%s' % domain['pk']

    inCache = cache.get(cache_var)
    ignore_cache = request.GET.get('ignore_cache') or request.GET.get('force_new')
    if inCache and not ignore_cache:
        result = inCache
    else:

        # Вытаскиваем менюшку portfolio
        portfolio_menu = Blocks.objects.filter(tag='portfolio', link='/portfolio/', state=4).first()

        parents = '%s_%s' % (portfolio_menu.parents, portfolio_menu.id)

        search_blocks = Blocks.objects.filter(state=4, is_active=True).filter(Q(parents=parents)|Q(parents__startswith='%s_' % parents))
        for item in search_blocks:
            all_blocks.append(item)
        menu_queryset = []
        recursive_fill(search_blocks, menu_queryset, parents)
        menus = sort_voca(menu_queryset)

        # --------------------------
        # Переводим блоки/контейнеры
        # --------------------------
        if settings.IS_DOMAINS:
            domains = get_domains()
            domain = get_domain(request, domains)
            if domain:
                domains = [domain]
                get_translate(all_blocks, domains)
                translate_rows(all_blocks, domain)

        result['menus'] = menus
        cache.set(cache_var, result, cache_time)
    result['request'] = request
    return result

@register.filter(name = 'dynamic_portfolio2')
def dynamic_portfolio2(request):
    cache_time = 300
    cache_var = '%s_dynamic_portfolio2' % (settings.PROJECT_NAME, )
    domains = get_domains()
    domain = get_domain(request, domains)
    if domain:
        cache_var += '_%s' % domain['pk']

    inCache = cache.get(cache_var)
    if inCache and not request.GET.get('force_new') and not request.GET.get('ignore_cache'):
        return inCache

    # Вытаскиваем менюшку portfolio
    # Там лежат верхние разделы Identity, Illustration, Toys
    # В каждом из разделов лежит по 1 привязанному контейнеру с нужным контентом
    portfolio_menu = Blocks.objects.filter(tag='portfolio', link='/portfolio/', state=4).first()
    if not portfolio_menu:
        return {}
    parents = '_%s' % portfolio_menu.id
    if portfolio_menu.parents:
        parents = '%s%s' % (portfolio_menu.parents, parents)
    portfolio_menus = Blocks.objects.filter(parents=parents)
    ids_menus = [item.id for item in portfolio_menus]
    linked_containers = LinkContainer.objects.filter(block__in=ids_menus)
    # Запоминаем привязки к portfolio_menus

    containers = [cont.container for cont in linked_containers]
    containers_blocks = Blocks.objects.select_related('container').filter(container__in=containers)

    if domain:
        domains = [domain]
        get_translate(containers_blocks, domains)
        translate_rows(containers_blocks, domain)
        get_translate(containers, domains)
        translate_rows(containers, domain)

    portfolio = {}
    for menu in portfolio_menus:
        portfolio[menu.id] = {
            'menu': menu,
            'containers': {},
        }
        for link in linked_containers:
            if link.block_id == menu.id:
                portfolio[menu.id]['containers'][link.container.id] = {
                  'container': link.container,
                  'blocks': [],
                }
                cur_blocks = []
                for block in containers_blocks:
                    if block.container_id == link.container.id:
                        #portfolio[menu.id]['containers'][link.container.id]['blocks'].append(block)
                        cur_blocks.append(block)
                menu_queryset = []
                recursive_fill(cur_blocks, menu_queryset, '')
                portfolio[menu.id]['containers'][link.container.id]['blocks'] = sort_voca(menu_queryset)
    result = []
    sorted_keys = []
    for data in sorted(portfolio.values(), key=lambda x:x['menu'].position):
        containers = []
        for cont_key, cont_value in data['containers'].items():
            containers.append(cont_value)
        if not containers:
            continue
        data['containers'] = containers
        result.append(data)

    cache.set(cache_var, result, cache_time)
    return result
