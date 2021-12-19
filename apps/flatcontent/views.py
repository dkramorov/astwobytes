# -*- coding:utf-8 -*-
import os
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.conf import settings
from django.core.cache import cache

from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.functions import object_fields, recursive_fill, sort_voca
from apps.main_functions.model_helper import ModelHelper, create_model_helper
from apps.main_functions.atomic_operations import atomic_update, bulk_replace
from apps.main_functions.crypto import serp_hash
from apps.main_functions.files import (check_path,
                                       full_path,
                                       file_size,
                                       make_folder,
                                       copy_file, )
from apps.flatcontent.models import (Containers,
                                     Blocks,
                                     LinkContainer,
                                     get_ftype,
                                     update_containers_vars,
                                     update_blocks_vars,
                                     prepare_jstree,
                                     FAT_HIER, )

is_products = False
if 'apps.products' in settings.INSTALLED_APPS:
    is_products = True
    from apps.flatcontent.flatcat import get_costs_types
    from apps.products.models import Products, ProductsCats

if settings.IS_DOMAINS:
    from apps.languages.models import (
        get_domain,
        get_domains,
        get_translate,
        get_content_type,
        translate_rows, )

def api(request,
        action: str = 'containers',
        ftype: str = 'flatcat'):
    """Апи-метод для получения всех данных
       /flatcontent/blocks/flatcat/api/?filter__container=1&filter__parents=_1
    """

    mh_vars = containers_vars.copy()
    update_containers_vars(ftype, mh_vars)
    reverse_params = {'ftype': ftype}
    if action == 'blocks':
        container_id = request.GET.get('container_id') or request.POST.get('container_id') or 0
        mh_blocks_vars = blocks_vars.copy()
        update_blocks_vars(ftype, mh_blocks_vars)
        reverse_params['container_id'] = container_id
        return ApiHelper(request, mh_blocks_vars, CUR_APP, reverse_params=reverse_params)
    return ApiHelper(request, mh_vars, CUR_APP, reverse_params=reverse_params)

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

def clone_block(block, container, parents: str = None):
    """Клонирование блоков в другой контейнер
       Изменение pk, parents, img
       :param block: клонируемый блок
       :param container: контейнер получатель клонируемого блока
       :param parents: вложенность
    """
    img = folder = None
    if block.img:
        folder = block.get_folder()
        img = block.img

    pk = block.id
    block.id = None
    block.container = container
    block.parents = parents
    block.save()
    if img:
        new_folder = block.get_folder()
        make_folder(new_folder)
        copy_file(os.path.join(folder, img), os.path.join(new_folder, img))
    # ---------------------------------------------------
    # Каждый блок проверяем на линковку к Товарам/Услугам
    # ---------------------------------------------------
    if is_products:
        if hasattr(container, 'container_products'):
            for product in container.container_products:
                if product.cat_id == pk:
                    new = ProductsCats.objects.create(container=container, cat=block, product=product.product)
    # -------------------------
    # Спускаемся по вложенности
    # -------------------------
    if block.sub:
        if parents:
            parents += '_%s' % block.id
        else:
            parents = '_%s' % block.id
        for item in block.sub:
            clone_block(item, container, parents)
    return block

def fill_from_template(row, state: int = 99):
    """Заполнение контейнера данными из шаблона
       Нужно делать только если создаем контейнер,
       либо контейнер пустой и его сохранили
       :param row: контейнер
    """
    template = Containers.objects.filter(tag=row.tag, state=state).exclude(pk=row.id).first()
    if not template:
        return
    # --------------------------------------------------
    # Если мы создаем и не заполнен name/description/img
    # Заполняем контейнер как в шаблоне
    # --------------------------------------------------
    blocks = template.blocks_set.all()
    # ----------------------------
    # Записываем данные от шаблона
    # ----------------------------
    need_resave = False
    fields = ('template_position', 'name', 'description')
    for field in fields:
        value = getattr(template, field)
        if not getattr(row, field) and value:
            setattr(row, field, value)
            need_resave = True
    if template.img:
        new_folder = row.get_folder()
        make_folder(new_folder)
        copy_file(os.path.join(template.get_folder(), template.img), os.path.join(new_folder, template.img))
        row.img = template.img
        need_resave = True
    if need_resave:
        row.save()
    # ----------------------------------------------
    # Проверяем привязаны ли к шаблону Акции/Скидки
    # Проверяем привязаны ли к шаблону Товары/Услуги
    # ----------------------------------------------
    if is_products:
        container_products = []
        ids_blocks = [block.id for block in blocks]
        products = ProductsCats.objects.select_related('product').filter(Q(container=template)|Q(cat__in=ids_blocks))
        for product in products:
            # ------------------------------
            # Те, что НЕ привязаны к блокам,
            # создаем для контейнера,
            # остальное через clone_block
            # ------------------------------
            if not product.cat_id:
                ProductsCats.objects.create(container=row, product=product.product)
            else:
                container_products.append(product)
        row.container_products = container_products

    result = []
    recursive_fill(blocks, result)
    for block in result:
        clone_block(block, row)

