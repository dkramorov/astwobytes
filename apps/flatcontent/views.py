# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from django.core.cache import cache

from apps.main_functions.files import check_path, full_path, file_size
from apps.main_functions.functions import object_fields, recursive_fill, sort_voca
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.tabulator import tabulator_filters_and_sorters
from apps.main_functions.atomic_operations import atomic_update, bulk_replace
from apps.main_functions.crypto import serp_hash

from .models import (Containers,
                     Blocks,
                     LinkContainer,
                     get_ftype,
                     update_containers_vars,
                     update_blocks_vars, )

CUR_APP = 'flatcontent'
containers_vars = {
    'singular_obj': '',
    'plural_obj': '',
    'rp_singular_obj': '',
    'rp_plural_obj': '',
    'template_prefix': '',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'flatcontent',
    'submenu': '',
    'show_urla': 'show_containers',
    'create_urla': 'create_container',
    'edit_urla': 'edit_container',
    'model': Containers,
}

@login_required
def show_containers(request, ftype: str, *args, **kwargs):
    """Вывод контейнеров"""
    mh_vars = containers_vars.copy()
    update_containers_vars(ftype, mh_vars)

    mh = create_model_helper(mh_vars, request, CUR_APP, reverse_params={'ftype': ftype})
    context = mh.context
    context['ftype_state'] = get_ftype(ftype)
    mh.filter_add({'state': context['ftype_state']})

    # -----------------------
    # Фильтрация и сортировка
    # -----------------------
    filters_and_sorters = tabulator_filters_and_sorters(request)
    for rfilter in filters_and_sorters['filters']:
        mh.filter_add(rfilter)
    for rsorter in filters_and_sorters['sorters']:
        mh.order_by_add(rsorter)
    context['fas'] = filters_and_sorters['params']

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        result = []
        for row in rows:
            item = object_fields(row)
            item['actions'] = row.id
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
            item['folder'] = row.get_folder()
            result.append(item)

        if request.GET.get('page'):
            result = {'data': result,
                      'last_page': mh.raw_paginator['total_pages'],
                      'total_records': mh.raw_paginator['total_records'],
                      'cur_page': mh.raw_paginator['cur_page'],
                      'by': mh.raw_paginator['by'], }
        return JsonResponse(result, safe=False)
    template = '%stable.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def edit_container(request, ftype: str, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование контейнера"""
    mh_vars = containers_vars.copy()
    update_containers_vars(ftype, mh_vars)

    mh = create_model_helper(mh_vars, request, CUR_APP, action, reverse_params={'ftype': ftype})
    context = mh.context
    context['ftype_state'] = get_ftype(ftype)
    mh.filter_add({'state': context['ftype_state']})

    row = mh.get_row(row_id)
    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))

    if mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'ftype': ftype, 'action': 'edit', 'row_id': mh.row.id})
        mh.url_tree = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'ftype': ftype, 'action': 'tree', 'row_id': mh.row.id})
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['row']['folder'] = mh.row.get_folder()
        context['redirect'] = mh.url_edit
        context['url_edit'] = mh.url_edit
        context['url_tree'] = mh.url_tree
        mh.breadcrumbs_add({
            'link': mh.url_edit,
            'name': mh.row.name,
        })

    if request.method == 'GET':
        if action == 'create':
            mh.breadcrumbs_add({
                'link': mh.url_create,
                'name': '%s %s' % (mh.action_create, mh.rp_singular_obj),
            })
        elif action == 'edit' and row:
            mh.breadcrumbs_add({
                'link': mh.url_edit,
                'name': '%s %s' % (mh.action_edit, mh.rp_singular_obj),
            })
        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удален' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'
        elif action == 'tree' and row:
            context['is_tree'] = True
            context['container'] = row
            mh.breadcrumbs_add({
                'link': mh.url_edit,
                'name': '%s %s' % ('Иерархия', mh.rp_singular_obj),
            })

    elif request.method == 'POST':
        pass_fields = ()
        mh.post_vars(pass_fields=pass_fields)

        if action == 'create' or (action == 'edit' and row):
            if action == 'create':
                if mh.permissions['create']:
                    mh.row = mh.model()
                    mh.save_row()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            if action == 'edit':
                if mh.permissions['edit']:
                    mh.save_row()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
        # --------------------
        # Загрузка изображения
        # --------------------
        elif action == 'img' and request.FILES:
            mh.uploads()

    if mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'ftype': ftype,
                                      'action': 'edit',
                                      'row_id': mh.row.id})
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['row']['folder'] = mh.row.get_folder()
        context['redirect'] = mh.url_edit

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def containers_positions(request, ftype: str, *args, **kwargs):
    """Изменение позиций контейнеров"""
    result = {}
    mh_vars = containers_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions', reverse_params={'ftype': ftype})
    mh.filter_add({'state': get_ftype(ftype)})
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

