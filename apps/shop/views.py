# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import ModelHelper, create_model_helper
from apps.main_functions.api_helper import ApiHelper, XlsxHelper
from apps.main_functions.views_helper import (show_view,
                                              edit_view,
                                              search_view, )
from apps.products.models import Products, CostsTypes, Costs

from .models import Orders, Purchases, Transactions, PromoCodes
from .cart import calc_cart, get_shopper, create_shopper, get_purchase

CUR_APP = 'shop'
orders_vars = {
    'singular_obj': 'Заказ',
    'plural_obj': 'Заказы',
    'rp_singular_obj': 'заказа',
    'rp_plural_obj': 'заказов',
    'template_prefix': 'orders_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'shop',
    'submenu': 'orders',
    'show_urla': 'show_orders',
    'create_urla': 'create_order',
    'edit_urla': 'edit_order',
    'model': Orders,
}

def api(request, action: str = 'orders'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    #if action == 'orders':
    #    result = ApiHelper(request, shop_vars, CUR_APP)
    result = ApiHelper(request, shop_vars, CUR_APP)
    return result

def import_xlsx(request, action: str = 'promocodes'):
    """Апи-метод для сохранения данных из excel-файла
                     удаления данных по excel-файлу
       :param request: HttpRequest
       :param action: какую модель использовать
    """
    #if action == 'user':
    #    result = XlsxHelper(request, promocodes_vars, CUR_APP)
    result = XlsxHelper(request, promocodes_vars, CUR_APP,
                        cond_fields = ['code'])
    return result

@login_required
def show_orders(request, *args, **kwargs):
    """Вывод заказов
       :param request: HttpRequest
    """
    mh_vars = orders_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('shopper')
    mh.select_related_add('promocode')
    context = mh.context
    context['state_choices'] = Orders.state_choices
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
def edit_order(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование заказа
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = orders_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('shopper')
    mh.select_related_add('promocode')
    row = mh.get_row(row_id)
    context = mh.context
    context['state_choices'] = Orders.state_choices
    template = '%sedit.html' % (mh.template_prefix, )

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
        elif action == 'view' and row:
            context['action_edit'] = 'Просмотр'
            mh.action_edit = 'Просмотр'
            mh.breadcrumbs_add({
                'link': mh.url_edit,
                'name': '%s %s' % (mh.action_edit, mh.rp_singular_obj),
            })
            template = '%sview.html' % (mh.template_prefix, )
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
        elif action == 'img' and request.FILES:
            mh.uploads()
    if mh.row:
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        context['redirect'] = mh.get_url_edit()
        context['row']['get_number'] = mh.row.get_number()
        context['row']['total_without_discount'] = mh.row.total_without_discount()
        if mh.row.promocode:
            context['row']['promocode'] = mh.row.get_promocode()
        context['row']['purchases'] = mh.row.get_purchases()
    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)

    return render(request, template, context)

@login_required
def orders_positions(request, *args, **kwargs):
    """Изменение позиций заказов
       :param request: HttpRequest
    """
    result = {}
    mh_vars = orders_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_orders(request, *args, **kwargs):
    """Поиск заказов
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = orders_vars,
                       cur_app = CUR_APP,
                       sfields = ('number', ), )

purchases_vars = {
    'singular_obj': 'Покупка',
    'plural_obj': 'Покупки',
    'rp_singular_obj': 'покупки',
    'rp_plural_obj': 'покупок',
    'template_prefix': 'purchases_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'shop',
    'submenu': 'purchases',
    'show_urla': 'show_purchases',
    'create_urla': 'create_purchase',
    'edit_urla': 'edit_purchase',
    'model': Purchases,
}

@login_required
def show_purchases(request, *args, **kwargs):
    """Вывод покупок
       :param request: HttpRequest
    """
    mh_vars = purchases_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('shopper')
    mh.select_related_add('order')
    mh.select_related_add('cost_type')
    context = mh.context

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
            item['shopper__id'] = '%s #%s' % (str(row.shopper), row.shopper.id) if row.shopper else ''
            item['order__id'] = '%s #%s' % (row.order.number or '', row.order.id) if row.order else ''
            item['cost_type__id'] = row.cost_type.name if row.cost_type else ''
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
def edit_purchase(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование покупок
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = purchases_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('shopper')
    mh.select_related_add('order')
    mh.select_related_add('cost_type')
    row = mh.get_row(row_id)
    context = mh.context

    if mh.error:
        return redirect('%s?error=not_found' % (mh.root_url, ))
    if request.method == 'GET':
        if action in ('create', 'edit'):
            context['costs_types'] = CostsTypes.objects.all()
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

@login_required
def purchases_positions(request, *args, **kwargs):
    """Изменение позиций покупок
       :param request: HttpRequest
    """
    result = {}
    mh_vars = purchases_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_purchases(request, *args, **kwargs):
    """Поиск покупок
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = purchases_vars,
                       cur_app = CUR_APP,
                       sfields = ('product_id', 'product_name', 'product_code'), )

transactions_vars = {
    'singular_obj': 'Транзакция',
    'plural_obj': 'Транзакции',
    'rp_singular_obj': 'транзакции',
    'rp_plural_obj': 'транзакций',
    'template_prefix': 'transactions_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'shop',
    'submenu': 'transactions',
    'show_urla': 'show_transactions',
    'create_urla': 'create_transaction',
    'edit_urla': 'edit_transaction',
    'model': Transactions,
}

