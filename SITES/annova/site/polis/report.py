import xlsxwriter
import datetime
from django.conf import settings

from apps.shop.sbrf import SberPaymentProvider
from apps.main_functions.files import full_path
from apps.main_functions.api_helper import open_wb

from apps.site.polis.models import Polis

def polis_report():
    if settings.FULL_SETTINGS_SET.get('REPORT_TYPE') == 'cruises':
        return polis_report_cruises()
    return polis_report_hockey()


def polis_report_cruises():
    """Формирование отчета по полисам"""
    dest = 'report.xlsx'
    book = xlsxwriter.Workbook(full_path(dest))
    sheet = book.add_worksheet('Лист 1')

    row_number = 0
    header = [
        'Policy № / Номер полиса',
        'Surname of the patient /Фамилия застрахованного',
        'Name of the patient /Имя застрахованного',
        'Policy starts /Начало действия полиса',
        'Policy expires /Окончание действия полиса',
        'Date of Birth /Дата рождения застрахованного',
        'Days / Количество дней',
        'Insurance program /Программа страхования',
        'Insurance limit /Лимит покрытия',
        'Currency of the policy /Валюта договора',
        'Territory of coverage /Территория действия полиса',
        'Code /Код',
        'Coverage option /Вариант действия полиса',
        'Date of issue /Дата оформления',
        'Deductible /Франшиза',
        'Additional information /Дополнительная информация',
    ]
    indexes = {
        'number': 0,
        'surname': 1,
        'first_name': 2,
        'from_date': 3,
        'to_date': 4,
        'birthday': 5,
        'days': 6,
        'program': 7,
        'insurance_limit': 8,
        'currency': 9,
        'country': 10,
        'code': 11,
        'coverage': 12,
        'created': 13,
        'franchise': 14,
        'additional': 15,
    }
    inc = 0 # для увеличения i
    for i, item in enumerate(header):
        if isinstance(item, (list, tuple)):
            sheet.write(row_number, i + inc, item[0])
            inc += len(item[1]) - 1
            for j, subitem in enumerate(item[1]):
                sheet.write(row_number + 1, j + i, subitem)
        else:
            sheet.write(row_number, i + inc, item)
    row_number +=2

    sber = SberPaymentProvider()
    now = datetime.datetime.now()
    prev_week = now - datetime.timedelta(days=7)
    polises = Polis.objects.select_related('order__shopper', 'order').filter(order__isnull=False, created__gt=prev_week)
    print('polises count: %s' % len(polises))
    for polis in polises:
        order = polis.order
        # Проверяем, что оплачен
        order_status = sber.get_order_status(order.external_number, order.id)
        if order_status['orderStatus'] != 2:
            continue

        ind = indexes['number']
        zfill7 = 7 - len('%s' % polis.id)
        number = '0002114-%s%s/22МП' % ('0' * zfill7, polis.number)
        sheet.write(row_number, ind, number)

        name_parts = polis.name.split(' ')
        surname, first_name = None, None
        for item in name_parts:
            if item and not surname:
                surname = item
                continue
            if item and not first_name:
                first_name = item

        for purchase in order.purchases_set.all():
            if purchase.product_code == 'markup':
                continue
            code = 'B'
            if 'G' in purchase.product_code:
                code = 'G1'

            ind = indexes['surname']
            sheet.write(row_number, ind, surname)

            ind = indexes['first_name']
            sheet.write(row_number, ind, first_name)

            ind = indexes['from_date']
            sheet.write(row_number, ind, polis.from_date.strftime('%Y-%m-%d') if polis.from_date else '')

            ind = indexes['to_date']
            sheet.write(row_number, ind, polis.to_date.strftime('%Y-%m-%d') if polis.to_date else '')

            ind = indexes['birthday']
            sheet.write(row_number, ind, polis.birthday.strftime('%d-%m-%Y'))

            ind = indexes['days']
            sheet.write(row_number, ind, polis.days)

            ind = indexes['program']
            sheet.write(row_number, ind, code)

            ind = indexes['insurance_limit']
            sheet.write(row_number, ind, purchase.product_price)

            ind = indexes['currency']
            sheet.write(row_number, ind, 'EUR')

            ind = indexes['country']
            sheet.write(row_number, ind, 'Турция')

            ind = indexes['code']
            sheet.write(row_number, ind, 'TI')

            ind = indexes['coverage']
            sheet.write(row_number, ind, '')

            ind = indexes['created']
            sheet.write(row_number, ind, polis.created.strftime('%d-%m-%Y'))

            ind = indexes['franchise']
            sheet.write(row_number, ind, '')

            ind = indexes['additional']
            sheet.write(row_number, ind, '')

        #for purchase in polis.order.purchases_set.all():
        #    ind = indexes['insuranse_sum']
        #    sheet.write(row_number, ind, purchase.cost)

        #ind = indexes['insuranse_premium']
        #sheet.write(row_number, ind, polis.insurance_sum)

        row_number += 1

    book.close()