blocks_vars = {
    'singular_obj': 'Блок',
    'plural_obj': 'Блоки',
    'rp_singular_obj': 'блока',
    'rp_plural_obj': 'блоков',
    'template_prefix': '',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'flatcontent',
    'submenu': '',
    'show_urla': 'show_blocks',
    'create_urla': 'create_block',
    'edit_urla': 'edit_block',
    'model': Blocks,
}

@login_required
def show_blocks(request, ftype: str, container_id: int, *args, **kwargs):
    """Вывод блоков"""
    mh_vars = blocks_vars.copy()
    update_blocks_vars(ftype, mh_vars)

    # -------------------------------
    # Родительская модель (контейнер)
    # -------------------------------
    mh_vars_containers = containers_vars.copy()
    update_containers_vars(ftype, mh_vars_containers)
    mh_containers = create_model_helper(mh_vars_containers, request, CUR_APP, reverse_params={'ftype': ftype})
    container = mh_containers.get_row(container_id)
    if mh_containers.error:
        return redirect('%s?error=not_found' % (mh_containers.root_url, ))
    mh_containers.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars_containers['edit_urla']),
        kwargs={'ftype': ftype,
                'action': 'edit',
                'row_id': mh_containers.row.id})
    mh_containers.url_tree = reverse('%s:%s' % (CUR_APP, mh_vars_containers['edit_urla']),
        kwargs={'ftype': ftype,
                'action': 'tree',
                'row_id': mh_containers.row.id})

    mh = create_model_helper(mh_vars, request, CUR_APP, reverse_params={'ftype': ftype, 'container_id': container_id})

    # ---------------------------
    # Родительские хлебные крошки
    # ---------------------------
    for i, crumb in enumerate(mh_containers.breadcrumbs):
        mh.breadcrumbs.insert(i, crumb)
    # ----------------------------
    # Редактирование родительского
    # контейнера в хлебных крошках
    # ----------------------------
    mh.breadcrumbs.insert(i + 1, {
        'link': mh_containers.url_edit,
        'name': mh_containers.row.name or '%s %s' % (mh_containers.action_edit, mh_containers.rp_singular_obj),
    })

    context = mh.context
    context['ftype_state'] = get_ftype(ftype)
    context['container'] = mh_containers.row
    context['url_edit'] = mh_containers.url_edit
    context['url_tree'] = mh_containers.url_tree

    mh.filter_add({'container__id': mh_containers.row.id})
    mh.filter_add(Q(parents=''))
    # -----------------------
    # Фильтрация и сортировка
    # -----------------------
    filters_and_sorters = tabulator_filters_and_sorters(request)
    for rfilter in filters_and_sorters['filters']:
        mh.filter_add(rfilter)
    for rsorter in filters_and_sorters['sorters']:
        mh.order_by_add(rsorter)
    context['fas'] = filters_and_sorters['params']

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    #obj_container = object_fields(container)
    if request.is_ajax():
        rows = mh.standard_show()
        # ---------------------
        # Находим _children для
        # древовидной структуры
        # ---------------------
        ids_parents = ['_%s' % (row.id, ) for row in rows]
        cond = Q()
        cond.add(Q(parents__in=ids_parents), Q.OR)
        for parent in ids_parents:
            cond.add(Q(parents__startswith='%s_' % (parent, )), Q.OR)
        subrows = Blocks.objects.filter(container=mh_containers.row).filter(cond)

        result = []
        for row in rows:
            item = object_fields(row)
            #item['container'] = obj_container
            item['actions'] = row.id
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
            item['folder'] = row.get_folder()
            item['container_name'] = mh_containers.row.name
            children = []
            recursive_fill(subrows, children, parents='_%s' % (row.id, ))
            if children:
                sort_voca(children)
                objs = []
                json_children(children, objs)
                item['_children'] = objs
            result.append(item)

        if request.GET.get('page'):
            result = {'data': result,
                      'last_page': mh.raw_paginator['total_pages'],
                      'total_records': mh.raw_paginator['total_records'],
                      'cur_page': mh.raw_paginator['cur_page'],
                      'by': mh.raw_paginator['by'], }
        return JsonResponse(result, safe=False)
    template = '%stable.html' % (mh.template_prefix, )
    return render(request, template, context)

