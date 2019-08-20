# -*- coding:utf-8 -*-
from django.conf import settings
from django.db.models import Q

def tabulator_filters_and_sorters(request):
    """Приводим фильтры и сортировку из request к нужному виду"""
    result = {'filters': [], 'sorters': [], 'params': {}}
    rvars = None

    if request.method == "GET":
        rvars = request.GET
    elif request.method == "POST":
        rvars = request.POST
    if not rvars:
        return result

    rfilters = [rfilter for rfilter in rvars if (rfilter.startswith('filters[') and '[field]' in rfilter)]
    rsorters = [rsorter for rsorter in rvars if (rsorter.startswith('sorters[') and '[field]' in rsorter)]
    for rfilter in rfilters:
        key = rvars[rfilter]
        value = rvars[rfilter.replace('[field]', '[value]')]
        sort_type = rvars[rfilter.replace('[field]', '[type]')]
        result['params'][key] = value
        # -------------------
        # Поправка на boolean
        # -------------------
        if value in ('true', 'false'):
            if value == 'true':
                value = True
            else:
                value = False
        item = {key: value}
        if sort_type == 'like':
            item = {'%s__icontains' % (key, ): value}
        # ------------------
        # С использованием Q
        # ------------------
        #search_type = rvars[rfilter.replace('[field]', '[type]')]
        #if search_type == 'like':
        #    item = {'%s__icontains' % (key, ): value}
        #result['filters'].append(Q(**item))
        # -----------------------
        # Без использования Q т/к
        # надо проверить тип поля
        # -----------------------
        result['filters'].append(item)

    for rsorter in rsorters:
        key = rvars[rsorter]
        value = rvars[rsorter.replace('[field]', '[dir]')]
        if not value in ('asc', 'desc'):
            continue
        item = key
        if value == 'desc':
            item = '-%s' % (key, )
        result['sorters'].append(item)
    return result