def redirect_if_flatmain(ftype: str):
    """Если это контент для всех страничек,
       то переадресация сразу на блоки,
       например,
       c  /flatcontent/admin/flatmain/
       на /flatcontent/admin/flatmain/1/
       :param ftype: тип контейнера
    """
    if not ftype == 'flatmain':
        return
    flatmain = Containers.objects.filter(state=2, tag='main').values_list('id', flat=True).first()
    if flatmain:
        link = reverse('%s:%s' % (CUR_APP, blocks_vars['show_urla']),
                       kwargs={'ftype': ftype, 'container_id': flatmain})
        return link

@login_required
def show_containers(request, ftype: str, *args, **kwargs):
    """Вывод контейнеров"""
    mh_vars = containers_vars.copy()
    update_containers_vars(ftype, mh_vars)

    flatmain_link = redirect_if_flatmain(ftype)
    if flatmain_link:
        return redirect(flatmain_link)

    mh = create_model_helper(mh_vars, request, CUR_APP, reverse_params={'ftype': ftype})
    context = mh.context
    context['is_products'] = is_products
    context['ftype_state'] = get_ftype(ftype)
    mh.filter_add({'state': context['ftype_state']})

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

    template_prefix = 'flatcontent_core_'
    # Если буду разделять вывод, то заюзаю конструкцию
    # template_prefix = mh.template_prefix
    # if context['ftype'] in ('flattemplates', 'flatpages', ):
    #     template_prefix = 'flatcontent_core_'

    template = '%stable.html' % template_prefix
    return render(request, template, context)

def reverse_edit(mh_vars: dict, ftype: str, action: str, row_id: int):
    """Вспомогательная функция для ссылки редактирования контейнера,
       чтобы трехэтажный kwargs не писать каждый раз
       :param mh_vars: словарь с данными по модельке
       :param ftype: тип стат. страничек
       :param action: действие
       :param row_id: ид для реверса
    """
    edit_link = '%s:%s' % (CUR_APP, mh_vars['edit_urla'])
    return reverse(edit_link, kwargs={
        'ftype': ftype,
        'action': action,
        'row_id': row_id,
    })