def json_children(rows: list, result: list):
    """Преобразование древовидной структуры ORM
       в json структуру по всей вложенности"""
    for row in rows:
        obj = object_fields(row)
        if hasattr(row, 'sub'):
            if row.sub:
                obj['_children'] = []
                json_children(row.sub, obj['_children'])
        result.append(obj)

@login_required
def edit_block(request, ftype: str, action: str, container_id: int, row_id: int = None, *args, **kwargs):
    """Создание/редактирование блока"""
    mh_vars = blocks_vars.copy()
    update_blocks_vars(ftype, mh_vars)

    # -------------------------------
    # Родительская модель (контейнер)
    # -------------------------------
    mh_vars_containers = containers_vars.copy()
    update_containers_vars(ftype, mh_vars_containers)
    mh_containers = create_model_helper(mh_vars_containers, request, CUR_APP, reverse_params={'ftype': ftype})
    container = mh_containers.get_row(container_id)
    if mh_containers.error:
        return redirect('%s?error=not_found' % (mh_containers.root_url, ))
    mh_containers.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars_containers['edit_urla']),
        kwargs={'ftype': ftype,
                'action': 'edit',
                'row_id': mh_containers.row.id})
    mh_containers.url_tree = reverse('%s:%s' % (CUR_APP, mh_vars_containers['edit_urla']),
        kwargs={'ftype': ftype,
                'action': 'tree',
                'row_id': mh_containers.row.id})

    mh = create_model_helper(mh_vars, request, CUR_APP, action, reverse_params={'ftype': ftype, 'container_id': container_id})
    mh.select_related_add('container')

    # ---------------------------
    # Родительские хлебные крошки
    # ---------------------------
    for i, crumb in enumerate(mh_containers.breadcrumbs):
        mh.breadcrumbs.insert(i, crumb)
    # ----------------------------
    # Редактирование родительского
    # контейнера в хлебных крошках
    # ----------------------------
    mh.breadcrumbs.insert(i + 1, {
        'link': mh_containers.url_edit,
        'name': mh_containers.row.name or '%s %s' % (mh_containers.action_edit, mh_containers.rp_singular_obj),
    })

    context = mh.context
    context['ftype_state'] = get_ftype(ftype)
    context['container'] = object_fields(mh_containers.row)
    context['url_edit'] = mh_containers.url_edit
    context['url_tree'] = mh_containers.url_tree

    mh.filter_add({'container__id': mh_containers.row.id})

    row = mh.get_row(row_id)
    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))

    if request.method == 'GET':
        if action == 'create':
            mh.breadcrumbs_add({
                'link': mh.url_create,
                'name': '%s %s' % (mh.action_create, mh.rp_singular_obj),
            })
        elif action == 'edit' and row:
            mh.breadcrumbs_add({
                'link': mh.url_edit,
                'name': '%s %s' % (mh.action_edit, mh.rp_singular_obj),
            })
        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удален' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'

    elif request.method == 'POST':
        pass_fields = ()
        mh.post_vars(pass_fields=pass_fields)

        if action == 'create' or (action == 'edit' and row):
            if action == 'create':
                if mh.permissions['create']:
                    mh.row = mh.model()
                    mh.save_row()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            if action == 'edit':
                if mh.permissions['edit']:
                    mh.save_row()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
        # --------------------
        # Загрузка изображения
        # --------------------
        elif action == 'img' and request.FILES:
            mh.uploads()

    if mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'ftype': ftype,
                                      'action': 'edit',
                                      'container_id': mh_containers.row.id,
                                      'row_id': mh.row.id})
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['row']['folder'] = mh.row.get_folder()
        context['row']['container_name'] = mh_containers.row.name
        context['redirect'] = mh.url_edit

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def blocks_positions(request, ftype: str, container_id: int, *args, **kwargs):
    """Изменение позиций блоков в контейнере"""
    result = {}
    mh_vars = blocks_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions', reverse_params={'ftype': ftype})
    mh.filter_add({'state': get_ftype(ftype)})
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def prepare_jstree(data, menus):
    """Вспомогательная функция для построения
       меню из queryset в формат jstree"""
    for menu in menus:
        data.append({
            'id': menu.id,
            'text': menu.name,
            'state': {'opened': False, 'selected': False},
            'children': [],
        })
        if hasattr(menu, 'sub'):
            if menu.sub:
                prepare_jstree(data[-1]['children'], menu.sub)

