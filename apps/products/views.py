# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper, ModelHelper
from apps.main_functions.api_helper import ApiHelper, XlsxHelper
from apps.main_functions.string_parser import analyze_digit
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view,
                                              special_model_vars, )

from apps.flatcontent.flatcat import get_filters_for_cat
from apps.flatcontent.models import Containers, Blocks
from .models import (Products,
                     ProductsCats,
                     ProductsPhotos,
                     Property,
                     PropertiesValues,
                     ProductsProperties,
                     CostsTypes,
                     Costs,
                     CURRENCY_CHOICES, )

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
    'search_result_format': ('{}, id={}, код={}', 'name id code'),
}

def api(request, action: str = 'products'):
    """Апи-метод для получения всех данных"""
    if action == 'props':
        result = ApiHelper(request, props_vars, CUR_APP)
    elif action == 'pvalues':
        result = ApiHelper(request, pvalues_vars, CUR_APP)
    else:
        result = ApiHelper(request, products_vars, CUR_APP)
    return result

def import_xlsx(request, action: str = 'vocabulary'):
    """Апи-метод для сохранения данных из excel-файла
                     удаления данных по excel-файлу
       :param request: HttpRequest
       :param action: какую модель использовать
    """
    #if action == 'promotion':
    #    result = XlsxHelper(request, vocabulary_vars, CUR_APP)
    result = XlsxHelper(request, products_vars, CUR_APP,
                        cond_fields = ['code'])
    return result

