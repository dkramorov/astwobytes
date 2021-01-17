# -*- coding:utf-8 -*-
from django import template
from django.conf import settings
from django.core.cache import cache
from django.db.models import Count

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
    cache_var = '%s_dynamic_portfolio' % (settings.DATABASES['default']['NAME'], )
    domains = get_domains()
    domain = get_domain(request, domains)
    if domain:
        cache_var += '_%s' % domain['pk']

    inCache = cache.get(cache_var)
    if inCache and not request.GET.get('force_new'):
        return inCache

    # Вытаскиваем менюшку portfolio
    portfolio_menu = Containers.objects.filter(tag='portfolio', state=1).first()
    if not portfolio_menu:
        return {}
    all_blocks = portfolio_menu.blocks_set.all()

    if domain:
        domains = [domain]
        get_translate(all_blocks, domains)
        translate_rows(all_blocks, domain)

    menu_queryset = []
    recursive_fill(all_blocks, menu_queryset, '')
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
        related_by_link = Blocks.objects.filter(container__state=3, link__in=ids_subblocks.values())
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
        block.images.sort(key=lambda x:x.custom_pos)

    # Перевод описаний вытащенных по ссылкам
    if domain:
        domains = [domain]
        get_translate(descriptions, domains)
        translate_rows(descriptions, domain)

    result = {
        'blocks': blocks,
    }
    cache.set(cache_var, result, cache_time)
    return result