@login_required
def tree_co(request):
    """Дерево контейнера и операции над ним"""
    errors = []
    result = []

    container_id = request.GET.get('container_id')
    container = Containers.objects.filter(pk=container_id).first()
    if not container:
        return JsonResponse(result, safe=False)

    mh_vars = containers_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'tree', reverse_params={'ftype': 'flatmain'})

    if request.method == 'GET':
        operation = request.GET.get('operation')
        # Выбрать узел
        if operation == 'select_node':
            node_id = int(request.GET.get('node_id'), 0)
            node = Blocks.objects.filter(container=container, pk=node_id).first()
            if node:
                result = object_fields(node)
                result['folder'] = node.get_folder()
                result['thumb'] = node.thumb()
                mh_vars_blocks = blocks_vars.copy()
                result['url_edit'] = reverse('%s:%s' % (CUR_APP,
                    mh_vars_blocks['edit_urla']),
                    kwargs={'ftype': get_ftype(container.state, by_id=True),
                            'action': 'edit',
                            'container_id': container.id,
                            'row_id': node.id})
                result['url_upload_img'] = reverse('%s:%s' % (CUR_APP,
                    mh_vars_blocks['edit_urla']),
                    kwargs={'ftype': get_ftype(container.state, by_id=True),
                            'action': 'img',
                            'container_id': container.id,
                            'row_id': node.id})
                result = {'row': result}
        # Получить каталог
        elif operation == 'get_children' and mh.permissions['view']:
            menus = []
            query = Blocks.objects.filter(container=container).order_by('position')
            recursive_fill(query, menus, parents='')
            sort_voca(menus)
            data = []
            prepare_jstree(data, menus)
            result = [{
                'id': 'container_%s' % (container.id, ),
                'text': container.name,
                'state': {'opened': True, 'selected': False, 'disabled': True},
                'children': data,
            }]
        # Создание / редактирование рубрики
        elif operation == 'rename_node' and mh.permissions['edit']:
            node_id = request.GET.get('node_id')
            node_name = request.GET.get('name')
            menu = None
            if node_id.isdigit():
                menu = Blocks.objects.filter(pk=node_id, container=container).first()
            if not menu:
                parent_id = request.GET.get('parent_id')
                parents_str = ''
                parent = Blocks.objects.filter(pk=parent_id, container=container).first()
                if parent:
                    parents_str = '_%s' % (parent.id, )
                    if parent.parents:
                        parents_str = '%s_%s' % (parent.parents, parent.id)
                menu = Blocks(parents=parents_str, container=container)
            menu.name = node_name
            menu.save()
            result = {'success': True, 'id': menu.id}
        elif operation == 'drop_node' and mh.permissions['drop']:
            node_id = request.GET.get('node_id')
            menu = Blocks.objects.filter(pk=node_id, container=container).first()
            if menu:
                parents_str = '_%s' % (menu.id, )
                if menu.parents:
                    parents_str = '%s_%s' % (menu.parents, menu.id)
                children = Blocks.objects.filter(Q(parents=parents_str)|Q(parents__startswith='%s_' % (parents_str, )))
                for child in children:
                    child.delete()
                menu.delete()
                result = {'success': True}
            else:
                result = {'error': True}
        elif operation == 'move_node' and mh.permissions['edit']:
            node_id = request.GET.get('node_id')
            parent_id = request.GET.get('parent_id', '')
            position = request.GET.get('position', '')
            menu = Blocks.objects.filter(pk=node_id, container=container).first()
            parent = None
            if menu and position.isdigit() and parent_id.isdigit():
                # Находим родительскую рубрику, куда переносим хозяйство
                parent_parents = ''
                parent_id = int(parent_id)
                if parent_id > 0:
                    parent = Blocks.objects.filter(pk=parent_id).first()
                    parent_parents = '_%s' % (parent.id, )
                    if parent:
                        parent_parents = '%s_%s' % (parent.parents, parent.id)

                position = int(position)
                menu_parents = '_%s' % (menu.id, )
                if menu.parents:
                    menu_parents = '%s_%s' % (menu.parents, menu.id)

                # 1) Одинаковая корневая рубрика - меняем просто позицию
                # 2) Разная корневая рубрика
                #     a) parents всех вложенных рубрик
                #     b) родительский parents
                if not parent_parents == menu_parents:
                    new_parents = '%s_%s' % (parent_parents, menu.id)
                    queryset = Blocks.objects.filter(container=container).filter(Q(parents=menu_parents)|Q(parents__startswith='%s_' % (menu_parents, )))
                    bulk_replace(queryset, 'parents', menu_parents, new_parents)
                    Blocks.objects.filter(pk=menu.id).update(**{'parents': parent_parents})
                # Меняем позицию в любом случае
                ids_menus = list(Blocks.objects.filter(parents=menu.parents, container=container).exclude(pk=menu.id).values_list('id', flat=True).order_by('position'))
                ids_menus.insert(position, menu.id)
                atomic_update(Blocks, [{'id': item, 'position': i + 1} for i, item in enumerate(ids_menus)])
                result = {'success': True}
            else:
                result = {'error': True}

    return JsonResponse(result, safe=False)