def polis_report_hockey():
    """Формирование отчета по полисам"""
    dest = 'report.xlsx'
    book = xlsxwriter.Workbook(full_path(dest))
    sheet = book.add_worksheet('Лист 1')

    row_number = 0
    header = [
        '№ п.п.',
        'Фамилия Имя Отчество',
        'Дата рождения',
        [
            'Паспортные данные',
            [
                'серия',
                'номер',
                'кем выдан',
                'дата выдачи',
            ],
        ],
        'Адрес места регистрации',
        'Срок страхования',
        'Страховая сумма на одно (каждое) Застрахованное лицо, руб.',
        'Страховая премия на одно (каждое) Застрахованное лицо, руб.',
    ]
    indexes = {
        'number': 0,
        'name': 1,
        'birthday': 2,
        'passport_series': 3,
        'passport_number': 4,
        'passport_issued': 5,
        'passport_issued_date': 6,
        'address': 7,
        'insurance_period': 8,
        'insuranse_sum': 9,
        'insuranse_premium': 10,
    }
    inc = 0 # для увеличения i
    for i, item in enumerate(header):
        if isinstance(item, (list, tuple)):
            sheet.write(row_number, i + inc, item[0])
            inc += len(item[1]) - 1
            for j, subitem in enumerate(item[1]):
                sheet.write(row_number + 1, j + i, subitem)
        else:
            sheet.write(row_number, i + inc, item)
    row_number +=2

    polises = Polis.objects.select_related('order__shopper', 'order').all()
    for polis in polises:
        ind = indexes['number']
        sheet.write(row_number, ind, polis.number)

        ind = indexes['name']
        sheet.write(row_number, ind, polis.name)

        ind = indexes['birthday']
        sheet.write(row_number, ind, polis.birthday.strftime('%d-%m-%Y'))

        ind = indexes['name']
        sheet.write(row_number, ind, polis.name)

        passport = polis.order.shopper.passport_set.all().first()
        ind = indexes['passport_series']
        sheet.write(row_number, ind, passport.series)
        ind = indexes['passport_number']
        sheet.write(row_number, ind, passport.number)
        ind = indexes['passport_issued']
        sheet.write(row_number, ind, passport.issued)
        ind = indexes['passport_issued_date']
        sheet.write(row_number, ind, passport.issued_date.strftime('%d-%m-%Y') if passport.issued_date else '')
        ind = indexes['address']
        sheet.write(row_number, ind, passport.registration)

        ind = indexes['insurance_period']
        from_date = polis.from_date.strftime('%d-%m-%Y') if polis.from_date else ''
        to_date = polis.to_date.strftime('%d-%m-%Y') if polis.to_date else ''
        sheet.write(row_number, ind, '%s - %s' % (from_date, to_date))

        for purchase in polis.order.purchases_set.all():
            ind = indexes['insuranse_sum']
            sheet.write(row_number, ind, purchase.cost)

        ind = indexes['insuranse_premium']
        sheet.write(row_number, ind, polis.insurance_sum)

        row_number += 1

    book.close()
