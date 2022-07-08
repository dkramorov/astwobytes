# -*- coding:utf-8 -*-
import os
import json
import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q, Count

from apps.main_functions.files import check_path, copy_file
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import (create_model_helper,
                                              get_user_permissions,
                                              ModelHelper,
                                              tabulator_filters_and_sorters, )
from apps.main_functions.api_helper import ApiHelper, XlsxHelper
from apps.main_functions.string_parser import analyze_digit, translit
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view,
                                              special_model_vars, )

from apps.flatcontent.models import Containers, Blocks
from apps.products.models import (
    Products,
    ProductsCats,
    ProductsPhotos,
    Property,
    PropertiesValues,
    ProductsProperties,
    CostsTypes,
    Costs,
    CURRENCY_CHOICES,
)

from apps.products.strategy import get_search_strategy

logger = logging.getLogger('main')

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

def get_products_cats(ids_products: dict, tag: str = None):
    """Получение категорий по списку товаров (пока без хлебных крох)
       :param ids_products: словарь идентификаторов товаров
       :param tag: тег каталога
    """
    cats = ProductsCats.objects.select_related('cat').filter(product__in=ids_products, cat__isnull=False, cat__container__state=7)
    if tag:
        cats = cats.filter(cat__container__tag=tag)
    cats = cats.values('product', 'cat__id', 'cat__link', 'cat__name')

    for cat in cats:
        if not ids_products[cat['product']]:
            ids_products[cat['product']] = []
        ids_products[cat['product']].append({
            'id': cat['cat__id'],
            'link': cat['cat__link'],
            'name': cat['cat__name'],
        })

@login_required
def show_products(request, *args, **kwargs):
    """Вывод товаров"""
    mh_vars = products_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, disable_fas=True)

    filters_and_sorters = tabulator_filters_and_sorters(request)
    for rsorter in filters_and_sorters['sorters']:
        if not rsorter in ('cat', '-cat'):
            mh.order_by_add(rsorter)
    for rfilter in filters_and_sorters['filters']:
        mh.filter_add(rfilter)
    mh.context['fas'] = filters_and_sorters['params']
    # Чтобы получить возможность модифицировать фильтры и сортировщики
    mh.filters_and_sorters = filters_and_sorters

    context = mh.context
    context['import_xlsx_url'] = reverse('%s:%s' % (CUR_APP, 'import_xlsx'),
                                         kwargs={'action': 'products'})
    # Условие под выборку определенной категории
    cat_filter = filters_and_sorters['params'].get('filters', {})
    if 'cat' in cat_filter:
        ids_products = ProductsCats.objects.filter(cat=cat_filter['cat']).values_list('product', flat=True)
        ids_products = list(ids_products)
        mh.filter_add(Q(pk__in = ids_products))

    special_model_vars(mh, mh_vars, context)
    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        only_fields = (
            'id',
            'name',
            'code',
            'price',
            'img',
            'is_active',
            'position',
        )
        # Для переопределения получаемых полей
        if kwargs.get('only_fields') and kwargs['only_fields']:
            only_fields = kwargs['only_fields']

        rows = mh.standard_show(only_fields=only_fields)

        ids_products = {row.id: None for row in rows}
        get_products_cats(ids_products)

        result = []
        for row in rows:
            item = object_fields(row, only_fields=only_fields)
            item['actions'] = row.id
            item['folder'] = row.get_folder()
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
            if ids_products[row.id]:
                item['cat'] = ids_products[row.id]
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
    if not 'row' in context:
        context['row'] = object_fields(product)
    context['row']['is_gallery'] = True

def create_double(product):
    """Создать дубль товара/услуги
       TODO: если несколько цен
       :param product: Product model instance
    """
    pass_fields = ('id', 'created', 'updated', 'position', 'parents', 'code')
    new_product = Products()
    for field in object_fields(product, pass_fields=pass_fields):
       value = getattr(product, field)
       setattr(new_product, field, value)
    code = '%s-DOUBLE' % product.code
    new_product.code = code
    new_product.save()

    # Изображение
    if product.img:
        imga = os.path.join(product.get_folder(), product.img)
        if not check_path(imga):
            new_imga = os.path.join(new_product.get_folder(), product.img)
            copy_file(imga, new_imga)

    # Галерея
    gallery = ProductsPhotos.objects.filter(product=product).order_by('position')
    for photo in gallery:
        imga = os.path.join(photo.get_folder(), photo.img)
        if not check_path(imga):
            params = {
                'name': photo.name,
                'product': new_product,
                'img': photo.img,
            }
            new_photo = ProductsPhotos.objects.create(**params)
            new_imga = os.path.join(new_photo.get_folder(), photo.img)
            copy_file(imga, new_imga)

    # Рубрики (TODO: container?)
    cats = ProductsCats.objects.select_related('cat').filter(product=product)
    for cat in cats:
        ProductsCats.objects.create(product=new_product, cat=cat.cat)

    # SEO
    seo_block = product.get_seo()
    if seo_block:
        seo = {
            'seo_title': seo_block.title,
            'seo_description': seo_block.description,
            'seo_keywords': seo_block.keywords,
        }
        new_product.fill_seo(**seo)

    # Свойства товара
    props = ProductsProperties.objects.select_related('prop').filter(product=product)
    for prop in props:
        ProductsProperties.objects.create(product=new_product, prop=prop.prop)

    return new_product

