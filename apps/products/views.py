# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper, ModelHelper
from apps.main_functions.tabulator import tabulator_filters_and_sorters
from apps.main_functions.string_parser import analyze_digit

from apps.flatcontent.models import Containers, Blocks
from .models import Products, ProductsCats, ProductsPhotos, Property

CUR_APP = 'products'
products_vars = {
    'singular_obj': 'Товар',
    'plural_obj': 'Товары',
    'rp_singular_obj': 'товара',
    'rp_plural_obj': 'товаров',
    'template_prefix': 'products_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'products',
    'submenu': 'products',
    'show_urla': 'show_products',
    'create_urla': 'create_product',
    'edit_urla': 'edit_product',
    'model': Products,
}

def api(request, action: str = 'products_vars'):
    """Апи-метод для получения всех данных"""
    mh_vars = products_vars.copy()
    #if action == 'products_vars':
    #    mh_vars = products_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    # Принудительные права на просмотр
    mh.permissions['view'] = True
    context = mh.context
    rows = mh.standard_show()
    result = []
    for row in rows:
        item = object_fields(row)
        item['folder'] = row.get_folder()
        result.append(item)
    result = {'data': result,
              'last_page': mh.raw_paginator['total_pages'],
              'total_records': mh.raw_paginator['total_records'],
              'cur_page': mh.raw_paginator['cur_page'],
              'by': mh.raw_paginator['by'], }
    return JsonResponse(result, safe=False)

@login_required
def show_products(request, *args, **kwargs):
    """Вывод товаров"""
    mh_vars = products_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    context = mh.context
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
            item['folder'] = row.get_folder()
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
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

def add_photo2gallery(photo, product, context):
    """Добавить фото к товару/услугу в галерею
       :param photo: ссылка или request.FILES.get('img')
       :param product: Товар/услуга
       :param context: результирующая информация о загрузке
    """
    new_photo = ProductsPhotos.objects.create(product=product)
    new_photo.upload_img(photo)
    context['photo'] = object_fields(new_photo, pass_fields=('product', ))
    context['photo']['folder'] = new_photo.get_folder()
    context['photo']['thumb'] = new_photo.thumb()
    context['photo']['imagine'] = new_photo.imagine()
    context['row']['is_gallery'] = True

@login_required
def edit_product(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование товара"""
    mh_vars = products_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    context = mh.context
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
            context['cats'] = row.productscats_set.select_related('cat', 'cat__container').all()
            context['photos'] = row.productsphotos_set.all()
        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удален' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'
    elif request.method == 'POST':
        pass_fields = []
        if request.POST.get('2gallery'):
            pass_fields.append('grab_img_by_url')
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
            # Сохраняем категории для товара
            ids_cats = request.POST.getlist('cats')
            mh.row.productscats_set.all().delete()
            if ids_cats:
                cats = Blocks.objects.filter(pk__in=ids_cats)
                for cat in cats:
                    ProductsCats.objects.create(product=mh.row, cat=cat)

            # Загрузка в галерею,
            # причем только по ссылке, т/к
            # обработчик request.FILES работает через action='img'
            if request.POST.get('2gallery') and request.POST.get('grab_img_by_url') and mh.row:
                context['row'] = object_fields(mh.row)
                add_photo2gallery(request.POST.get('grab_img_by_url'), mh.row, context)

        elif action == 'img' and request.FILES:
            # Загрузка в галерею
            if request.POST.get('2gallery'):
                add_photo2gallery(request.FILES.get('img'), mh.row, context)
                return JsonResponse(context, safe=False)
            else:
                mh.uploads()
    if mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        # Чтобы не перезаписывать инфу о загруженном фото в галерею
        if not 'row' in context:
            context['row'] = object_fields(mh.row)
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.url_edit
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def products_positions(request, *args, **kwargs):
    """Изменение позиций товаров"""
    result = {}
    mh_vars = products_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_products(request, *args, **kwargs):
    """Поиск объектов"""
    result = {'results': []}
    mh = ModelHelper(Products, request)
    mh_vars = products_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)
    mh.search_fields = ('id', 'name')
    rows = mh.standard_show()
    for row in rows:
        name = row.name
        if row.code:
            name += ' (%s)' % (row.code, )
        name += ' #%s' % (row.id, )
        result['results'].append({'text': name, 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}
    return JsonResponse(result, safe=False)

photos_vars = {
    'singular_obj': 'Фото товара',
    'plural_obj': 'Галерея товара',
    'rp_singular_obj': 'фото товара',
    'rp_plural_obj': 'галереи товара',
    'template_prefix': 'photos_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'products',
    'submenu': 'photos',
    'show_urla': 'show_photos',
    #'create_urla': 'create_photo',
    #'edit_urla': 'edit_photo',
    'model': ProductsPhotos,
}

@login_required
def show_photos(request, *args, **kwargs):
    """Вывод фото для товаров/услуг"""
    mh_vars = photos_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.get_permissions(Products) # Права от товаров/услуг
    context = mh.context
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
            item['folder'] = row.get_folder()
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
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
def edit_photo(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование фото товара"""
    mh_vars = photos_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.get_permissions(Products) # Права от товаров/услуг
    context = mh.context
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
                context['success'] = '%s удалено' % (mh.singular_obj, )
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
        elif action == 'img' and request.FILES:
            mh.uploads()
    if mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.url_edit
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)


props_vars = {
    'singular_obj': 'Свойство товара',
    'plural_obj': 'Свойства товара',
    'rp_singular_obj': 'свойства товара',
    'rp_plural_obj': 'свойств товара',
    'template_prefix': 'props_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'products',
    'submenu': 'props',
    'show_urla': 'show_props',
    'create_urla': 'create_prop',
    'edit_urla': 'edit_prop',
    'model': Property,
}

@login_required
def show_props(request, *args, **kwargs):
    """Вывод свойств для товаров/услуг"""
    mh_vars = props_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.get_permissions(Products) # Права от товаров/услуг
    context = mh.context
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
            item['folder'] = row.get_folder()
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
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
def edit_prop(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование свойства для товара"""
    mh_vars = props_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.get_permissions(Products) # Права от товаров/услуг
    context = mh.context
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
            # Значения свойства
            context['pvalues'] = mh.row.propertiesvalues_set.all().values('str_value', 'digit_value')
            context['pvalues_ends'] = analyze_digit(len(context['pvalues']), end = ('запись', 'записей', 'записи'))

        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удалено' % (mh.singular_obj, )
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

        elif action == 'img' and request.FILES:
            mh.uploads()
    if mh.row:
        mh.url_edit = reverse('%s:%s' % (CUR_APP, mh_vars['edit_urla']),
                              kwargs={'action': 'edit', 'row_id': mh.row.id})
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.url_edit
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)