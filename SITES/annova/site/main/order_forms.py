# -*- coding:utf-8 -*-
import math

from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.db.models import Q

from apps.main_functions.views import DefaultFeedback
from apps.main_functions.date_time import str_to_date, date_plus_days
from apps.personal.models import Shopper
from apps.shop.models import Orders, Purchases
from apps.products.models import Products
from apps.flatcontent.models import Blocks

from apps.site.passport.models import Passport
from apps.site.polis.models import Polis, PolisMember

main_vars = {
    'singular_obj': 'Главная',
    'template_prefix': 'main_',
    'show_urla': 'home',
}

def get_markup_product(total_price: float):
    """Товар для наценки на 2.3%
       сначала добавляем 2.3%
       потом от этой суммы выясняем 2.3%
       и добавляем к первоначальной сумме
    """
    total_price = float(total_price)
    markup_price = (total_price + total_price * 2.3/100) * 2.3/100
    markup = Products.objects.filter(code='markup').first()
    if not markup:
        markup = Products.objects.create(code='markup', name='Банковский налог')

    # Фикс на копейки
    for i in range(100):
        total_price_with_markup = total_price + markup_price
        diff = total_price_with_markup * 2.3 / 100
        if total_price_with_markup - diff < total_price:
            markup_price += 0.01
        else:
            break

    markup.price = markup_price

    return markup


