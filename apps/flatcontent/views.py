# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from apps.main_functions.files import check_path, full_path, file_size
from apps.main_functions.functions import object_fields, recursive_fill, sort_voca
from apps.main_functions.model_helper import create_model_helper
from apps.main_functions.tabulator import tabulator_filters_and_sorters
from apps.main_functions.atomic_operations import atomic_update, bulk_replace

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
    mh.filter_add({'container__id': mh_containers.row.id})

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
        result = []
        for row in rows:
            item = object_fields(row)
            #item['container'] = obj_container
            item['actions'] = row.id
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
            item['folder'] = row.get_folder()
            item['container_name'] = mh_containers.row.name
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
        operation = request.GET.get("operation")
        # Получить каталог
        if operation == "get_children" and mh.permissions['view']:
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