def SearchLink(urla: str,
               q_string: dict = None,
               request = None,
               mcap: dict = None,
               cache_time: int = 60):
    """Страница поиска неслужебных ссылок (статич.)
        mcap - Main (tag) Content for All Pages
        mcap должно на выходе содержать (("main", ))
        mcap это замена get_containers(("main", ))
        Можно передать в mcap список по умолчанию
        выводимых контейнеров, затем в шаблоне
        выводить их куда следует по одному через page

        containers = { # это mcap
            "social_sidebar":None,
            "news_sidebar":None,
            "subscribe":None,
            "article_sidebar":None,
        }"""
    is_static_path = False
    path_info = '/'

    if not mcap:
        mcap = {'main': None}

    if request:
        path_info = request.META['PATH_INFO']

        if '/media/' in path_info or '/static/' in path_info:
            is_static_path = True

        link_with_params = path_info
        query_string = request.META['QUERY_STRING']
        if query_string:
            link_with_params += '?%s' % (query_string, )

        hashed_link = serp_hash(link_with_params.encode('utf-8'))
        cache_var = '%s_%s' % (hashed_link, settings.DATABASES['default']['NAME'])
        # Если сайт мультиязычный, то кэш нужен на домен
        if settings.IS_DOMAINS:
            domain = get_domain(request)
            cache_var = "%s_%s" % (domain, cache_var)

        # На хостинге может так случиться,
        # что мы будем в кэш пихать статику (файлы),
        # надо статику раньше обрабатывать
        # чем ссылки на статические странички
        if not is_static_path:
            inCache = cache.get(cache_var)
            if inCache:
                block_with_content = inCache['block_with_content']
                # Нужно дозаполнить q_string, mcap
                if block_with_content:
                    head_fill(block_with_content, q_string)
                mcap = {key: value for key, value in inCache['mcap'].items()}
                return block_with_content

    # all_blocks нужны только для перевода
    all_blocks = []
    all_containers = []

    # Блок с title/description
    # Его будем считать правильным
    block_with_content = None

    # Ищем менюшку
    # Ищем привязки к менюшке
    ids_containers = {}

    container_all_pages = Containers.objects.filter(tag__in=mcap.keys()).exclude(state__in=(99, 100))

    for cap in container_all_pages:
        ids_containers[cap.id] = {
            'container': cap,
            'blocks': [],
            'tags': {},
            'prices': [],
            'forest': None,
            'position': cap.position,
        }
        all_containers.append(cap) # Для перевода

    blocks = Blocks.objects.filter(link=path_info, state=4)

    # Найдем менюшку -
    # найдем привязанные контейнеры
    if blocks:
        for block in blocks:
            if block.title or block.description:
                block_with_content = block
        if not block_with_content:
            block_with_content = blocks[0]

        all_blocks.append(block_with_content) # Для перевода

    if block_with_content:
        containers = LinkContainer.objects.select_related('container').filter(block=block_with_content)
        if containers:
            for container in containers:
                all_containers.append(container.container) # Для перевода
                ids_containers[container.container.id] = {
                    'container': container.container,
                    'blocks': [],
                    'tags': {},
                    'prices': [],
                    'forest': None,
                    'position': container.position,
                }

    # ids_containers[container.container.id] = {
    #     "container":container.container,
    #     "blocks":[],
    #     "tags":{},
    #     "prices":[],
    #     "forest":None,
    #     "position":container.position,
    # }
    templar(ids_containers, mcap, block_with_content, all_containers, all_blocks, q_string, request)

    # -----
    # CACHE
    # -----
    if request:
        if not is_static_path:
            d = {
                'mcap': mcap,
                'block_with_content': block_with_content,
            }
            if not settings.DEBUG:
                cache.set(cache_var, d, cache_time)
    return block_with_content