@login_required
def show_transactions(request, *args, **kwargs):
    """Вывод транзакций
       :param request: HttpRequest
    """
    mh_vars = transactions_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('order')
    context = mh.context

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
def edit_transaction(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование транзакции
       :param request: HttpRequest
       :param action: действие над объектом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = transactions_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('order')
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

@login_required
def transactions_positions(request, *args, **kwargs):
    """Изменение позиций транзакций
       :param request: HttpRequest
    """
    result = {}
    mh_vars = transactions_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_transactions(request, *args, **kwargs):
    """Поиск транзакций
       :param request: HttpRequest
    """
    return search_view(request,
                       model_vars = transactions_vars,
                       cur_app = CUR_APP,
                       sfields = ('uuid', 'order__id', 'order__number'), )

promocodes_vars = {
    'singular_obj': 'Промокод',
    'plural_obj': 'Промокоды',
    'rp_singular_obj': 'промокода',
    'rp_plural_obj': 'промокодов',
    'template_prefix': 'promocodes_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'shop',
    'submenu': 'promocodes',
    'show_urla': 'show_promocodes',
    'create_urla': 'create_promocode',
    'edit_urla': 'edit_promocode',
    'model': PromoCodes,
    #'custom_model_permissions': Orders,
    'select_related_list': ('personal', ),
}

@login_required
def show_promocodes(request, *args, **kwargs):
    """Вывод промокодов"""
    extra_vars = {
        'import_xlsx_url': reverse('%s:%s' % (CUR_APP, 'import_xlsx'),
                                             kwargs={'action': 'promocodes'}),
    }
    return show_view(request,
                     model_vars = promocodes_vars,
                     cur_app = CUR_APP,
                     extra_vars = extra_vars, )

@login_required
def edit_promocode(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование промокодов"""
    return edit_view(request,
                     model_vars = promocodes_vars,
                     cur_app = CUR_APP,
                     action = action,
                     row_id = row_id,
                     extra_vars = None, )

@login_required
def promocodes_positions(request, *args, **kwargs):
    """Изменение позиций промокодов"""
    result = {}
    mh_vars = promocodes_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_promocodes(request, *args, **kwargs):
    """Поиск промокодов"""
    return search_view(request,
                       model_vars = promocodes_vars,
                       cur_app = CUR_APP,
                       sfields = ('name', 'code'), )

def cart(request, action):
    """Взаимодействие пользователя с корзинкой
       :param request: HttpRequest
       :param action: действие
    """
    result = {}
    shopper = get_shopper(request)

    method = request.GET
    if request.method == 'POST':
        method = request.POST
    quantity = method.get('quantity', 1)
    product_id = method.get('product_id')
    purchase_id = method.get('purchase_id')
    cost_type_id = method.get('cost_type_id')
    cost_type = None
    cost = None

    if action == 'show':
        # Аякс корзинка
        cart = calc_cart(shopper)
        context = {
            'cart': cart,
        }
        template = 'web/order/ajax_cart.html'
        return render(request, template, context)
    elif action == 'add' and product_id.isdigit():
        # Добавление товара в корзинку
        count = int(quantity)
        if count <= 0:
            count = 1
        product = Products.objects.filter(pk=product_id).first()
        # Проверяем передан ли тип цены
        if cost_type_id and product:
            cost_type = CostsTypes.objects.filter(pk=cost_type_id).first()
            if not cost_type:
                result['error'] = 'Тип цены не найден'
            else:
                cost = Costs.objects.filter(product=product, cost_type=cost_type).first()
                if not cost:
                    result['error'] = 'Цена не найдена'
        # Если цены нет, тогда и товара нет :) ибо - пысу!
        if product and not product.price and not cost:
            product = None

        purchase = None
        if not product:
            result['error'] = 'Товар не найден'
        else:
            if not shopper or not shopper.id:
                shopper = create_shopper(request)
            else:
                purchase = get_purchase(product.id, shopper, is_purchase=False, cost_type=cost_type)
            if purchase:
                Purchases.objects.filter(pk=purchase.id).update(count=purchase.count + count)
                result['success'] = 'Количество увеличено'
            else:
                Purchases.objects.create(
                    shopper=shopper,
                    product_id=product.id,
                    product_name=product.name,
                    product_manufacturer=product.manufacturer,
                    product_measure=product.measure,
                    product_price=product.price or cost.cost,
                    product_code=product.code,
                    product_min_count=product.min_count,
                    product_multiplicity=product.multiplicity,
                    count=quantity,
                    cost=product.price or cost.cost,
                    cost_type=cost_type, )
                result['success'] = 'Добавлено в корзинку'
    elif shopper and action == 'quantity' and purchase_id and quantity:
        not_found = 'Покупка не найдена или передано неправильное количество'

        if purchase_id.isdigit() and quantity.isdigit():
            purchase_id = int(purchase_id)
            count = int(quantity)
            purchase = get_purchase(purchase_id, shopper)
            if purchase and count > 0:
                Purchases.objects.filter(pk=purchase.id).update(count=count)
                result['success'] = 'Количество обновлено'
            else:
                result['error'] = not_found
        else:
            result['error'] = not_found
    elif shopper and action == 'drop' and purchase_id:
        not_found = 'Покупка не найдена'
        if purchase_id.isdigit():
            purchase = get_purchase(purchase_id, shopper)
            purchase.delete()
            result['success'] = 'Покупка удалена'
        else:
            result['error'] = not_found
    elif shopper and action == 'promocode':
        code = method.get('promocode')
        if not code:
            result['error'] = 'Вы не ввели промокод'
        else:
            code = code.strip()
            promocodes = PromoCodes.objects.filter(code=code)
            for promocode in promocodes:
                if not promocode.is_valid(shopper_id=shopper.id):
                    continue
                request.session['promocode'] = promocode.id
                result['success'] = 'Промокод успешно применен'
                break
            if not 'promocode' in request.session:
                result['error'] = 'Промокод не найден или истек срок действия'
    else:
        result['error'] = 'Произошла ошибка'

    return JsonResponse(result, safe=False)