@login_required
def edit_product(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование товара"""
    mh_vars = products_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    row = mh.get_row(row_id)
    context = mh.context

    all_costs_types = CostsTypes.objects.all().order_by('position')
    ids_costs_types = {
        cost_type.id: cost_type for cost_type in all_costs_types
    }

    context['costs_types'] = [{
            'id': cost_type.id,
            'name': cost_type.name,
            'tag': cost_type.tag,
            'currency': cost_type.currency,
        } for cost_type in all_costs_types]

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
            context['cats'] = row.productscats_set.select_related('cat', 'cat__container').filter(cat__isnull=False, cat__container__state=7)

            # Вывод родительских рубрик
            all_ids_parents = []
            ids_parents = {}
            ids_cats = {item.cat.id: item.cat for item in context['cats']}
            for k, v in ids_cats.items():
                if v.parents:
                    ids_parents[k] = [int(parent) for parent in v.parents.split('_') if parent]
                    all_ids_parents += ids_parents[k]
            parents = Blocks.objects.filter(pk__in=all_ids_parents)
            all_parents = {parent.id: parent for parent in parents}
            for item in context['cats']:
                if not item.cat.id in ids_parents:
                    continue
                item.parents = []
                for parent in ids_parents[item.cat.id]:
                    if parent in all_parents:
                        item.parents.append(all_parents[parent])

            context['props'] = row.productsproperties_set.select_related('prop', 'prop__prop').all()
            context['photos'] = row.productsphotos_set.all().order_by('position')
            context['seo'] = row.get_seo()
            costs = Costs.objects.filter(product=mh.row).values('cost_type', 'cost')
            ids_costs = {
                cost['cost_type']: cost['cost'] for cost in costs
            }
            for cost in context['costs_types']:
                if cost['id'] in ids_costs:
                    cost['price'] = ids_costs[cost['id']]
        elif action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удален' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'
        elif action == 'copy' and row:
            # Дублирование товара
            double = create_double(row)
            kwargs = {'row_id': double.id, 'action': 'edit'}
            return redirect(reverse('%s:%s' % (CUR_APP, 'edit_product'),
                                               kwargs=kwargs))
    elif request.method == 'POST':
        pass_fields = ['min_price', 'max_price']
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
            # ------------------------------
            # Сохраняем категории для товара
            # ------------------------------
            if mh.permissions['edit']:
                ids_cats = request.POST.getlist('cats')
                mh.row.productscats_set.filter(cat__container__state=7).delete()
                if ids_cats:
                    cats = Blocks.objects.select_related('container').filter(pk__in=ids_cats)
                    for cat in cats:
                        ProductsCats.objects.create(
                            product=mh.row,
                            cat=cat,
                            container=cat.container)
            # ------------------
            # Сохраняем типы цен
            # ------------------
            if mh.permissions['edit']:
                product_costs = Costs.objects.filter(product=mh.row).values('id', 'cost_type')
                ids_costs = {
                    cost['cost_type']: cost['id'] for cost in product_costs
                }
                for cost_type in all_costs_types:
                    cur_price = request.POST.get('price_%s' % cost_type.id)
                    if cost_type.id in ids_costs:
                        if cur_price:
                            Costs.objects.filter(pk=ids_costs[cost_type.id]).update(cost=cur_price)
                        else:
                            Costs.objects.filter(product=mh.row, cost_type=cost_type).delete()
                    elif cur_price:
                        Costs.objects.create(product=mh.row, cost_type=cost_type, cost=cur_price)

            # ------------
            # SEO/articles
            # ------------
            if mh.permissions['edit']:
                seo = {k: request.POST.get(k) for k in ('seo_title', 'seo_description', 'seo_keywords')}
                seo['linkcontainer'] = request.POST.getlist('linkcontainer')
                mh.row.fill_seo(**seo)

            # Загрузка в галерею,
            # причем только по ссылке, т/к
            # обработчик request.FILES работает через action='img'
            if request.POST.get('2gallery') and request.POST.get('grab_img_by_url') and mh.row and mh.permissions['edit']:
                context['row'] = object_fields(mh.row)
                add_photo2gallery(request.POST.get('grab_img_by_url'), mh.row, context)

        elif action == 'img' and request.FILES and mh.permissions['edit']:
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
        elif action == 'update' and row:
            if mh.permissions['edit']:
                row.name = request.POST.get('name')
                row.save()
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
    'search_result_format': ('{} ({}) #{}', 'name code id'),
}

def fast_create_props(request):
    """Быстрое создание свойств пачкой
       :param request: HttpRequest
    """
    result = {}
    perms = get_user_permissions(request.user, props_vars['model'])
    if not request.method == 'POST' or not request.POST.get('props') or not perms['create']:
        result['error'] = 'Недостаточно прав' if not perms['create'] else 'Нет данных для сохранения'
        return JsonResponse(result, safe=False)

    props = []
    props_count = request.POST.get('props', 0)
    try:
        props_count = int(props_count)
    except ValueError:
        return JsonResponse(result, safe=False)
    for i in range(props_count):
        props.append({
            'name': request.POST.get('name_%s' % i).strip(),
            'code': request.POST.get('code_%s' % i).strip(),
        })
    already_exists = 0
    created = 0
    for prop in props:
        if not prop['name']:
            continue
        code = prop['code'] or translit(prop['name'])
        analog = Property.objects.filter(code=code)
        if analog:
            already_exists += 1
            continue
        analog = Property.objects.create(name=prop['name'], code=code)
        created += 1
    result['success'] = 'Данные успешно сохранены'
    if already_exists:
        result['success'] += '<br>Уже найдено свойств: %s' % already_exists
        result['success'] += '<br>Добавлено новых свойств: %s' % created
    if not created:
        result['error'] = 'Не добавлено ни одного свойство'
    return JsonResponse(result, safe=False)

def fast_props2cat(request):
    """Быстрое добавление свойств к товарам по рубрике
       :param request: HttpRequest
    """
    result = {}
    perms = get_user_permissions(request.user, props_vars['model'])
    if not request.method == 'POST' or not request.POST.get('props2cat') or not perms['edit']:
        result['error'] = 'Недостаточно прав' if not perms['edit'] else 'Нет данных для сохранения'
        return JsonResponse(result, safe=False)
    props2cat = request.POST.getlist('props2cat')
    cat_id = request.POST.get('cat')
    if not props2cat or not cat_id:
        result['error'] = 'Недостаточно данных'
        return JsonResponse(result, safe=False)
    props2cat = [int(prop_id) for prop_id in props2cat if prop_id]
    pcats = ProductsCats.objects.select_related('product').filter(cat=cat_id)

    pvalues = PropertiesValues.objects.filter(prop__in=props2cat).order_by('position')
    ids_pvalues = {}
    for pvalue in pvalues:
        if pvalue.prop_id in ids_pvalues:
            continue
        ids_pvalues[pvalue.prop_id] = pvalue

    props = Property.objects.filter(pk__in=ids_pvalues.keys())
    ids_props = {prop.id: prop for prop in props}

    for pcat in pcats:
        for prop_id in props2cat:
            if not prop_id in ids_props:
                logger.info('[ERROR]: prop not found %s' % prop_id)
            prop = ids_props[prop_id]
            # Любое значение свойства привязано
            analog = ProductsProperties.objects.filter(prop__prop=prop, product=pcat.product).aggregate(Count('id'))['id__count']
            if analog:
                continue
            # Нету нифуя - создаем свойство из первого значения св-ва
            pvalue = ids_pvalues[prop.id]
            ProductsProperties.objects.create(prop=pvalue, product=pcat.product)
    result['success'] = 'Данные успешно сохранены'
    return JsonResponse(result, safe=False)

@login_required
def show_props(request, *args, **kwargs):
    """Вывод свойств для товаров/услуг"""
    if request.method == 'POST':
        if request.POST.get('props'):
            # Быстрое создание свойств пачкой
            return fast_create_props(request)
        if request.POST.get('props2cat'):
            # Быстрое добавление свойств к товарам по рубрике
            return fast_props2cat(request)
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
            if value:
                value = value.strip()
            is_active = request.POST.get('is_active')
            code = request.POST.get('code')
            prop = PropertiesValues(prop=row)
            if pk:
                analog = PropertiesValues.objects.filter(pk=pk, prop=row).first()
                if analog:
                    prop = analog
            else:
                # Дубли нам не нужны
                analog = PropertiesValues.objects.filter(prop=row, str_value=value)
                if analog:
                    result['error'] = 'Вы создаете дубликат'
                    return JsonResponse(result, safe=False)
            prop.str_value = value
            prop.is_active = True if is_active else False
            prop.code = code

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

@login_required
def props_positions(request, *args, **kwargs):
    """Изменение позиций свойств"""
    result = {}
    mh_vars = props_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    mh.get_permissions(Products) # Права от товаров/услуг
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_props(request, *args, **kwargs):
    """Поиск свойств
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = props_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', 'code', 'id'), )

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
    else:
        mh.order_by_add('position')

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
    mh_vars['select_related_list'] = ['prop', 'prop__prop']
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.get_permissions(Products) # Права от товаров/услуг
    context = mh.context
    row = mh.get_row(row_id)
    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))

    special_model_vars(mh, mh_vars, context)

    if request.method == 'GET':
        if action == 'drop' and row:
            if mh.permissions['drop']:
                row.delete()
                mh.row = None
                context['success'] = '%s удалено' % (mh.singular_obj, )
            else:
                context['error'] = 'Недостаточно прав'
    elif request.method == 'POST':
        # Обновляем линковку
        prop = None
        prop_id = request.POST.get('prop_id')
        if prop_id:
            prop = Property.objects.filter(pk=prop_id).first()

        pvalue = None
        pvalue_id = request.POST.get('pvalue_id')
        if pvalue_id:
            pvalue = PropertiesValues.objects.filter(pk=pvalue_id).first()

        product = None
        product_id = request.POST.get('product')
        if product_id:
            product = Products.objects.filter(pk=product_id).first()

        new_tag = request.POST.get('new_tag', '')
        new_tag = new_tag.strip()
        if prop and new_tag and not pvalue:
            pvalue = PropertiesValues.objects.filter(prop=prop, str_value=new_tag).first()
            if not pvalue and mh.permissions['create']:
                pvalue = PropertiesValues()
                pvalue.prop = prop
                pvalue.str_value = new_tag
                pvalue.save()

        if action == 'create' or (action == 'edit' and row):

            analog = ProductsProperties.objects.filter(
                product = product,
                prop = pvalue,
            )
            if row:
                analog = analog.exclude(pk=row.id)
            if analog:
                if analog:
                    context['error'] = 'Такое свойство уже присвоено этому товару'
            elif action == 'create' and product and pvalue:
                if mh.permissions['create'] and prop:
                    row = ProductsProperties.objects.create(
                        product = product,
                        prop = pvalue,
                    )
                    context['success'] = 'Данные успешно записаны'
                    context['row'] = {'id': row.id}
                else:
                    context['error'] = 'Недостаточно прав'
            elif action == 'edit' and row and product and product.id == row.product_id:
                if mh.permissions['edit']:
                    if pvalue:
                        row.prop = pvalue
                    row.save()
                    context['success'] = 'Данные успешно записаны'
                else:
                    context['error'] = 'Недостаточно прав'
            else:
                context['error'] = 'Произошла ошибка'
        if row:
            context['row'] = {
                'id': row.id,
                'prop_id': row.prop.prop.id,
                'pvalue_id': row.prop.id,

                'name': row.prop.prop.name,
                'is_active': row.prop.prop.is_active,
                'position': row.prop.prop.position,
                'value': row.prop.str_value,
            }
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
            cat = None
            try:
                cat_id = int(cat_id)
            except ValueError:
                logger.exception('cat_id not int')
                cat_id = None
            if cat_id:
                cat = Blocks.objects.filter(pk=cat_id).first()
                if cat:
                    mh.filter_add(Q(cat=cat))
            if not cat:
                mh.filter_add(Q(pk=0))
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
        edit_urla = reverse('%s:%s' % (CUR_APP, 'edit_product'),
                            kwargs={'action': 'edit', 'row_id': 0})
        for row in rows:
            item = object_fields(row,
                                 only_fields=only_fields,
                                 fk_only_keys=fk_keys, )
            item['actions'] = row.id
            item['edit_urla'] = edit_urla.replace('/0/', '/%s/' % row.id)
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
    method = request.GET if request.method == 'GET' else request.POST
    search_facet = True if method.get('search_facet') else False
    force_new = True if method.get('force_new') else False
    strategy = get_search_strategy()
    result = strategy.get_facet_filters(
        cat_id=cat_id,
        search_facet=search_facet,
        force_new=force_new,
    )
    return JsonResponse(result, safe=False)