def order_form_hockey(request):
    """Страничка оформления заказа для страховки Хоккей
       У нас теперь 2 паспорта фигирирует, страхователя и застрахованного
       Ребенка привязываем к PolisMember (к нему паспорт)
       Родителя привязываем к Shopper (по нему найдем паспорт)
    """
    mh_vars = main_vars.copy()
    context = {}
    q_string = {}
    containers = {}

    kwargs = {
        'force_send': 1, # Принудительная отправка
        #'fv': [],
        #'dummy': 1, # Не возвращаем HttpResponse
        #'do_not_send': 1, # Не отправляем письмо
        'fields':[
          {'name': 'test_field', 'value': 'Тестовое поле'},
          {'name': 'insurance_type', 'value': 'Тип страховки'},
          {'name': 'started', 'value': 'Дата начала программы'},
          # Страхователь
          {'name': 'last_name', 'value': 'Фамилия родителя'},
          {'name': 'first_name', 'value': 'Имя родителя'},
          {'name': 'middle_name', 'value': 'Отчество родителя'},

          {'name': 'passport_birthday', 'value': 'Дата рождения родителя'},
          {'name': 'passport_series', 'value': 'Паспорт родителя, серия'},
          {'name': 'passport_number', 'value': 'Паспорт родителя, номер'},
          {'name': 'passport_issued', 'value': 'Паспорт родителя, кем выдан'},
          {'name': 'passport_issued_date', 'value': 'Паспорт родителя, когда выдан'},
          {'name': 'passport_registration', 'value': 'Паспорт родителя, место регистрации'},

          # Ребенок
          {'name': 'child_last_name', 'value': 'Фамилия ребенка'},
          {'name': 'child_first_name', 'value': 'Имя ребенка'},
          {'name': 'child_middle_name', 'value': 'Отчество ребенка'},

          {'name': 'child_passport_birthday', 'value': 'Дата рождения ребенка'},
          {'name': 'child_passport_series', 'value': 'Паспорт ребенка, серия'},
          {'name': 'child_passport_number', 'value': 'Паспорт ребенка, номер'},
          {'name': 'child_passport_issued', 'value': 'Паспорт ребенка, кем выдан'},
          {'name': 'child_passport_issued_date', 'value': 'Паспорт ребенка, когда выдан'},
          {'name': 'child_passport_registration', 'value': 'Паспорт ребенка, место регистрации'},

          {'name': 'birthday_cert', 'value': 'Свидетельство о рождении ребенка'},
        ],
    }

    if request.method == 'POST':
        order_id = None
        # Заполняем паспортные данные, по ним найдем пользователя
        passport_fields = {
            'series': '',
            'number': '',
            'issued': '',
            'issued_date': '',
            'registration': '',
            'birthday': '',
        }
        parent_passport_fields = {}
        child_passport_fields = {}

        for key in passport_fields.keys():
            parent_passport_fields[key] = request.POST.get('passport_%s' % key)
            child_passport_fields[key] = request.POST.get('child_passport_%s' % key)

        # TODO: если искать имеющиеся паспорта, тогда будет проблема с PolisMember
        # т/к polis_member.passport OneToOneField на Passport
        # пока просто создаем новые паспорта,
        # по-хорошему, нужно Shopper-Passport связь сделать тоже OneToOneField
        passports = []
        #passports = Passport.objects.select_related('shopper').filter(
        #    Q(series=parent_passport_fields['series'], number=parent_passport_fields['number'])|
        #    Q(series=child_passport_fields['series'], number=child_passport_fields['number'])
        #)
        parent_passport = Passport(ptype=1)
        child_passport = Passport(ptype=1)
        for passport in passports:
            if passport.series == parent_passport_fields['series'] and passport.number == parent_passport_fields['number']:
                parent_passport = passport
            elif passport.series == child_passport_fields['series'] and passport.number == child_passport_fields['number']:
                child_passport = passport

        for key in passport_fields.keys():
            pvalue = parent_passport_fields[key]
            cvalue = child_passport_fields[key]
            if key in ('birthday', 'issued_date'):
                pvalue = str_to_date(pvalue)
                cvalue = str_to_date(cvalue)
            setattr(parent_passport, key, pvalue)
            setattr(child_passport, key, cvalue)
        parent_passport.save()
        # Фикс на свидетельство о рождении
        if request.POST.get('passport_ptype') in (2, '2'):
            child_passport.ptype = 3
            child_passport.registration = request.POST.get('birthday_cert')
        child_passport.save()
        # Заполняем пользователя
        if parent_passport.shopper:
            shopper = parent_passport.shopper
        else:
            shopper = Shopper()
        shopper_fields = {
            'name': '',
            'phone': '',
            'email': '',
            'first_name': '',
            'last_name': '',
            'middle_name': '',
        }
        for key in shopper_fields.keys():
            shopper_fields[key] = request.POST.get(key)
            if not shopper_fields[key]:
                continue
            setattr(shopper, key, shopper_fields[key])
        if not shopper.name:
            shopper.name = '%s %s %s' % (
                shopper.last_name if shopper.last_name else '',
                shopper.first_name if shopper.first_name else '',
                shopper.middle_name if shopper.middle_name else '',
            )
        shopper.save()
        request.session['shopper'] = shopper.to_dict()

        parent_passport.shopper = shopper
        parent_passport.save()

        # Заполняем заказ
        product = Products.objects.filter(pk=request.POST.get('product')).first()

        started = str_to_date(request.POST.get('started'))
        if product:
            markup = get_markup_product(product.price)
            order = Orders.objects.create(
                total=float(product.price) + float(markup.price),
                shopper=shopper,
                shopper_name=shopper.name,
                shopper_email=shopper.email,
                shopper_phone=shopper.phone,
                shopper_address=parent_passport.registration,
                comments='Паспорт: \nСерия: %s, номер: %s\nКем выдан: %s\nКогда выдан: %s' % (
                    parent_passport.series,
                    parent_passport.number,
                    parent_passport.issued,
                    parent_passport.issued_date.strftime('%Y-%m-%d') if parent_passport.issued_date else None,
                )
            )
            order_id = order.id
            purchase = Purchases.objects.create(
                product_id=product.id,
                product_name=product.name,
                product_price=product.min_count, # страховая премия
                product_code=product.code,
                product_measure=product.measure,
                count=1,
                cost=product.price,
                shopper=shopper,
                order=order,
            )

            purchase = Purchases.objects.create(
                product_id=markup.id,
                product_name=markup.name,
                product_price=0,
                product_code=markup.code,
                count=1,
                cost=markup.price,
                shopper=shopper,
                order=order,
            )

            ended = None
            if started and product.count:
                ended = date_plus_days(started, product.count * 30) 
            ptype = request.POST.get('ptype')
            if not ptype or not ptype.isdigit():
                ptype = 1
            polis = Polis.objects.create(
                order = order,
                ptype=ptype,
                number = order_id,
                name = shopper.name,
                #birthday = birthday, # depricated
                insurance_sum = product.min_count,
                insurance_program = product.stock_info,
                from_date = started,
                to_date = ended)
            # Заполняем для ребенка (в name пишем свидетельство о рождении)
            first_name = request.POST.get('child_first_name')
            last_name = request.POST.get('child_last_name')
            middle_name = request.POST.get('child_middle_name')
            child_member = PolisMember(polis=polis,
                                       passport=child_passport,
                                       name='%s %s %s' % (last_name, first_name, middle_name))
            child_member.save()

        DefaultFeedback(request, **kwargs)

        return redirect('/shop/checkout/?order_id=%s' % order_id)
    template = 'web/thanks.html'

    page = SearchLink(q_string, request, containers)
    context['page'] = page
    context['containers'] = containers

    return render(request, template, context)

