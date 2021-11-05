# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q

from apps.flatcontent.models import Blocks
from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import (
    create_model_helper,
    ModelHelper,
    tabulator_filters_and_sorters,
)
from apps.main_functions.api_helper import ApiHelper
from apps.main_functions.catcher import defiz_phone
from apps.main_functions.views_helper import (
    show_view,
    edit_view,
    search_view,
)

from .models import (
    Company,
    MainCompany,
    Contact,
    Company2Category,
    MainCompany2Category,
)

CUR_APP = 'companies'
companies_vars = {
    'singular_obj': 'Филиал',
    'plural_obj': 'Филиалы',
    'rp_singular_obj': 'филиала',
    'rp_plural_obj': 'филиалов',
    'template_prefix': 'companies_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'companies',
    'submenu': 'companies',
    'show_urla': 'show_companies',
    'create_urla': 'create_company',
    'edit_urla': 'edit_company',
    'model': Company,
    #'custom_model_permissions': Company,
}

def api(request, action: str = 'companies'):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param action: к какой модели обращаемся
    """
    #if action == 'companies':
    #    result = ApiHelper(request, companies_vars, CUR_APP)
    result = ApiHelper(request, companies_vars, CUR_APP)
    return result

def fill_parent_cats(cats: dict):
    """Вывод родительских рубрик
       :param cats: context['cats']
                    родительские рубрики экземпляров моделей (компаний)
    """
    all_ids_parents = []
    ids_parents = {}
    ids_cats = {item.cat.id: item.cat for item in cats}
    for k, v in ids_cats.items():
        if v.parents:
            ids_parents[k] = [int(parent) for parent in v.parents.split('_') if parent]
            all_ids_parents += ids_parents[k]
    parents = Blocks.objects.filter(pk__in=all_ids_parents)
    all_parents = {parent.id: parent for parent in parents}
    for item in cats:
        if not item.cat.id in ids_parents:
            continue
        item.parents = []
        for parent in ids_parents[item.cat.id]:
            if parent in all_parents:
                item.parents.append(all_parents[parent])

@login_required
def show_companies(request, *args, **kwargs):
    """Вывод филиалов
       :param request: HttpRequest
    """
    mh_vars = companies_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('main_company')
    mh.select_related_add('address')
    context = mh.context

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()
        result = []
        for row in rows:
            item = object_fields(row)
            item['phone'] = defiz_phone(row.phone)
            item['actions'] = row.id
            item['folder'] = row.get_folder()
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
            if row.main_company:
                item['main_company__id'] = row.main_company.id
                item['main_company__name'] = row.main_company.name
            if row.address:
                item['address'] = object_fields(row.address)
                item['address']['address_str'] = row.address.address_str()

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
def edit_company(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование филиала
       :param request: HttpRequest
       :param action: действие над филиалом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = companies_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('main_company')
    mh.select_related_add('address')
    row = mh.get_row(row_id)
    context = mh.context # Контекст дозаполняется в get_row

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
            context['cats'] = row.company2category_set.select_related(
                'cat', 'cat__container'
            ).filter(
                cat__isnull=False,
                cat__container__state=7,
                cat__container__tag='catalogue',
            )
            # Вывод родительских рубрик
            fill_parent_cats(context['cats'])

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
            # ----------------------------
            # Сохраняем категории компании
            # ----------------------------
            if mh.permissions['edit']:
                ids_cats = request.POST.getlist('company2category')
                mh.row.company2category_set.filter(
                    cat__container__state=7,
                    cat__container__tag='catalogue',
                ).delete()
                if ids_cats:
                    cats = Blocks.objects.select_related('container').filter(pk__in=ids_cats)
                    for cat in cats:
                        Company2Category.objects.create(
                            company=mh.row,
                            cat=cat,
                        )

        elif action == 'img' and request.FILES:
            mh.uploads()
    if mh.row:
        context['row'] = object_fields(mh.row, pass_fields=('password', ))
        context['row']['folder'] = mh.row.get_folder()
        context['row']['thumb'] = mh.row.thumb()
        context['row']['imagine'] = mh.row.imagine()
        if mh.row.address:
            context['row']['address'] = object_fields(mh.row.address)
            context['row']['address']['address_str'] = mh.row.address.address_str()
        context['redirect'] = mh.get_url_edit()

    if request.is_ajax() or action == 'img':
        return JsonResponse(context, safe=False)
    template = '%sedit.html' % (mh.template_prefix, )
    return render(request, template, context)

@login_required
def companies_positions(request, *args, **kwargs):
    """Изменение позиций филиалов
       :param request: HttpRequest
    """
    result = {}
    mh_vars = companies_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_companies(request, *args, **kwargs):
    """Поиск филиалов
       :param request: HttpRequest
    """
    result = {'results': []}
    mh = ModelHelper(Company, request)
    mh_vars = companies_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)
    mh.search_fields = ('id', 'name')
    rows = mh.standard_show()
    for row in rows:
        result['results'].append({'text': '%s (%s)' % (row.name, row.id), 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}
    return JsonResponse(result, safe=False)

main_companies_vars = {
    'singular_obj': 'Компания',
    'plural_obj': 'Компании',
    'rp_singular_obj': 'компании',
    'rp_plural_obj': 'компаний',
    'template_prefix': 'main_companies_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'companies',
    'submenu': 'main_companies',
    'show_urla': 'show_main_companies',
    'create_urla': 'create_main_company',
    'edit_urla': 'edit_main_company',
    'model': MainCompany,
    #'custom_model_permissions': Company,
}

def get_main_companies_cats(ids_companies: dict, tag: str = None):
    """Получение категорий по списку компаний
       :param ids_companies: словарь идентификаторов товаров
       :param tag: тег каталога
    """
    cats = MainCompany2Category.objects.select_related('cat').filter(main_company__in=ids_companies, cat__isnull=False, cat__container__state=7)
    if tag:
        cats = cats.filter(cat__container__tag=tag)
    cats = cats.values('main_company', 'cat__id', 'cat__link', 'cat__name')

    for cat in cats:
        if not ids_companies[cat['main_company']]:
            ids_companies[cat['main_company']] = []
        ids_companies[cat['main_company']].append({
            'id': cat['cat__id'],
            'link': cat['cat__link'],
            'name': cat['cat__name'],
        })

@login_required
def show_main_companies(request, *args, **kwargs):
    """Вывод группы компаний
       :param request: HttpRequest
    """
    mh_vars = main_companies_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)

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

    # Условие под выборку определенной категории
    cat_filter = filters_and_sorters['params'].get('filters', {})
    if 'cat' in cat_filter:
        ids_companies = MainCompany2Category.objects.filter(cat=cat_filter['cat']).values_list('main_company', flat=True)
        ids_companies = list(ids_companies)
        mh.filter_add(Q(pk__in = ids_companies))

    # -----------------------------
    # Вся выборка только через аякс
    # -----------------------------
    if request.is_ajax():
        rows = mh.standard_show()

        ids_companies = {row.id: None for row in rows}
        get_main_companies_cats(ids_companies)

        result = []
        for row in rows:
            item = object_fields(row)
            item['actions'] = row.id
            item['folder'] = row.get_folder()
            item['thumb'] = row.thumb()
            item['imagine'] = row.imagine()
            if ids_companies[row.id]:
                item['cat'] = ids_companies[row.id]
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
def edit_main_company(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование компании
       :param request: HttpRequest
       :param action: действие над компанией (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = main_companies_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    row = mh.get_row(row_id)
    context = mh.context # Контекст дозаполняется в get_row

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
            context['cats'] = row.maincompany2category_set.select_related(
                'cat', 'cat__container'
            ).filter(
                cat__isnull=False,
                cat__container__state=7,
                cat__container__tag='catalogue',
            )
            # Вывод родительских рубрик
            fill_parent_cats(context['cats'])

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

            # ----------------------------
            # Сохраняем категории компании
            # ----------------------------
            if mh.permissions['edit']:
                ids_cats = request.POST.getlist('maincompany2category')
                mh.row.maincompany2category_set.filter(
                    cat__container__state=7,
                    cat__container__tag='catalogue',
                ).delete()
                if ids_cats:
                    cats = Blocks.objects.select_related('container').filter(pk__in=ids_cats)
                    for cat in cats:
                        MainCompany2Category.objects.create(
                            main_company=mh.row,
                            cat=cat,
                        )

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
def main_companies_positions(request, *args, **kwargs):
    """Изменение позиций компаний
       :param request: HttpRequest
    """
    result = {}
    mh_vars = main_companies_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_main_companies(request, *args, **kwargs):
    """Поиск компаний
       :param request: HttpRequest
    """
    result = {'results': []}
    mh = ModelHelper(MainCompany, request)
    mh_vars = main_companies_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)
    mh.search_fields = ('id', 'name')
    rows = mh.standard_show()
    for row in rows:
        result['results'].append({'text': '%s (%s)' % (row.name, row.id), 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}
    return JsonResponse(result, safe=False)


contacts_vars = {
    'singular_obj': 'Контакт',
    'plural_obj': 'Контакты',
    'rp_singular_obj': 'контакта',
    'rp_plural_obj': 'контактов',
    'template_prefix': 'contacts_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'companies',
    'submenu': 'contacts',
    'show_urla': 'show_contacts',
    'create_urla': 'create_contact',
    'edit_urla': 'edit_contact',
    'model': Contact,
    #'custom_model_permissions': Company,
}

@login_required
def show_contacts(request, *args, **kwargs):
    """Вывод контактов
       :param request: HttpRequest
    """
    mh_vars = contacts_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    mh.select_related_add('company')
    mh.select_related_add('main_company')
    context = mh.context
    context['ctypes'] = Contact.ctype_choices

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
            item['indexed_value'] = row.value
            if row.main_company:
                item['main_company__id'] = row.main_company.id
                item['main_company__name'] = row.main_company.name
            if row.company:
                item['company__id'] = row.company.id
                item['company__name'] = row.company.name
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
def edit_contact(request, action: str, row_id: int = None, *args, **kwargs):
    """Создание/редактирование контакта
       :param request: HttpRequest
       :param action: действие над контактом (создание/редактирование/удаление)
       :param row_id: ид записи
    """
    mh_vars = contacts_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, action)
    mh.select_related_add('company')
    mh.select_related_add('main_company')
    row = mh.get_row(row_id)
    context = mh.context # Контекст дозаполняется в get_row
    context['ctypes'] = Contact.ctype_choices

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
        pass_fields = ('main_company', )
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
def contacts_positions(request, *args, **kwargs):
    """Изменение позиций контактов
       :param request: HttpRequest
    """
    result = {}
    mh_vars = contacts_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP, 'positions')
    result = mh.update_positions()
    return JsonResponse(result, safe=False)

def search_contacts(request, *args, **kwargs):
    """Поиск контактов
       :param request: HttpRequest
    """
    result = {'results': []}
    mh = ModelHelper(Contact, request)
    mh_vars = contacts_vars.copy()
    for k, v in mh_vars.items():
        setattr(mh, k, v)
    mh.search_fields = ('id', 'name')
    rows = mh.standard_show()
    for row in rows:
        result['results'].append({'text': '%s (%s)' % (row.name, row.id), 'id': row.id})
    if mh.raw_paginator['cur_page'] == mh.raw_paginator['total_pages']:
        result['pagination'] = {'more': False}
    else:
        result['pagination'] = {'more': True}
    return JsonResponse(result, safe=False)

