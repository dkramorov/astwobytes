# -*- coding:utf-8 -*-
from django.conf import settings
from django.db.models import Q

from apps.main_functions.date_time import str_to_date

def tabulator_filters_and_sorters(request, custom_position_field: str = None):
    """Приводим фильтры и сортировку из request к нужному виду
       custom_position_field для своего поля сортировки, например,
       user => customuser OneToOneRelation и тогда
       custom_position_field = customuser__position

       Как переопределить сортировку по умолчанию:
       filters_and_sorters = tabulator_filters_and_sorters(request)
       if not filters_and_sorters['sorters']:
           filters_and_sorters['params']['sorters']['id'] = 'desc'
    """
    result = {'filters': [], 'sorters': [], 'params': {'filters': {}, 'sorters': {}}}
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
        key = rvars[rfilter].replace('.', '__')
        # ----------------------------
        # Переопределяем поле position
        # ----------------------------
        if key == 'position' and custom_position_field:
            key = custom_position_field
        value = rvars[rfilter.replace('[field]', '[value]')]
        sort_type = rvars[rfilter.replace('[field]', '[type]')]
        result['params']['filters'][key] = value
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
        elif sort_type == 'regex':
            # Предположительно даты,
            # берется начальная дата и ищем до следующей (gte=>lt)
            multiple_dates_separator = ' - '
            if multiple_dates_separator in value:
                dates = value.split(multiple_dates_separator)
                date1 = str_to_date(dates[0])
                date2 = str_to_date(dates[1])
                if date1 and date2:
                    result['filters'].append(Q(**{'%s__gte' % key: date1}))
                    result['filters'].append(Q(**{'%s__lt' % key: date2}))
                    continue
            else:
                date = str_to_date(value)
                if date:
                    item = date
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
        key = rvars[rsorter].replace('.', '__')
        # ----------------------------
        # Переопределяем поле position
        # ----------------------------
        if key == 'position' and custom_position_field:
            key = custom_position_field
        value = rvars[rsorter.replace('[field]', '[dir]')]
        if not value in ('asc', 'desc'):
            continue
        item = key
        if value == 'desc':
            item = '-%s' % (key, )
        result['sorters'].append(item)
        result['params']['sorters'][key] = value

    return result