@login_required
def show_products(request, *args, **kwargs):
    """Вывод товаров"""
    extra_vars = {
        'import_xlsx_url': reverse('%s:%s' % (CUR_APP, 'import_xlsx'),
                                   kwargs={'action': 'products'}),
    }
    return show_view(request,
                     model_vars = products_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

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
    if not 'row' in context:
        context['row'] = object_fields(product)
    context['row']['is_gallery'] = True

@login_required
def edit_product(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование товара"""
    mh_vars = products_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    row = mh.get_row(row_id)
    context = mh.context

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
            context['props'] = row.productsproperties_set.select_related('prop', 'prop__prop').all()
            context['photos'] = row.productsphotos_set.all()
            context['seo'] = row.get_seo()
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
            # SEO
            seo = {k: request.POST.get(k) for k in ('seo_title', 'seo_description', 'seo_keywords')}
            mh.row.fill_seo(**seo)

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
        # Чтобы не перезаписывать инфу о загруженном фото в галерею
        if not 'row' in context:
            context['row'] = object_fields(mh.row)
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['row']['link'] = mh.row.link()
        context['redirect'] = mh.get_url_edit()
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
    """Поиск товаров
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = products_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

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
    'custom_model_permissions': Products,
}

@login_required
def show_photos(request, *args, **kwargs):
    """Вывод фото для товаров/услуг"""
    return show_view(request,
                     model_vars = photos_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_photo(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование фото товара"""
    mh_vars = photos_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.get_permissions(Products) # Права от товаров/услуг
    row = mh.get_row(row_id)
    context = mh.context
    special_model_vars(mh, mh_vars, context)
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
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.get_url_edit()
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

props_vars = {
    'singular_obj': 'Свойство товара',
    'plural_obj': 'Свойства товаров',
    'rp_singular_obj': 'свойства товара',
    'rp_plural_obj': 'свойств товаров',
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
    'custom_model_permissions': Products,
}

@login_required
def show_props(request, *args, **kwargs):
    """Вывод свойств для товаров/услуг"""
    return show_view(request,
                     model_vars = props_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_prop(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование свойства для товара"""
    mh_vars = props_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.get_permissions(Products) # Права от товаров/услуг
    row = mh.get_row(row_id)
    context = mh.context
    special_model_vars(mh, mh_vars, context)

    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    if request.method == 'GET':
        if action in ('create', 'edit'):
            context['ptypes'] = Property.ptype_choices
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
            context['pvalues'] = [object_fields(prop, pass_fields=('prop', ))
                for prop in mh.row.propertiesvalues_set.all()]
            context['pvalues_ends'] = analyze_digit(len(context['pvalues']), end = ('запись', 'записей', 'записи'))

        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удалено' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'
        elif action == 'pvalue' and row:
            result = {}
            if mh.permissions['drop']:
                drop_pvalue = request.GET.get('drop_pvalue')
                if drop_pvalue:
                    result['drop_pvalue'] = drop_pvalue
                    pvalue = PropertiesValues.objects.filter(prop=row, pk=drop_pvalue).first()
                    if pvalue:
                        pvalue.delete()
                result['success'] = 'Значение свойства удалено'
            else:
                result['error'] = 'Недостаточно прав'
            return JsonResponse(result, safe=False)

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
        elif action == 'pvalue' and row:
            result = {}
            pk = request.POST.get('id')
            value = request.POST.get('value')
            is_active = request.POST.get('is_active')
            prop = PropertiesValues(prop=row)
            if pk:
                analog = PropertiesValues.objects.filter(pk=pk, prop=row).first()
                if analog:
                    prop = analog
            prop.str_value = value
            prop.is_active = True if is_active else False

            if mh.permissions['edit']:
                result['success'] = 'Данные успешно записаны'
                prop.save()
            else:
                result['error'] = 'Недостаточно прав'
            result['row'] = object_fields(prop, pass_fields=('prop', ))
            return JsonResponse(result, safe=False)
    if mh.row:
        kwargs = {'action': 'pvalue', 'row_id': mh.row.id}
        context['url_edit_pvalue'] = reverse('%s:%s' % (CUR_APP, 'edit_prop'),
                                             kwargs=kwargs)
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.get_url_edit()
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

def search_props(request, *args, **kwargs):
    """Поиск свойств
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = props_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

pvalues_vars = {
    'singular_obj': 'Значение свойства',
    'plural_obj': 'Значения свойства',
    'rp_singular_obj': 'значения свойства товара',
    'rp_plural_obj': 'значений свойств товара',
    'template_prefix': 'pvalues_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'products',
    'submenu': 'pvalues',
    'show_urla': 'show_pvalues',
    #'create_urla': 'create_pvalue',
    #'edit_urla': 'edit_pvalue',
    'model': PropertiesValues,
    'custom_model_permissions': Products,
}

@login_required
def show_pvalues(request, *args, **kwargs):
    """Вывод значений свойств для товаров/услуг"""
    return show_view(request,
                     model_vars = pvalues_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def pvalues_positions(request, *args, **kwargs):
    """Изменение позиций значений свойств в свойстве"""
    result = {}
    mh_vars = pvalues_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    mh.get_permissions(Products) # Права от товаров/услуг
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_pvalues(request, *args, **kwargs):
    """Поиск значений свойств
       :param request: HttpRequest
    """
    result = {'results': []}
    mh = ModelHelper(PropertiesValues, request)
    mh_vars = pvalues_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)
    mh.search_fields = ('id', 'str_value')

    prop_id = request.GET.get('prop_id')
    if prop_id:
        mh.filter_add(Q(prop__id=prop_id))
    order_by = request.GET.get('order_by')
    if order_by:
        for item in order_by.split(','):
            mh.order_by_add(item.strip())

    rows = mh.standard_show()
    for row in rows:
        result['results'].append({'text': row.str_value, 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}
    return JsonResponse(result, safe=False)

products_pvalues_vars = {
    'singular_obj': 'Значение свойства товара',
    'plural_obj': 'Значения свойства товара',
    'rp_singular_obj': 'значения свойства товара',
    'rp_plural_obj': 'значений свойств товара',
    'template_prefix': 'products_pvalues_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'products',
    'submenu': 'products_pvalues',
    'show_urla': 'show_product_pvalues',
    'create_urla': 'create_product_pvalue',
    'edit_urla': 'edit_product_pvalue',
    'model': ProductsProperties,
    'custom_model_permissions': Products,
}

@login_required
def show_product_pvalues(request, *args, **kwargs):
    """Вывод привязанных свойств для товаров/услуг"""
    return show_view(request,
                     model_vars = products_pvalues_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_product_pvalue(request, action: str, row_id: int = None, *args, **kwargs):
    """Добавление/удаление свойства к товару
       Аяксовый метод
       :param request: HttpRequest
       :param action: действие
       :param row_id: ид ProductsProperties
    """
    result = {}
    mh_vars = products_pvalues_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.get_permissions(Products) # Права от товаров/услуг
    context = mh.context
    row = mh.get_row(row_id)
    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))

    if request.method == 'GET':
        if action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удалено' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'
    elif request.method == 'POST':
        # Нетрадиционное сохранение
        # Принимаем prop, записываем линковку
        prop = None
        prop_id = request.POST.get('prop')
        if prop_id:
            prop = PropertiesValues.objects.filter(pk=prop_id).first()
        product = None
        product_id = request.POST.get('product')
        if product_id:
            product = Products.objects.filter(pk=product_id).first()

        if action == 'create' or (action == 'edit' and row):
            if action == 'create' and product and prop:
                if mh.permissions['create'] and prop:
                    row = ProductsProperties.objects.create(
                        product=product,
                        prop = prop,
                    )
                    context['success'] = 'Данные успешно записаны'
                    context['row'] = {'id': row.id}
                else:
                    context['error'] = 'Недостаточно прав'
            if action == 'edit' and row and prop and product and product.id == row.product_id:
                if mh.permissions['edit']:
                    row.prop = prop
                    row.save()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'

    return JsonResponse(context, safe=False)

costs_vars = {
    'singular_obj': 'Тип цены',
    'plural_obj': 'Типы цен',
    'rp_singular_obj': 'типа цены',
    'rp_plural_obj': 'типов цен',
    'template_prefix': 'costs_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'products',
    'submenu': 'costs',
    'show_urla': 'show_costs',
    'create_urla': 'create_cost',
    'edit_urla': 'edit_cost',
    'model': CostsTypes,
    'custom_model_permissions': Products,
}

@login_required
def show_costs(request, *args, **kwargs):
    """Вывод типов цен"""
    return show_view(request,
                     model_vars = costs_vars,
                     cur_app = CUR_APP,
                     extra_vars = None, )

@login_required
def edit_cost(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование типа цены"""
    extra_vars = {'currency_choices': CURRENCY_CHOICES}
    return edit_view(request,
                     model_vars = costs_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = extra_vars, )

def search_costs(request, *args, **kwargs):
    """Поиск типов цен
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = costs_vars,
                       cur_app = CUR_APP,
                       sfields = None, )

@login_required
def costs_positions(request, *args, **kwargs):
    """Изменение позиций типов цен"""
    result = {}
    mh_vars = costs_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

products_cats_vars = {
    'singular_obj': 'Товар в рубрике',
    'plural_obj': 'Товары в рубриках',
    'rp_singular_obj': 'товара из рубрики',
    'rp_plural_obj': 'товаров из рубрик',
    'template_prefix': 'products_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'products',
    'submenu': 'products',
    'show_urla': 'show_cats_products',
    'create_urla': 'create_cat_product',
    'edit_urla': 'edit_cat_product',
    'model': ProductsCats,
    'custom_model_permissions': Products,
}

@login_required
def show_cats_products(request, *args, **kwargs):
    """Вывод привязок товаров к рубрикам"""
    mh_vars = products_cats_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('product')
    #mh.select_related_add('cat')
    context = mh.context
    # Условие под выборку определенной категории
    if request.method == 'GET':
        cat_id = request.GET.get('cat_id')
        if cat_id:
            try:
                cat_id = int(cat_id)
            except ValueError:
                logger.exception('cat_id not int')
                cat_id = None
            if cat_id:
                cat = Blocks.objects.filter(pk=cat_id).first()
                if cat:
                    mh.filter_add(Q(cat=cat))
    special_model_vars(mh, mh_vars, context)
    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        only_fields = (
            'id',
            'product__id',
            'product__name',
            'product__code',
            #'cat__name'
        )
        rows = mh.standard_show(only_fields=only_fields)
        result = []
        fk_keys = {
            'product': ('id', 'name', 'code'),
            #'cat': ('name', ),
        }
        for row in rows:
            item = object_fields(row,
                                 only_fields=only_fields,
                                 fk_only_keys=fk_keys, )
            item['actions'] = row.id
            #item['folder'] = row.get_folder()
            #item['thumb'] = row.thumb()
            #item['imagine'] = row.imagine()
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
def edit_cat_product(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование линковки товара к категории"""
    return edit_view(request,
                     model_vars = products_cats_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

def facet_filters(request, cat_id):
    """Получение фасетных фильтров
       :param cat_id: ид категории
    """
    result = get_filters_for_cat(cat_id)
    return JsonResponse(result, safe=False)
