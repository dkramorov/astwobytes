import xlsxwriter

from apps.main_functions.files import full_path
from apps.main_functions.api_helper import open_wb

from apps.site.polis.models import Polis

def polis_report():
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