def order_form_cruise(request):
    """Страничка оформления заказа для страховки Круиз"""
    mh_vars = main_vars.copy()
    context = {}
    q_string = {}
    containers = {}

    kwargs = {
        'force_send': 1, # Принудительная отправка
        #'fv': [],
        #'dummy': 1, # Не возвращаем HttpResponse
        #'do_not_send': 1, # Не отправляем письмо
        'fields':[
          {'name': 'cruise', 'value': 'Круиз'},

          #{'name': 'fname', 'value': 'Имя страхователя на латинице'},
          {'name': 'last_fname', 'value': 'Фамилия страхователя на латинице'},
          {'name': 'first_fname', 'value': 'Имя страхователя на латинице'},

          {'name': 'last_name', 'value': 'Фамилия страхователя на русском языке'},
          {'name': 'first_name', 'value': 'Имя страхователя на русском языке'},
          {'name': 'middle_name', 'value': 'Отчество страхователя на русском языке'},

          {'name': 'insurance_type', 'value': 'Тип страховки'},

          {'name': 'already_safe', 'value': 'Страхователь застрахован'},
          {'name': 'passport_type', 'value': 'Тип паспорта'},
          {'name': 'passport_birthday', 'value': 'Дата рождения'},
          {'name': 'passport_series', 'value': 'Паспорт, серия'},
          {'name': 'passport_number', 'value': 'Паспорт, номер'},
          {'name': 'fpassport_series', 'value': 'Паспорт, серия'},
          {'name': 'fpassport_number', 'value': 'Паспорт, номер'},
          {'name': 'passport_issued', 'value': 'Паспорт, кем выдан'},
          {'name': 'passport_issued_date', 'value': 'Паспорт, когда выдан'},
          {'name': 'passport_registration', 'value': 'Паспорт, место регистрации'},
        ],
    }

    if request.method == 'POST':

        already_safe = 1 if request.POST.get('already_safe') == '1' else None
        polis_members = []
        for key, value in request.POST.items():
            if key and key.startswith('name_'):
                digit = key.split('_')[-1]
                birthday = request.POST.get('birthday_%s' % digit)
                if value and birthday:
                    polis_members.append({
                        'name': '%s %s' % (request.POST.get('surname_%s' % digit) or '', value),
                        'birthday': str_to_date(birthday),
                    })
                kwargs['fields'].append({
                    'name': key,
                    'value': 'Застрахованный %s. Имя' % digit,
                })
                kwargs['fields'].append({
                    'name': 'surname_%s' % digit,
                    'value': 'Застрахованный %s. Фамилия' % digit,
                })
                kwargs['fields'].append({
                    'name': 'birthday_%s' % digit,
                    'value': 'Застрахованный %s. Дата рождения' % digit,
                })

        order_id = None
        # Заполняем паспортные данные, по ним найдем пользователя
        passport_fields = {
            'series': '',
            'number': '',
            'issued': '',
            'issued_date': '',
            'registration': '',
            'birthday': '',
            'ptype': '1',
        }
        for key in passport_fields.keys():
            passport_fields[key] = request.POST.get('passport_%s' % key)
        if passport_fields['ptype'] == '2':
            passport_fields['series'] = request.POST.get('fpassport_series')
            passport_fields['number'] = request.POST.get('fpassport_number')
        passport = Passport.objects.select_related('shopper').filter(
            series=passport_fields['series'],
            number=passport_fields['number'],
        ).first()
        if not passport:
            passport = Passport()
        for key, value in passport_fields.items():
            if not value:
                continue
            if key in ('birthday', 'issued_date'):
                value = str_to_date(value)
            setattr(passport, key, value)

        passport.save()
        # Заполняем пользователя
        if passport.shopper:
            shopper = passport.shopper
        else:
            shopper = Shopper()
        shopper_fields = {
            'first_name': '',
            'last_name': '',
            'middle_name': '',
            'name': '',
            'phone': '',
            'email': '',
        }
        for key in shopper_fields.keys():
            shopper_fields[key] = request.POST.get(key)
            if not shopper_fields[key]:
                continue
            setattr(shopper, key, shopper_fields[key])
        setattr(shopper, 'name', '%s %s %s' % (
            request.POST.get('last_name') or '',
            request.POST.get('first_name') or '',
            request.POST.get('middle_name') or '',
        ))
        shopper.save()
        request.session['shopper'] = shopper.to_dict()

        passport.shopper = shopper
        passport.save()
        # Заполняем заказ

        ids_products = []
        for key in request.POST.keys():
            if key.startswith('cat_'):
                product_id = request.POST[key]
                if product_id and product_id.isdigit():
                    ids_products.append(product_id)
        products = Products.objects.filter(pk__in=ids_products)

        birthday = passport.birthday.strftime('%Y-%m-%d') if passport.birthday else None
        started = str_to_date(request.POST.get('started'))

        if products:
            ids_purchases = []
            price = 0

            count = 0
            # Галка страховщик +1
            if already_safe:
                count += 1
            # Кол-во застрахованных + n
            count += len(polis_members)

            for product in products:
                price += product.price * count
                purchase = Purchases.objects.create(
                    product_id=product.id,
                    product_name=product.name,
                    product_price=product.min_count, # страховая премия
                    product_code=product.code,
                    product_measure=product.measure,
                    count=count,
                    cost=product.price,
                    shopper=shopper,
                )
                ids_purchases.append(purchase.id)

            markup = get_markup_product(price)
            purchase = Purchases.objects.create(
                product_id=markup.id,
                product_name=markup.name,
                product_price=0,
                product_code=markup.code,
                count=1,
                cost=markup.price,
                shopper=shopper,
            )
            ids_purchases.append(purchase.id)

            order = Orders.objects.create(
                total=float(price) + markup.price,
                shopper=shopper,
                shopper_name=shopper.name,
                shopper_email=shopper.email,
                shopper_phone=shopper.phone,
                shopper_address=passport.registration,
                comments='Паспорт: \nСерия: %s, номер: %s \nДата рождения: %s \nКем выдан: %s, когда выдан: %s' % (
                    passport.series,
                    passport.number,
                    birthday,
                    passport.issued,
                    passport.issued_date.strftime('%Y-%m-%d') if passport.issued_date else None,
                )
            )
            order_id = order.id
            Purchases.objects.filter(pk__in=ids_purchases).update(order=order)

            ptype = request.POST.get('ptype')
            if not ptype or not ptype.isdigit():
                ptype = 1

            cruise = Blocks.objects.filter(pk=request.POST.get('cruise')).first()
            started = cruise.created

            try:
                days = int(cruise.description)
            except ValueError:
                days = 1
            ended = date_plus_days(started, days=days) 

            polis = Polis.objects.create(
                order = order,
                ptype = ptype,
                number = order_id,
                name = '%s %s' % (
                    request.POST.get('last_fname') or '',
                    request.POST.get('first_fname') or '',
                ),
                birthday = birthday,
                insurance_sum = product.min_count,
                insurance_program = product.stock_info,
                from_date = started,
                already_safe = already_safe,
                to_date = ended,
                days=days)
            for polis_member in polis_members:
                PolisMember.objects.create(
                    polis=polis,
                    name=polis_member['name'],
                    birthday=polis_member['birthday'],
                )

        DefaultFeedback(request, **kwargs)

        return redirect('/shop/checkout/?order_id=%s' % order_id)
    template = 'web/thanks.html'

    page = SearchLink(q_string, request, containers)
    context['page'] = page
    context['containers'] = containers

    return render(request, template, context)