def templar(ids_containers: dict, mcap: dict, block_with_content: Blocks,
            all_containers: list, all_blocks: list, q_string: dict,
            request=None, cache_time: int = 60):
    """Готовит данные к flatcontent тегу
       l = LinkContainer ...
       ids_containers[l.container.id] = {
           "container":container.container,
           "blocks":[],
           "tags":{},
           "prices":[],
           "forest":None,
           "position":container.position
       }"""
    # Возможно, есть контейнеры с товарами/услугами
    # Либо контейнеры с выводом рубрик
    have_prices = []
    blocks_prices = {}
    have_cats = {}

    if ids_containers:
      blocks = Blocks.objects.filter(container__in=ids_containers.keys())
      if is_prices:
        # Обрабатываем нестандартные контейнеры
        prices = PriceContainer.objects.select_related("price").filter(container__in=ids_containers.keys()).order_by("position")
        ids_prices = {x.price.id:x.price for x in prices}
        # Разные типы цен
        get_costs_types(ids_prices)
        # Находим скидки для всех товаров
        shopper = None
        if request:
          shopper = request.session.get("shopper", None)
        search_disconts_for_prices(ids_prices, shopper)
        # Рейтинги товаров/услуг
        if is_reviews:
          get_objects_ratings(ids_prices, "price.Products")
        # Переводим товары/услуги
        if settings.IS_DOMAINS and request:
          ct_prices = ContentType.objects.get_for_model(Products)
          get_translations(ids_prices.values(), ct_prices)
          translate_rows(ids_prices.values(), request)

        # Для сохранения сортировки идем по prices
        for item in prices:
          price = ids_prices[item.price.id]

          if item.block_id:
            if not item.block_id in blocks_prices:
              blocks_prices[item.block_id] = []
            blocks_prices[item.block_id].append(price)
          else:
            if item.container_id in ids_containers:
              ids_containers[item.container_id]['prices'].append(price)
            have_prices.append(item.container_id)

        # Ищем скидки/акции по товарам/услугам
        if have_prices:
          disconts = Disconts.objects.filter(container__in=have_prices)
          for discont in disconts:
            # Добавлять надо к самому контейнеру
            for key, value in ids_containers.items():
              container_id = value['container'].id
              if discont.container_id == container_id:
                value['container'].discont = discont
                break

      if is_trees:
        # Обрабатываем нестандартные контейнеры
        # Достаем только рубрики пришитые к контейнерам
        # А через templatetags flatcats достанем
        # все контейнеры, пришитые к рубрике
        trees_containers = []
        for key, value in ids_containers.items():
          if value['container'].state == 7:
            trees_containers.append(key)

        forests = Forest.objects.all()
        forests = forests.filter(Q(container__in=trees_containers))
        forests = forests.filter(tol=1)
        forests = forests.order_by("position")
        for item in forests:
          if not item.container_id in have_cats:
            have_cats[item.container_id] = []
          have_cats[item.container_id].append(item.cat_id)
        # На каждый контейнер надо выдирать
        # содержание рубрик с пагинацией
        l_vars = {
            "root_url":"/blog/",
            "singular_obj":u"Статья",
            "plural_obj":u"Статьи",
            "breadcrumbs":[],
            "template_prefix":"flatcontent_",
            "paginator_template":"web/paginator.html",
            "action_add":u"Добавить",
            "action_edit":u"Исправить"
        }
        # Ищем содержимое (блоки) для контейнеров с рубриками
        if have_cats:
          # Достаем все встреченные рубрики
          ids_rubrics = {}
          for key, value in have_cats.items():
            for cat_id in value:
              ids_rubrics[cat_id] = None
          rubrics = Catalogue.objects.filter(pk__in=ids_rubrics.keys())
          for rubric in rubrics:
            ids_rubrics[rubric.id] = rubric

          forest_containers = {}
          by_blocks = filter(lambda x:(x.tag == "by" and x.description), [y for y in blocks])
          # Далее по каждому контейнеру!
          # Достаем с постраничной навигацией
          for key, value in ids_containers.items():
            container_id = value['container'].id
            # Если данный контейнер с прилепленными рубриками
            if container_id in have_cats:
              l = StandardAdmin(Forest, request)
              for key in l_vars:
                setattr(l, key, l_vars[key])
              l.q_string_fill()
              # Проверяем подблоки в контейнере,
              # возможно, там есть указания о
              # количестве записей на страничке и др
              if by_blocks:
                for by_block in by_blocks:
                  if by_block.container_id == container_id:
                    try:
                      by = int(qqize(by_block.description))
                    except ValueError:
                      by = None
                    if by:
                      l.q_string['by'] = by
                    break
              l.select_related_add("container")
              l.filter_add(Q(cat_id__in=have_cats[container_id]))
              l.filter_add(Q(tol__isnull=True))
              l.order_by_add("position")
              rows = l.standard_show()
              paginator = l.paginator
              value['forest'] = {"rows":[], "paginator":paginator, "cats":[]}
              for row in rows:
                row.container.blocks = []
                # Прилепляем рубрику к контейнеру
                # Прикрепляем к лесу контейнеры
                linked_cats = have_cats[container_id]
                for cat in linked_cats:
                  if cat in ids_rubrics:
                    value['forest']['cats'].append(ids_rubrics[cat])
                value['forest']['rows'].append(row.container)
                forest_containers[row.container_id] = row.container
          # Теперь надо выдрать блоки под контейнеры
          trees_blocks = Blocks.objects.filter(container__in=forest_containers.keys()).order_by("position")
          for block in trees_blocks:
            forest_containers[block.container_id].blocks.append(block)

      for block in blocks:
        if block.id in blocks_prices:
          block.prices = blocks_prices[block.id]

        ids_containers[block.container_id]['blocks'].append(block)
        all_blocks.append(block) # Для перевода

      for key, value in ids_containers.items():
        menu_queryset = []
        recursive_fill(value['blocks'], menu_queryset)
        menus = sort_voca(menu_queryset)
        ids_containers[key]['blocks'] = menus
        # Добавляем словарь по тегу в каждый контейнер
        for item in value['blocks']:
          if item.tag:
            ids_containers[key]['tags'][item.tag] = item

        # MCAP (Main Content for All Pages)
        if value['container'].tag == "main":
          mcap['main'] = value
      if block_with_content:
        block_with_content.containers = sorted(ids_containers.values(), key=lambda x: x['position']) #ids_containers.values()

    # Переводим блоки/контейнеры
    if settings.IS_DOMAINS and request:
      ct_blocks = ContentType.objects.get_for_model(Blocks)
      ct_containers = ContentType.objects.get_for_model(Containers)
      get_translations(all_blocks, ct_blocks)
      translate_rows(all_blocks, request)
      get_translations(all_containers, ct_containers)
      translate_rows(all_containers, request)

    if block_with_content:
      head_fill(block_with_content, q_string)
    # Если надо работать через кэш