@login_required
def edit_container(request, ftype: str, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование контейнера"""
    mh_vars = containers_vars.copy()
    update_containers_vars(ftype, mh_vars)

    mh = create_model_helper(mh_vars, request, CUR_APP, action, reverse_params={'ftype': ftype})
    ftype_state = get_ftype(ftype)
    mh.reverse_params = {'ftype': ftype}
    mh.filter_add({'state': ftype_state})
    row = mh.get_row(row_id)
    context = mh.context
    context['is_products'] = is_products
    # ----------------------------
    # Не грузим таблицу по товарам
    # ----------------------------
    if ftype in ('flatmenu', 'flatmain'):
        context['is_products'] = False
    # ----------------------------
    # Подливаем линковку к менюшке
    # ----------------------------
    elif ftype == 'flatpages':
        links = LinkContainer.objects.select_related('block', 'block__container').filter(container=mh.row)
        edit_link = '%s:%s' % (CUR_APP, mh_vars['edit_urla'])
        fmenu = 'flatmenu'
        context['links'] = [{
            'id': link.block.id,
            'container_id': link.block.container_id,
            'name': link.block.name,
            'tag': link.block.tag,
            'link': link.block.link,
            'container': object_fields(link.block.container),
            'blocks': reverse('%s:%s' % (CUR_APP, blocks_vars['show_urla']),
                              kwargs={'ftype': fmenu, 'container_id': link.block.container_id}),
            'edit': reverse_edit(mh_vars, fmenu, 'edit', link.block.container_id),
            'tree': reverse_edit(mh_vars, fmenu, 'tree', link.block.container_id),
        } for link in links]

    context['ftype_state'] = ftype_state

    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))

    if mh.row:
        mh.url_tree = reverse_edit(mh_vars, ftype, 'tree', mh.row.id)
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['row']['folder'] = mh.row.get_folder()
        context['redirect'] = mh.get_url_edit()
        context['url_tree'] = mh.url_tree
        mh.breadcrumbs_add({
            'link': reverse('%s:%s' % (CUR_APP, blocks_vars['show_urla']),
                            kwargs={'ftype': ftype, 'container_id': mh.row.id}),
            'name': mh.row.name,
        })

    if request.method == 'GET':
        if action in ('edit', 'show') and mh.row:
            if is_products:
                context['products'] = ProductsCats.objects.select_related('product').filter(container=mh.row, cat__isnull=True).values_list('product__id', 'product__name', 'product__code')
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
            context['lazy'] = row.blocks_set.all().aggregate(Count('id'))['id__count'] > FAT_HIER
            mh.breadcrumbs_add({
                'link': mh.url_edit,
                'name': '%s %s' % ('Вид деревом', mh.rp_singular_obj),
            })
            # В иерархии нужны права именно блоков,
            # а не контейнеров
            mh.get_permissions(Blocks)
            context['permissions'] = mh.permissions
        elif action == 'copy' and row:
            # ---------------------
            # Клонировать контейнер
            # ---------------------
            if mh.permissions['create'] and mh.permissions['edit']:
                new_container = row
                new_container.id = None
                new_container.position = None
                new_container.save()
                fill_from_template(new_container, row.state)
                urla = reverse_edit(mh_vars, ftype, 'edit', new_container.id)
                return redirect(urla)
            else:
                context['error'] = 'Недостаточно прав'

        elif action == 'show' and row:
            # -------------------------------
            # Просмотр шаблона/стат.странички
            # -------------------------------
            template_position = None
            if row.template_position:
                template_position = row.template_position

            mcap = {'main': None, row.id: None}
            page = Blocks()
            # block_with_content нет, поэтому даже не присваиваем
            context['q_string'] = {}
            SearchLink(context['q_string'], request, mcap)
            page.containers = mcap.values()
            # ---------------------------------------------------
            # page.is_template будет убирает в шаблонах элементы,
            # которые мешают редактору правильно отобразить
            # их редактирование - например, изображение в блоке,
            # который before перекрывает его эффектом
            # ---------------------------------------------------
            page.is_template = 1
            template = 'web/main_stat_template.html'
            context.update({
                'page': page,
                'containers': page.containers,
                'template_position': template_position,
            })
            return render(request, template, context)

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

            # -----------------------------
            # Заполнение данными из шаблона
            # flatpages/flatcat
            # -----------------------------
            row = mh.row
            children = row.blocks_set.all().aggregate(Count('id'))['id__count']
            if not children and is_products:
                children = row.productscats_set.all().aggregate(Count('id'))['id__count']
            if (action == 'create' or not children) and row.tag and row.state in (3, 7):
                fill_from_template(row)
            # Записываем привязки товаров к рубрике
            update_productscats(request, row, None)

        # --------------------
        # Загрузка изображения
        # --------------------
        elif action == 'img' and request.FILES:
            mh.uploads()

    if mh.row:
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['row']['folder'] = mh.row.get_folder()
        context['redirect'] = mh.get_url_edit()

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

def search_containers(request, *args, **kwargs):
    """Поиск контейнеров
       Параметры GET для поиска:
           :param without_templates: Без шаблонов (99,100)
           :param without_menus: Без менюшек (1)
           :param without_main: Без контента для всех страничек (2)
           :param without_seo_prices: Без сео страничек для товаров (4)
           :param without_cats: Без каталогов (7)
           :param with_images: Только с изображениями
           :param only_templates: Только шаблоны state__in=(99,100)
           :param only_cats: Только рубрики state=7
    """
    result = {'results': []}

    mh = ModelHelper(Containers, request)

    # Исключение из поиска определенных типов контейнеров
    exclude_ids = []
    without_templates = request.GET.get('without_templates')
    if without_templates:
        exclude_ids.append(99)
        exclude_ids.append(100)
    without_menus = request.GET.get('without_menus')
    if without_menus:
        exclude_ids.append(1)
    without_main = request.GET.get('without_main')
    if without_main:
        exclude_ids.append(2)
    without_seo_prices = request.GET.get('without_seo_prices')
    if without_seo_prices:
        exclude_ids.append(4)
    without_cats = request.GET.get('without_cats')
    if without_cats:
        exclude_ids.append(7)
    if exclude_ids:
        mh.exclude_add(Q(state__in=exclude_ids))

    only_templates = request.GET.get('only_templates')
    if only_templates:
        mh.filter_add(Q(state__in=(99, 100)))
    only_cats = request.GET.get('only_cats')
    if only_cats:
        mh.filter_add(Q(state=7))
    with_images = request.GET.get('with_images')
    if with_images:
        mh.filter_add(Q(img__isnull=False))

    mh_vars = containers_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)

    mh.search_fields = ('name', 'tag')
    rows = mh.standard_show()

    for row in rows:
        name = '%s #%s' % (row.name, row.id)
        if row.tag:
            name += ' (%s)' % (row.tag, )
        # При поиске по шаблону отдаем тег, а не id в поле id
        if only_templates:
            result['results'].append({'text': name, 'id': row.tag})
        else:
            result['results'].append({'text': name, 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}

    return JsonResponse(result, safe=False)

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

def fill_blocks_breadcrumbs(mh_containers, mh, ftype: str):
    """Заполнить хлебные крошки для контейнеров блока,
       для flatmain мы переадресовываем сразу на блоки,
       поэтому ссыль на контейнер там не нужна
       :param mh_containers: помощник модели по контейнеру
       :param mh: помощник модели по блокам
       :param ftype: раздел
    """
    # ---------------------------
    # Родительские хлебные крошки
    # ---------------------------
    for i, crumb in enumerate(mh_containers.breadcrumbs):
        mh.breadcrumbs.insert(i, crumb)
    # ----------------------------
    # Редактирование родительского
    # контейнера в хлебных крошках
    # ----------------------------
    if ftype == 'flatmain':
        return
    mh.breadcrumbs.insert(i + 1, {
        'link': mh_containers.url_edit,
        'name': mh_containers.row.name or '%s %s' % (mh_containers.action_edit, mh_containers.rp_singular_obj),
    })

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

    fill_blocks_breadcrumbs(mh_containers, mh, ftype)

    context = mh.context
    context['is_products'] = is_products
    context['ftype_state'] = get_ftype(ftype)
    context['container'] = mh_containers.row
    context['url_edit'] = mh_containers.url_edit
    context['url_tree'] = mh_containers.url_tree

    mh.filter_add({'container__id': mh_containers.row.id})

    if not context['fas']['filters']:
        mh.filter_add(Q(parents=''))
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
        pk_arr = Blocks.objects.filter(container=mh_containers.row).filter(cond).values_list('id', flat=True)
        pk_arr = list(pk_arr) # чтобы в subquery не уходило

        # Если слишком много вложенных рубрик, то не выводим
        subrows = []
        if len(pk_arr) < FAT_HIER:
            subrows = Blocks.objects.filter(container=mh_containers.row).filter(pk__in=pk_arr)

        result = []
        for row in rows:
            item = object_fields(row)
            #item['container'] = obj_container
            item['actions'] = row.id
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
            item['folder'] = row.get_folder()
            #item['container_name'] = mh_containers.row.name
            children = []
            recursive_fill(subrows, children, parents='_%s' % (row.id, ))
            if children:
                sorted_children = sort_voca(children)
                objs = []
                json_children(sorted_children, objs)
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
        obj['actions'] = row.id
        obj['thumb'] = row.thumb()
        obj['imagine'] = row.imagine()
        obj['folder'] = row.get_folder()
        if hasattr(row, 'sub'):
            if row.sub:
                obj['_children'] = []
                json_children(row.sub, obj['_children'])
        result.append(obj)

def update_linkcontainer(request, container, row):
    """Записываем линковки к пункту меню / каталогу
       :param request: HttpRequest
       :param container: контейнер блока меню
       :param row: блок меню к которому линкуем контейнеры
    """
    if not container.state in (1, 7):
        return
    LinkContainer.objects.filter(block=row).delete()
    linkcontainer = [int(pk) for pk in request.POST.getlist('linkcontainer') if pk.isdigit()]
    if linkcontainer:
        containers = Containers.objects.filter(pk__in=linkcontainer)
        ids_containers = {cont.id: cont for cont in containers}
        # Соблюдаем последовательность
        for item in linkcontainer:
            if item in ids_containers:
                LinkContainer.objects.create(block=row, container=ids_containers[item])

def update_productscats(request, container, row):
    """Записываем привязки товаров к рубрике
       :param request: HttpRequest
       :param container: контейнер блока-рубрики
       :param row: блок-рубрика к которому привязыаем товары
    """
    if not is_products:
        return
    is_container = False
    old = ProductsCats.objects.all()
    if row:
        old = old.filter(cat=row)
    elif container:
        is_container = True
        old = old.filter(container=container, cat__isnull=True)
    else:
        return

    # Сначала удаляем
    cat_products_fordel = request.POST.get('cat_products_fordel')
    if cat_products_fordel:
        fordel = [pk for pk in cat_products_fordel.split(',') if pk.isdigit()]
        if fordel:
            old.filter(pk__in=fordel).delete()

    # Затем добавляем новые
    new_productscats = []
    productscats = [int(pk) for pk in request.POST.getlist('products')]
    if productscats:
        all_links = old.values_list('product', flat=True)
        exists = [item for item in productscats if item in all_links]
        new_productscats = [item for item in productscats if not item in exists]

    # Удалем товары, которые не встретились
    # для контейнера
    if is_container:
        all_links = old.values_list('product', flat=True)
        absent = [item for item in all_links if not item in productscats]
        if absent:
            ProductsCats.objects.filter(container=container,
                                        cat=row,
                                        product__in=absent).delete()

    if new_productscats:
        # Без моделей работаем с листом
        # учитываем это при сохранении через product_id=int
        ids_products = list(Products.objects.filter(pk__in=new_productscats).values_list('id', flat=True))
        # Соблюдаем последовательность
        for item in new_productscats:
            if item in ids_products:
                ProductsCats.objects.create(container=container,
                                            cat=row,
                                            product_id=item)

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

    fill_blocks_breadcrumbs(mh_containers, mh, ftype)

    mh.filter_add({'container__id': mh_containers.row.id})
    row = mh.get_row(row_id)
    context = mh.context
    context['is_products'] = is_products
    context['ftype_state'] = get_ftype(ftype)
    context['container'] = object_fields(mh_containers.row)
    context['url_tree'] = mh_containers.url_tree
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
            context['containers'] = LinkContainer.objects.select_related('container').filter(block=row)
            if is_products:
                #context['products'] = ProductsCats.objects.select_related('product').filter(cat=row).values_list('product__id', 'product__name', 'product__code')
                context['products_count'] = ProductsCats.objects.filter(cat=row).aggregate(Count('product'))['product__count']
        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удален' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'
        elif action == 'copy' and row:
            # ---------------------
            # Клонировать контейнер
            # ---------------------
            if mh.permissions['create'] and mh.permissions['edit']:
                parents = '_%s' % row.id
                if row.parents:
                    parents = '%s%s' % (row.parents, parents)
                blocks = mh_containers.row.blocks_set.filter(Q(parents=parents)|Q(parents__startswith='%s_' % parents))
                result = []
                blocks = [block for block in blocks]
                blocks.append(row)
                recursive_fill(blocks, result, parents=row.parents)
                if len(result) != 1:
                    assert False
                new_block = clone_block(result[0], mh_containers.row, parents=result[0].parents)
                clone_url_params = {
                    'ftype': ftype,
                    'action': 'edit',
                    'container_id': mh_containers.row.id,
                    'row_id': new_block.id,
                }
                urla = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']), kwargs=clone_url_params)
                return redirect(urla)
            else:
                context['error'] = 'Недостаточно прав'

    elif request.method == 'POST':
        pass_fields = ('parents', )
        mh.post_vars(pass_fields=pass_fields)

        # Специфическая операция - обновление сео-полей
        # редактируем, но прав нет, но есть сео-права
        seo_perms = (row and row.container.state == 1 and mh.permissions.get('seo_fields') == True)
        if action == 'edit' and not mh.permissions['edit'] and seo_perms:
            context['success'] = 'Данные успешно записаны'
            block_fields = object_fields(Blocks())
            pass_fields = [field for field in block_fields if not field in ('title', 'description', 'keywords')]
            mh.post_vars(pass_fields=pass_fields)
            mh.save_row()

        elif action == 'create' or (action == 'edit' and row):
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
            # Записываем линковки к пункту меню
            update_linkcontainer(request, container, mh.row)
            # Записываем привязки товаров к рубрике
            update_productscats(request, container, mh.row)
        # --------------------
        # Загрузка изображения
        # --------------------
        elif action == 'img' and request.FILES:
            mh.uploads()

    if mh.row:
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['row']['folder'] = mh.row.get_folder()
        context['row']['container_name'] = mh_containers.row.name
        context['redirect'] = mh.get_url_edit()

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

def search_blocks(request, *args, **kwargs):
    """Поиск блоков
       Параметры GET для поиска:
           :param without_templates: Без шаблонов state__in=(99,100)
           :param without_menus: Без менюшек state=1
           :param without_main: Без контента для всех страничек state=2
           :param with_images: Только с изображениями
           :param only_templates: Только шаблоны state__in=(99,100)
           :param only_cats: Только рубрики state=7
           :param only_menus: Только менюшки state=1
    """
    result = {'results': []}

    mh = ModelHelper(Blocks, request)

    # Исключение из поиска определенных типов контейнеров
    without_templates = request.GET.get('without_templates')
    if without_templates:
        mh.exclude_add(Q(container__state__in=(99, 100)))
    without_menus = request.GET.get('without_menus')
    if without_menus:
        mh.exclude_add(Q(container__state=1))
    without_main = request.GET.get('without_main')
    if without_main:
        mh.exclude_add(Q(container__state=2))
    only_templates = request.GET.get('only_templates')
    if only_templates:
        mh.filter_add(Q(container__state__in=(99, 100)))
    only_cats = request.GET.get('only_cats')
    if only_cats:
        mh.filter_add(Q(container__state=7))
    only_menus = request.GET.get('only_menus')
    if only_menus:
        mh.filter_add(Q(container__state=1))
    with_images = request.GET.get('with_images')
    if with_images:
        mh.filter_add(Q(img__isnull=False))
    filters = [cond for cond in request.GET.keys() if cond.startswith('filter__')]
    for key in filters:
        cond = request.GET.get(key)
        mh.filter_add(Q(**{key.replace('filter__', ''): cond}))

    mh_vars = blocks_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)

    mh.search_fields = ('id', 'name', 'tag', 'container__name', 'container__tag')
    mh.select_related_add('container')
    rows = mh.standard_show()

    # Родительские блоки
    all_ids_parents = []
    ids_parents = {}
    ids_rows = {row.id: row for row in rows}
    for row_id, row in ids_rows.items():
        if not row.parents:
            continue
        ids_parents[row_id] = [int(parent) for parent in row.parents.split('_') if parent]
        all_ids_parents += ids_parents[row_id]
    parents = Blocks.objects.filter(pk__in=all_ids_parents)
    all_parents = {parent.id: parent for parent in parents}
    for row in rows:
        if not row.id in ids_parents:
            continue
        row.parents_arr = []
        for parent in ids_parents[row.id]:
            if parent in all_parents:
                row.parents_arr.append(all_parents[parent])

    for row in rows:
        parents = ''
        if hasattr(row, 'parents_arr'):
            for parent in row.parents_arr:
                parents += ' > %s #%s' % (parent.name, parent.id)
        name = '%s%s > %s #%s' % (row.container.name, parents, row.name, row.id)
        if row.tag:
            name += ' (%s)' % (row.tag, )
        # При поиске по шаблону отдаем тег, а не id в поле id
        if only_templates:
            result['results'].append({'text': name, 'id': row.tag})
        else:
            result['results'].append({'text': name, 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}

    return JsonResponse(result, safe=False)

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
    # В иерархии нужны права именно блоков,
    # а не контейнеров
    mh.get_permissions(Blocks)

    if request.method == 'GET':
        operation = request.GET.get('operation')
        # Сообщение о нехватке прав
        if operation in ('rename_node', 'move_node') and not mh.permissions['edit']:
            result = {'error': 'Недостаточно прав'}
        elif operation == 'drop_node' and not mh.permissions['drop']:
            result = {'error': 'Недостаточно прав'}
        # Выбрать узел
        if operation == 'select_node':
            node_id = int(request.GET.get('node_id'), 0)
            node = Blocks.objects.filter(container=container, pk=node_id).first()
            if node:
                domains = []
                if settings.IS_DOMAINS:
                    domains = get_domains()
                    get_translate([node], domains)
                result = object_fields(node)
                result['folder'] = node.get_folder()
                result['thumb'] = node.thumb()
                result['imagine'] = node.imagine()
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
                # Линковки для пункта меню / каталога
                if container.state in (1, 7) and node.state == 4:
                    result['linkcontainer'] = []
                    linkcontainer = LinkContainer.objects.select_related('container').filter(block=node).order_by('position')
                    for item in linkcontainer:
                        result['linkcontainer'].append({
                            'name': item.container.name,
                            'id': item.container.id,
                            'tag': item.container.tag,
                        })

                # Привязка товаров к рубрикам
                # лучше tabulator таблицей пользоваться,
                # а через select2 добавлять, т/к слишком много
                # товаров может быть привязано - медленно
                if is_products:
                    result['products_count'] = ProductsCats.objects.filter(cat=node).aggregate(Count('product'))['product__count']
                #    result['products'] = [
                #        {
                #            'name': product[1],
                #            'id': product[0],
                #            'tag': product[2],
                #        }
                #        for product in ProductsCats.objects.select_related('product').filter(cat=node).values_list('product__id', 'product__name', 'product__code')
                #    ]
                result = {'row': result}
                if domains:
                    result['domains'] = {domain['pk']: domain['translations'] for domain in domains}
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
                'a_attr': {
                    'href': 'javascript:void(0);',
                },
            }]
        # Получить каталог с lazy загрузкой
        elif operation == 'get_children_lazy' and mh.permissions['view']:
            node_id = request.GET.get('node_id')
            if not node_id:
                result = [{
                    'id': 'container_%s' % (container.id, ),
                    'text': container.name,
                    'state': {'opened': True, 'selected': False, 'disabled': True},
                    #'children': data,
                    'children': True,
                    'a_attr': {
                        'href': 'javascript:void(0);',
                    },
                }]
            else:
                if node_id.isdigit():
                    menus = Blocks.objects.filter(container=container, parents__endswith='_%s' % node_id).order_by('position')
                else:
                    menus = Blocks.objects.filter(container=container, parents='').order_by('position')
                data = []
                prepare_jstree(data, menus, lazy=True)
                result = data

        # Создание / редактирование блока
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
                state = 1
                if container.state in (1, 7): # flatmenu/flatcat
                    state = 4
                menu = Blocks(parents=parents_str,
                              container=container, state=state)
            menu.name = node_name
            menu.save()
            # Записываем линковки к пункту меню
            update_linkcontainer(request, container, menu)
            # Записываем привязки товаров к рубрике
            update_productscats(request, container, menu)
            result = {
                'success': True,
                'id': menu.id,
            }
        elif operation == 'drop_node' and mh.permissions['drop']:
            node_id = request.GET.get('node_id')
            menu = Blocks.objects.filter(pk=node_id, container=container).first()
            if menu:
                parents_str = '_%s' % (menu.id, )
                if menu.parents:
                    parents_str = '%s_%s' % (menu.parents, menu.id)
                children = Blocks.objects.filter(Q(parents=parents_str)|Q(parents__startswith='%s_' % (parents_str, )))
                # Только без вложенности
                if not children:
                    for child in children:
                        child.delete()
                    menu.delete()
                    result = {'success': True}
                else:
                    result = {'error': True}
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

        if request.GET['operation'] == 'search':
            q = request.GET['str']
            cats = []
            ids = []
            result = []
            if q and len(q) >= 2:
                ids = jstree_search(q, container)

            if ids:
                cats = Blocks.objects.filter(pk__in=ids)
                for cat in cats:
                    if cat.parents:
                        parents = cat.parents.split('_')
                        for parent in parents:
                            if parent and not parent == '1':
                                if not parent in result:
                                    result.append(parent)
                if result:
                    result.insert(0, 'container_%s' % container.id)

    return JsonResponse(result, safe=False)

def jstree_search(q: str, container):
    """Поиск id блоков по q для jstree ajax search
       :param q: поисковая фраза
       :param container: родительский контейнер
    """
    q_array = q.split(' ')
    cond = Q()

    for item in q_array:
        if not item:
            continue
        cond.add(Q(Q(name__icontains=item)|Q(tag__icontains=item)), Q.AND)
    query = Blocks.objects.filter(container=container)

    if q.isdigit():
        search_blocks = query.filter(Q(cond) | Q(pk=q)).values_list('id', flat=True)
    else:
        search_blocks = query.filter(cond).values_list('id', flat=True)
    return [x for x in search_blocks]


def head_fill(block, q_string):
    """Заполнение мета-тегов и заголовка в q_string"""
    if not block.state == 4 or not isinstance(block, Blocks):
        return
    for field in ('title', 'keywords', 'description'):
        value = getattr(block, field)
        if value:
            q_string[field] = value

def SearchLink(q_string: dict = None,
               request = None,
               mcap: dict = None,
               cache_time: int = 60):
    """Страница поиска неслужебных ссылок (статич.)
       mcap - Main (tag) Content for All Pages
       Можно передать в mcap список по умолчанию
       выводимых контейнеров, затем в шаблоне
       выводить их куда следует по одному через page

       это mcap
       containers = {
           'social_sidebar': None,
           'news_sidebar': None,
           'subscribe': None,
           'article_sidebar': None,
       }
    """
    is_static_path = False
    path_info = '/'

    if not mcap and isinstance(mcap, dict):
        mcap['main'] = None

    if request:
        path_info = request.META['PATH_INFO']

        if '/media/' in path_info or '/static/' in path_info:
            is_static_path = True

        link_with_params = path_info
        query_string = request.META['QUERY_STRING']
        if query_string:
            link_with_params += '?%s' % (query_string, )

        hashed_link = serp_hash(link_with_params.encode('utf-8'))
        cache_var = '%s_%s' % (hashed_link, settings.PROJECT_NAME)
        # ------------------------
        # Если сайт мультиязычный,
        # то кэш нужен на домен
        # ------------------------
        if settings.IS_DOMAINS:
            domain = get_domain(request)
            if domain:
                cache_var = '%s%s' % (domain['pk'], cache_var)

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
                for k, v in inCache['mcap'].items():
                    mcap[k] = v
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

    container_all_pages = Containers.objects.filter(tag__in=mcap.keys(), is_active=True).exclude(state__in=(99, 100))
    blocks = []

    # ------------------------------------------------------
    # Корректировка запроса, если в mcap запросили айдишники
    # это предпросмотр, выбираем только main + pk
    # ------------------------------------------------------
    intas = [digit for digit in mcap.keys() if isinstance(digit, int)] # long?

    if intas:
        container_all_pages = Containers.objects.filter(Q(tag='main')|Q(pk__in=intas))
    else:
        blocks = Blocks.objects.filter(link=path_info, state=4, is_active=True)

    for cap in container_all_pages:
        ids_containers[cap.id] = {
            'container': cap,
            'blocks': [],
            'tags': {},
            'products': [],
            'position': cap.position,
        }
        all_containers.append(cap) # Для перевода

    containers = []
    # Найдем менюшку -
    # найдем привязанные контейнеры
    blocks_with_content = [block for block in blocks]
    if blocks_with_content:
        containers = LinkContainer.objects.select_related('container').filter(block__in=blocks_with_content)
        if containers:
            blocks_dict = {block.id: block for block in blocks_with_content}
            for container in containers:
                if container.block_id in blocks_dict:
                    block_with_content = blocks_dict[container.block_id]
                    all_blocks.append(block_with_content)
                    break
        if not block_with_content and blocks:
            block_with_content = blocks[0]
            all_blocks.append(block_with_content) # Для перевода
        block_with_content.tags = []

    if containers:
        for container in containers:
            all_containers.append(container.container) # Для перевода
            ids_containers[container.container.id] = {
                'container': container.container,
                'blocks': [],
                'tags': {},
                'products': [],
                'position': container.position,
            }
            if container.container.tag:
                block_with_content.tags.append(container.container.tag)

    # Хлебные крошки выше текущего блока
    if block_with_content and block_with_content.parents:
        block_with_content.breadcrumbs = []
        parents = [int(parent) for parent in block_with_content.parents.split('_') if parent]
        superblocks = Blocks.objects.filter(pk__in=parents)
        all_blocks += superblocks
        ids_superblocks = {superblock.id: superblock for superblock in superblocks}
        for parent in parents:
            if parent in ids_superblocks:
                block_with_content.breadcrumbs.append(ids_superblocks[parent])

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

def blocks_contains_prices(ids_containers: dict, blocks: dict):
    """Заполняем контейнеры с товарами/услугами"""
    have_prices = []
    blocks_products = {}
    if not ids_containers or not is_products:
        return

    # Как отличать служебный каталог, где нельзя к блокам-рубрикам
    # вытаскивать товары - т/к их может быть много
    # от каталога-шаблона (м/б проверять есть ли такой шаблон?)
    # Тупо - если мы здесь и выводим именно через flatcontent,
    # значит, надо все-таки подливать товары - пока так

    # Обрабатываем контейнеры с товарами
    products = ProductsCats.objects.select_related('product').filter(container__in=ids_containers.keys())
    ids_products = {x.product.id: x.product for x in products}

    # Разные типы цен
    get_costs_types(ids_products.values())

    # Находим скидки для всех товаров
    #shopper = None
    #if request:
    #    shopper = request.session.get('shopper', None)
    #search_disconts_for_prices(ids_prices, shopper)

    # Рейтинги товаров/услуг
    #if is_reviews:
    #    get_objects_ratings(ids_prices, 'price.Products')

    # Переводим товары/услуги
    #if settings.IS_DOMAINS and request:
    #    ct_prices = ContentType.objects.get_for_model(Products)
    #    get_translations(ids_prices.values(), ct_prices)
    #    translate_rows(ids_prices.values(), request)

    # Для сохранения сортировки идем по products
    for item in products:
        product = ids_products[item.product.id]
        if item.cat_id:
            if not item.cat_id in blocks_products:
                blocks_products[item.cat_id] = []
            blocks_products[item.cat_id].append(product)
        else:
            if item.container_id in ids_containers:
                ids_containers[item.container_id]['products'].append(product)
            if not item.container_id in have_prices:
                have_prices.append(item.container_id)

    # Ищем скидки/акции по товарам/услугам
    #if have_prices:
    #    disconts = Disconts.objects.filter(container__in=have_prices)
    #    for discont in disconts:
    #        # Добавлять надо к самому контейнеру
    #        for key, value in ids_containers.items():
    #            container_id = value['container'].id
    #            if discont.container_id == container_id:
    #                value['container'].discont = discont
    #                break

    for block in blocks:
        if block.id in blocks_products:
            block.products = blocks_products[block.id]

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
           "position":container.position
       }"""

    blocks = Blocks.objects.filter(container__in=ids_containers.keys(), is_active=True)

    blocks_contains_prices(ids_containers, blocks)

    for block in blocks:
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
        cur_tag = value['container'].tag
        if cur_tag == 'main' or cur_tag in mcap:
            mcap[cur_tag] = value
        else:
            pk = value['container'].id
            mcap[pk] = value

    if block_with_content:
        block_with_content.containers = sorted(ids_containers.values(), key=lambda x: x['position'])

    # Переводим блоки/контейнеры
    # Если выбран не основной домен
    if settings.IS_DOMAINS and request:
        domains = get_domains()
        domain = get_domain(request, domains)
        if domain:
            domains = [domain]
            get_translate(all_blocks, domains)
            translate_rows(all_blocks, domain)
            get_translate(all_containers, domains)
            translate_rows(all_containers, domain)

    if block_with_content:
        head_fill(block_with_content, q_string)

def MainStatPage(request, path: str = None, tags: list = None):
    """Статическая страничка (или 404)
       :param path: путь (ссылка)
       :param tags: теги для доп контейнеров"""
    breadcrumbs = []
    q_string = {}
    containers = {}
    if not path:
        path = request.META['PATH_INFO']
    else:
        if not path.startswith('/'):
            path = '/%s' % path

    if path.endswith('.html'):
        page = SearchLink(q_string, request, containers)
        template = 'flatcontent_static.html'
        return render(request, template, {'page':page, 'containers': containers})
    # ----------------------------------------
    # Проверяем оканчивается ли на слеш линка,
    # если не оканчивается - редиректим
    # ----------------------------------------
    if not path.endswith('/'):
        path += '/'
        return redirect(path)
    page = SearchLink(q_string, request, containers)
    if page:
        if hasattr(page, 'breadcrumbs') and isinstance(page.breadcrumbs, list):
            breadcrumbs += page.breadcrumbs
        breadcrumbs.append({'name': page.name, 'link': page.link})
        template = 'web/main_stat.html'
        return render(request, template, {
            'page': page,
            'containers': containers,
            'breadcrumbs': breadcrumbs,
            'q_string': q_string,
        })

    breadcrumbs.append({'name': 'Страничка не найдена', 'link': '/'})
    page_not_found = '404 - Page not found'
    q_string = {
        'title': page_not_found,
        'description': page_not_found,
    }
    resp = render(request, '404.html', {
        'containers': containers,
        'q_string': q_string,
        'breadcrumbs': breadcrumbs,
        'page': Blocks(name=page_not_found),
    })
    resp.status_code = 404
    return resp
