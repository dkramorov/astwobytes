# -*- coding:utf-8 -*-
from django.template import loader, Context

from apps.main_functions.string_parser import analyze_digit

def myPaginator(ids, page, by):
    """Разбивание постранично с помощью массива id
       ids - массив айдишников, либо количество записей - проверкой решаем
       page - текущая страничка
       by - количество записей на страницу"""
    paginator = {}
    records = {}
    # -------------------------------
    # Ошибка в постраничной навигации
    # Нужна по сути только для ajax
    # подгрузке следующей странички,
    # чтобы не долбить запросами,
    # когда нечего больше выводить
    # -------------------------------
    paginator_error = None
    # ----------------------------------------------
    # Определяем тип, который передали для пагинации
    # а соответственно вычисляем количество записей
    # ----------------------------------------------
    if type(ids) == list:
        total_records = len(ids)
    elif type(ids) == int or type(ids) == long:
        total_records = ids
    else:
        a = type(ids)
        assert False
    paginator['by'] = by
    paginator['total_records'] = total_records
    # -------------------------------
    # На одну страничку все не влезло
    # вычисляем на сколько влезет
    # -------------------------------
    if total_records > by:
        if by < 1:
            by = 1
            # -------------------------------
            # Ошибка в постраничной навигации
            # -------------------------------
            paginator_error = 1
        pages = divmod(total_records, by)
        if pages[1] > 0: # Остаток больше нуля (+ 1 страницу)
            pages = pages[0] + 1
        else:
            pages = pages[0] # Поделилось нацело - записи влазят на страницы

        next_page = page + 1
        prev_page = page - 1

        if page > pages:
            page = pages
            next_page = page
            prev_page = page - 1
            # -------------------------------
            # Ошибка в постраничной навигации
            # -------------------------------
            paginator_error = 1

        if page < 1:
            page = 1
            # -------------------------------
            # Ошибка в постраничной навигации
            # -------------------------------
            paginator_error = 1

        if next_page > pages:
            next_page = pages
        if prev_page < 1:
            prev_page = 1

        paginator = {'cur_page': page, 'by': by,
                     'next_page': next_page,
                     'prev_page': prev_page,
                     'total_pages': pages,
                     'total_records': total_records,
                     'error': paginator_error}
    else:
        page = 1
        paginator['cur_page'] = 1
        paginator['onepage'] = 1
        paginator['total_pages'] = 1
        # -----------------------------------------
        # Всегда даем ошибку если всего 1 страничка
        # -----------------------------------------
        paginator['error'] = 1

    start_record = (page-1)*by # С какой записи начинаем вывод
    end_record = start_record+by # Какой записью заканчиваем вывод
    # --------------------------------------
    # Если мы должны вывести больше чем есть
    # --------------------------------------
    if end_record > total_records:
        end_record = total_records # Выводим сколько есть
    records = {'start': start_record, 'end': end_record}
    paginator['ends'] = analyze_digit(paginator['total_records'],
                                      end=('запись', 'записей', 'записи'))
    return paginator, records

def navigator(paginator,
              q_string: dict,
              template:str = None,
              select: list = None):
    """HTML пагинатор с использованием шаблона
       :param paginator: результат работы myPaginator
       :param q_string: параметры для пагинации
       :param template: шаблон, например, web/html_paginator.html
    """
    if paginator['total_records'] == 0:
        return ''

    if not select:
        select = (5, 10, 20, 50, 100)
    if not template:
        template = 'admin_paginator.html'

    # q_string['q'] - содержит все условия для перехода по страницам
    halfa = 3
    html = ''
    page_request = ''
    ostatok1 = 0
    ostatok2 = 0

    t = loader.get_template(template)

    if 'q' in q_string:
        for key, value in q_string['q'].items():
            if isinstance(value, list):
                for item in value:
                    page_request += '%s=%s&' % (key, item)
            else:
                page_request += '%s=%s&' % (key, value)
        if page_request:
            page_request = page_request[:-1]

    if 'onepage' in paginator:
        c = {
            'q_string': q_string,
            'paginator': paginator,
            'page_request':page_request,
            'ends': paginator['ends'],
            'select': select,
        }
        return t.render(c)

    start_page, end_page = 0, paginator['total_pages']
    last = end_page
    if paginator['total_pages'] > halfa * 2:
        start_page = paginator['cur_page'] - halfa
        if start_page < 0:
            ostatok1 = -start_page
            start_page = 0

        end_page = paginator['cur_page'] + halfa
        if end_page > paginator['total_pages']:
            ostatok2 = end_page - paginator['total_pages']
            end_page = paginator['total_pages']

        # Фикс на количество страниц
        if ostatok1:
            end_page = end_page + ostatok1
        if ostatok2:
            start_page = start_page - ostatok2
        last = paginator['total_pages']
    pages = []
    for i in range(start_page, end_page):
        page = {'i':i}
        # ----------------
        # Первая страничка
        # ----------------
        if i == start_page:
            if paginator['cur_page'] == 1:
                page['content'] = 1
                page['active'] = 1
                pages.append(page)
            else:
                href = '%s' % q_string['link']
                if page_request:
                    href += '?%s' % page_request
                    href += 'page=1&by=%s' % q_string['by']
                else:
                    href += '?page=1&by=%s' % q_string['by']

                page['link'] = href
                page['content'] = 1
                pages.append(page)
                if paginator['cur_page'] - halfa >= 1:
                    # ---------------------------
                    # Чтобы троеточие не ставить
                    # между двумя последовательно
                    # идущими страничками
                    # ---------------------------
                    if not start_page == 0:
                        pages.append({'i': i, 'ellipsis': 1})
            continue
        # -------------------
        # Последняя страничка
        # -------------------
        if (i+1) == end_page:
            if paginator['cur_page'] == end_page:
                page['content'] = paginator['total_pages']
                page['active'] = 1
                pages.append(page)
            else:
                if paginator['total_pages'] >= paginator['cur_page'] + halfa:
                    # ---------------------------
                    # Чтобы троеточие не ставить
                    # между двумя последовательно
                    # идущими страничками
                    # ---------------------------
                    if not paginator['total_pages'] == pages[-1]['content'] + 1:
                      pages.append({'i': i, 'ellipsis': 1})
                page['link'] = '%s?%spage=%s&by=%s' % (q_string['link'], page_request, last, q_string['by'])
                page['content'] = paginator['total_pages']
                pages.append(page)
            continue
        # -------------------
        # Средняя страничка
        # -------------------
        if (i+1) == paginator['cur_page']:
            page['content'] = i + 1
            page['active'] = 1
            pages.append(page)
        else:
            page['link'] = '%s?%spage=%s&by=%s' % (q_string['link'], page_request, i+1, q_string['by'])
            page['content'] = i + 1
            pages.append(page)
    if paginator['cur_page'] < paginator['total_pages']:
        paginator['next_link'] = '%s?%spage=%s&by=%s' % (q_string['link'], page_request, paginator['next_page'], q_string['by'])
    if paginator['cur_page'] > 1:
        paginator['prev_link'] = '%s?%spage=%s&by=%s' % (q_string['link'], page_request, paginator['next_page'], q_string['by'])

    c = {
      'q_string': q_string,
      'paginator': paginator,
      'pages': pages,
      'page_request': page_request,
      'select': select,
      'ends': paginator['ends'],
    }
    return t.render(c)
