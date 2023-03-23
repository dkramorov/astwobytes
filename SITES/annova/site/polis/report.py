import xlsxwriter
import datetime
from django.conf import settings

from apps.shop.sbrf import SberPaymentProvider
from apps.main_functions.files import full_path
from apps.main_functions.api_helper import open_wb

from apps.site.passport.models import Passport
from apps.site.polis.models import Polis, PolisMember, DATE_FORMATTER

class PolisCruisesReport:
    simple_header = [
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
    simple_indexes = {
        k: v for v, k in enumerate([
            'number',
            'surname',
            'first_name',
            'from_date',
            'to_date',
            'birthday',
            'days',
            'program',
            'insurance_limit',
            'currency',
            'country',
            'code',
            'coverage',
            'created',
            'franchise',
            'additional',
        ])
    }
    # --- global Бордеро ---
    global_header = [
        '№',
        'Номер полиса',
        'Дата оформления полиса',
        'Сервисная компания',
        'Фамилия, имя Застрахованного',
        'Дата рождения Застрахованного',
        'Дата начала действия полиса',
        'Дата окончания действия полиса',
        'Количество дней',
        'Страна',
        'Дополнительное условие',
        'Программа страхования',
        'Страховая сумма на каждого (валюта)',
        'Франшиза',
        'Премия (вал)',
        'Программа страхования',
        'Страховая сумма на каждого (валюта)',
        'Программа страхования',
        'Страховая сумма на каждого (валюта)',
        'Валюта',
        'Дополнительная информация',
    ]
    global_indexes = {
        k: v for v, k in enumerate([
            'i',
            'number',
            'created',
            'service_company',
            'fio',
            'birthday',
            'from_date',
            'to_date',
            'days',
            'country',
            'code', # TI
            'program',
            'insurance_limit',
            'franchise',
            'cost', # Премия
            'social_program',
            'social_insurance_limit',
            'law_program',
            'law_insurance_limit',
            'currency',
            'additional',
        ])
    }
    global_header_merge = [
        # col - столбик
        # hsize => +сколько по высоте занимаем
        # wsize => +сколько по ширине занимаем
        # srow => +сколько будем добавлять, чтобы найти стартовую строку
        {'col': 0, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': '№'},
        {'col': 1, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Номер полиса'},
        {'col': 2, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Дата оформления полиса'},
        {'col': 3, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Сервисная компания'},
        {'col': 4, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Фамилия, имя Застрахованного'},
        {'col': 5, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Дата рождения Застрахованного'},
        {'col': 6, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Дата начала действия полиса'},
        {'col': 7, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Дата окончания действия полиса'},
        {'col': 8, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Количество дней'},
        {'col': 9, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Страна'},
        {'col': 10, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Дополнительное условие'},
        {'col': 11, 'srow': 0, 'hsize': 1, 'wsize': 7, 'name': 'Информация по рискам'},
        {'col': 11, 'srow': 1, 'hsize': 0, 'wsize': 3, 'name': 'Медицинские и иные расходы'},
        {'col': 15, 'srow': 1, 'hsize': 0, 'wsize': 1, 'name': 'Гражданская ответственность'},
        {'col': 17, 'srow': 1, 'hsize': 0, 'wsize': 1, 'name': 'Юридическая помощь'},
        {'col': 19, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Валюта'},
        {'col': 20, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Дополнительная информация'},
    ]
    # --- DSU Бордеро ---
    dsu_header = [
        '№',
        'Номер договора страхования',
        'Дата заключения договора',
        'Сервисная компания',
        'Тип страхователя',
        'оргформа',
        'наименование',
        'ИНН',
        'ОГРН',
        'ОКВЭД',
        'адрес',
        'фамилия',
        'имя',
        'отчество',
        'дата рождения',
        'вид документа',
        'серия документа',
        'номер документа',
        'адрес',
        'фамилия',
        'имя',
        'дата рождения',
        'Дата начала периода страхования',
        'Дата окончания периода страхования',
        'Количество дней',
        'Вариант действия договора страхования',
        'Страна',
        'Программа страхования',
        'Страховая сумма (валюта)',
        'Страховая премия (валюта)',
        'тип',
        'тип значения',
        'франшиза',
        'Программа страхования',
        'Страховая сумма (валюта)',
        'Страховая премия (валюта)',
        'тип',
        'тип значения',
        'франшиза',
        'Валюта договора',
        'Общая премия (валюта)',
        'Общая премия (рубли)',
        'Код вида деятельности',
        'наименование',
        'Комментарии',
    ]
    dsu_indexes = {
        k: v for v, k in enumerate([
            'i',
            'number',
            'created',
            'service_company',
            'insurance_person_type',
            'law_orgform',
            'law_name',
            'law_inn',
            'law_ogrn',
            'law_okved',
            'law_address',
            'main_surname',
            'main_first_name',
            'main_middle_name',
            'main_birthday',
            'doc_type',
            'doc_series',
            'doc_number',
            'address',
            'surname',
            'first_name',
            'birthday',
            'from_date',
            'to_date',
            'days',
            'variant',
            'country',
            'program',
            'insurance_sum',
            'cost',
            'franchise_type',
            'franchise_value_type',
            'franchise',
            'cancel_program',
            'cancel_insurance_sum',
            'cancel_cost',
            'cancel_franchise_type',
            'cancel_franchise_value_type',
            'cancel_franchise',
            'currency',
            'total_cost',
            'total_cost_rub',
            'additional_code',
            'additional_name',
            'additional_comments',
        ])
    }
    dsu_header_merge = [
        # col - столбик
        # hsize => +сколько по высоте занимаем
        # wsize => +сколько по ширине занимаем
        # srow => +сколько будем добавлять, чтобы найти стартовую строку
        {'col': 0, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': '№'},
        {'col': 1, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Номер договора страхования'},
        {'col': 2, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Дата заключения договора страхования'},
        {'col': 3, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Сервисная компания'},
        {'col': 4, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Тип Страхователя'},
        {'col': 5, 'srow': 0, 'hsize': 0, 'wsize': 13, 'name': 'Страхователь'},
        {'col': 19, 'srow': 0, 'hsize': 1, 'wsize': 2, 'name': 'Застрахованное лицо'},
        {'col': 22, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Дата начала периода страхования'},
        {'col': 23, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Дата окончания периода страхования'},
        {'col': 24, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Количество дней'},
        {'col': 25, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Вариант действия договора страхования'},
        {'col': 26, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Страна'},
        {'col': 27, 'srow': 0, 'hsize': 0, 'wsize': 5, 'name': 'Медицинские и иные расходы'},
        {'col': 33, 'srow': 0, 'hsize': 0, 'wsize': 5, 'name': 'Отмена поездки'},
        {'col': 39, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Валюта договора'},
        {'col': 40, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Общая премия (валюта)'},
        {'col': 41, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Общая премия (рубли)'},
        {'col': 42, 'srow': 0, 'hsize': 1, 'wsize': 1, 'name': 'Дополнительное условие'},
        {'col': 44, 'srow': 0, 'hsize': 2, 'wsize': 0, 'name': 'Комментарии'},
        {'col': 5, 'srow': 1, 'hsize': 0, 'wsize': 5, 'name': 'ЮЛ'},
        {'col': 11, 'srow': 1, 'hsize': 0, 'wsize': 7, 'name': 'ФЛ'},
        {'col': 27, 'srow': 1, 'hsize': 1, 'wsize': 0, 'name': 'Программа страхования'},
        {'col': 28, 'srow': 1, 'hsize': 1, 'wsize': 0, 'name': 'Страховая сумма (валюта)'},
        {'col': 29, 'srow': 1, 'hsize': 1, 'wsize': 0, 'name': 'Страховая премия (валюта)'},
        {'col': 30, 'srow': 1, 'hsize': 0, 'wsize': 2, 'name': 'Франшиза (валюта)'},
        {'col': 33, 'srow': 1, 'hsize': 1, 'wsize': 0, 'name': 'Программа страхования'},
        {'col': 34, 'srow': 1, 'hsize': 1, 'wsize': 0, 'name': 'Страховая сумма (валюта)'},
        {'col': 35, 'srow': 1, 'hsize': 1, 'wsize': 0, 'name': 'Страховая премия (валюта)'},
        {'col': 36, 'srow': 1, 'hsize': 0, 'wsize': 2, 'name': 'Франшиза (валюта)'},
    ]

    # --- DSU Бордеро (новый вариант) ---
    dsu_header_hockey = [
        '№',
        'Номер договора страхования (полиса)',
        'Дата подписания договора',

        # ЮЛ
        'Наименование страхователя ЮЛ',
        'Организационно-правовая форма',
        'ИНН страхователя ЮЛ',
        'Адрес страхователя',
        # ФЛ
        'ФИО',
        'Дата рождения',
        'Пол',
        'Гражданство',
        'Тип документа',
        'Серия документа',
        '№ документа',
        'Кем выдан',
        'Дата выдачи документа',
        'Адрес проживания',
        # Застрахованный
        'Фамилия',
        'Имя',
        'Отчество',
        'Дата рождения',
        'Пол',
        'Гражданство',
        'Тип документа',
        'Серия документа',
        '№ документа',
        'Кем выдан документ',
        'Дата выдачи документа',
        'Адрес проживания',
        'Контактный телефон',
        # страховая сумма
        'Смерть Застрахованного лица в результате несчастного случая или болезни',
        'Смерть Застрахованного лица в результате несчастного случая',
        'Смерть Застрахованного лица в результате болезни',
        'Смерть Застрахованного лица в результате дорожно-транспортного происшествия',
        'Смерть Застрахованного лица в результате авиакатастрофы',
        'Смерть Застрахованного лица в результате железнодорожной катастрофы',
        'Смерть Застрахованного лица в результате кораблекрушения',
        'Установление инвалидности Застрахованному лицу в результате несчастного случая или болезни',
        'Установление инвалидности Застрахованному лицу в результате несчастного случая',
        'Установление инвалидности Застрахованному лицу в результате болезни',
        'Постоянная (полная или частичная) утрата профессиональной трудоспособности Застрахованным лицом в результате несчастного случая',
        'Постоянная (полная или частичная) утрата профессиональной трудоспособности Застрахованным лицом в результате профессионального заболевания',
        'Постоянная (полная или частичная) утрата профессиональной трудоспособности Застрахованным лицом в результате болезни',
        'Телесные повреждения (травма) Застрахованного лица в результате несчастного случая',
        'Временная утрата трудоспособности (временное нарушение здоровья) Застрахованного лица в результате несчастного случая или болезни',
        'Временная утрата трудоспособности (временное нарушение здоровья) Застрахованного лица в результате несчастного случая',
        'Временная утрата трудоспособности (временное нарушение здоровья) Застрахованного лица в результате болезни',
        'Хирургическое вмешательство в результате несчастного случая или болезни',
        'Хирургическое вмешательство в результате несчастного случая',
        'Госпитализация (экстренная госпитализация) Застрахованного лица в результате несчастного случая или болезни',
        'Госпитализация (экстренная госпитализация) Застрахованного лица в результате несчастного случая',
        'Госпитализация (экстренная госпитализация) Застрахованного лица в результате болезни',
        'Первичное диагностирование критического заболевания или проведения хирургической операции',
        'Первичное диагностирование инфекционного заболевания',
        'Экстренная профилактика инфекционных заболеваний вследствие укуса клещом',
        'Экстренная профилактика бешенства вследствие укуса животным',

        'Общая страховая премия',
        'Срок оплаты премии',
        'Территория страхования',
        'Время действия',
        'Дата начала',
        'Дата окончания',
    ]
    dsu_indexes_hockey = {
        k: v for v, k in enumerate([
            'i',
            'number',
            'created',
            '', '', '', '', # ЮЛ
            # ФЛ
            'main_name',
            'main_birthday',
            '', # Пол
            '', # Гражданство
            'doc_type',
            'doc_series',
            'doc_number',
            'doc_issued',
            'doc_issued_date',
            'doc_registration',
            # Застрахованный
            'surname',
            'first_name',
            'middle_name',
            'birthday',
            '', # 'Пол'
            '', # 'Гражданство'
            '', # 'Тип документа'
            '', # 'Серия документа'
            '', # '№ документа'
            '', # 'Кем выдан документ'
            '', # 'Дата выдачи документа'
            '', # 'Адрес проживания'
            '', # 'Контактный телефон'
            # страховая сумма
            '', # 'Смерть Застрахованного лица в результате несчастного случая или болезни',
            '', # 'Смерть Застрахованного лица в результате несчастного случая',
            '', # 'Смерть Застрахованного лица в результате болезни',
            '', # 'Смерть Застрахованного лица в результате дорожно-транспортного происшествия',
            '', # 'Смерть Застрахованного лица в результате авиакатастрофы',
            '', # 'Смерть Застрахованного лица в результате железнодорожной катастрофы',
            '', # 'Смерть Застрахованного лица в результате кораблекрушения',
            '', # 'Установление инвалидности Застрахованному лицу в результате несчастного случая или болезни',
            '', # 'Установление инвалидности Застрахованному лицу в результате несчастного случая',
            '', # 'Установление инвалидности Застрахованному лицу в результате болезни',
            '', # 'Постоянная (полная или частичная) утрата профессиональной трудоспособности Застрахованным лицом в результате несчастного случая',
            '', # 'Постоянная (полная или частичная) утрата профессиональной трудоспособности Застрахованным лицом в результате профессионального заболевания',
            '', # 'Постоянная (полная или частичная) утрата профессиональной трудоспособности Застрахованным лицом в результате болезни',
            '', # 'Телесные повреждения (травма) Застрахованного лица в результате несчастного случая',
            '', # 'Временная утрата трудоспособности (временное нарушение здоровья) Застрахованного лица в результате несчастного случая или болезни',
            '', # 'Временная утрата трудоспособности (временное нарушение здоровья) Застрахованного лица в результате несчастного случая',
            '', # 'Временная утрата трудоспособности (временное нарушение здоровья) Застрахованного лица в результате болезни',
            '', # 'Хирургическое вмешательство в результате несчастного случая или болезни',
            '', # 'Хирургическое вмешательство в результате несчастного случая',
            '', # 'Госпитализация (экстренная госпитализация) Застрахованного лица в результате несчастного случая или болезни',
            '', # 'Госпитализация (экстренная госпитализация) Застрахованного лица в результате несчастного случая',
            '', # 'Госпитализация (экстренная госпитализация) Застрахованного лица в результате болезни',
            '', # 'Первичное диагностирование критического заболевания или проведения хирургической операции',
            '', # 'Первичное диагностирование инфекционного заболевания',
            '', # 'Экстренная профилактика инфекционных заболеваний вследствие укуса клещом',
            '', # 'Экстренная профилактика бешенства вследствие укуса животным',
            'order_total',
            '', # 'Срок оплаты премии',
            '', # 'Территория страхования',
            'days', # 'Время действия',
            'from_date',
            'to_date',
        ])
    }
    dsu_header_merge_hockey = [
        # col - столбик
        # hsize => +сколько по высоте занимаем
        # wsize => +сколько по ширине занимаем
        # srow => +сколько будем добавлять, чтобы найти стартовую строку
        {'col': 3, 'srow': 0, 'hsize': 0, 'wsize': 3, 'name': 'Страхователь ЮЛ'},
        {'col': 7, 'srow': 0, 'hsize': 0, 'wsize': 9, 'name': 'Страхователь ФЛ'},
        {'col': 17, 'srow': 0, 'hsize': 0, 'wsize': 12, 'name': 'Застрахованный'},
        {'col': 30, 'srow': 0, 'hsize': 0, 'wsize': 25, 'name': 'Страховая сумма'},
    ]
def polis_report(start_date: datetime.datetime,
                 end_date: datetime.datetime,
                 payed_status: str = None,
                 ptype: str = 'simple'):
    if settings.FULL_SETTINGS_SET.get('REPORT_TYPE') == 'cruises':
        return polis_report_cruises(start_date, end_date, payed_status=payed_status, ptype=ptype)
    return polis_report_hockey(start_date, end_date, ptype=ptype)


def polis_report_cruises(start_date: datetime.datetime,
                         end_date: datetime.datetime,
                         payed_status: str = None,
                         ptype: str = 'simple'):
    """Формирование отчета по полисам
       :param start_date: дата для фильтра от (создание полюса)
       :param end_date: дата для фильтра до (создание полюса)
       :param payed_status: статус оплаты заказа по полюсу 'payed' or 'not_payed'
       :param ptype: тип отчета
    """
    dest = 'report_%s.xlsx' % ptype
    if payed_status:
        dest = 'report_%s_%s.xlsx' % (payed_status, ptype)

    row_number = 0
    header = PolisCruisesReport.simple_header
    indexes = PolisCruisesReport.simple_indexes

    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)
    from_date = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
    to_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    if start_date:
        from_date = start_date
    if end_date:
        to_date = end_date

    if ptype == 'global':
        dest = 'Bordero on %s (Astoria Grande).xlsx' % to_date.strftime('%d-%m-%Y')

    book = xlsxwriter.Workbook(full_path(dest))
    sheet = book.add_worksheet('Лист 1')

    merge_format = book.add_format({'align': 'center'})
    # Формирование шапки
    if ptype == 'global':
        header = PolisCruisesReport.global_header
        indexes = PolisCruisesReport.global_indexes
        merges = PolisCruisesReport.global_header_merge
        for line in (
            'Список застрахованных СК "Согласие"',
            'Компания ассистанс : EVCALYPT GLOBAL',
            'Бордеро',
            'Дата: %s' % to_date.strftime(DATE_FORMATTER),
        ):
            sheet.write(row_number, 0, line)
            row_number += 1
        row_number += 1 # Пустая строка

        # Добавить в шапку мерж ячеек
        for merge in merges:
            sheet.merge_range(
                row_number + merge['srow'], # стартовая строка
                merge['col'], # стартовый столбик
                row_number + merge['srow'] + merge['hsize'], # конечная строка
                merge['col'] + merge['wsize'], # конечный столбик
                merge['name'], # содержимое ячейки
                merge_format,
            )
        row_number += 2 # учет мержей
        #row_number += 1 # Пустая строка
    elif ptype == 'dsu':
        header = PolisCruisesReport.dsu_header
        indexes = PolisCruisesReport.dsu_indexes
        merges = PolisCruisesReport.dsu_header_merge
        for line in ('Приложение №1', ):
            sheet.write(row_number, 0, line)
            row_number += 1

        # Добавить в шапку мерж ячеек
        for merge in merges:
            sheet.merge_range(
                row_number + merge['srow'], # стартовая строка
                merge['col'], # стартовый столбик
                row_number + merge['srow'] + merge['hsize'], # конечная строка
                merge['col'] + merge['wsize'], # конечный столбик
                merge['name'], # содержимое ячейки
                merge_format,
            )
        row_number += 2 # учет мержей

    elif ptype == 'dsu_hockey':
        header = PolisCruisesReport.dsu_header_hockey
        indexes = PolisCruisesReport.dsu_indexes_hockey
        merges = PolisCruisesReport.dsu_header_merge_hockey

        # Добавить в шапку мерж ячеек
        for merge in merges:
            sheet.merge_range(
                row_number + merge['srow'], # стартовая строка
                merge['col'], # стартовый столбик
                row_number + merge['srow'] + merge['hsize'], # конечная строка
                merge['col'] + merge['wsize'], # конечный столбик
                merge['name'], # содержимое ячейки
                merge_format,
            )
        row_number += 1 # Пустая строка

    inc = 0 # для увеличения i
    for i, item in enumerate(header):
        if isinstance(item, (list, tuple)):
            sheet.write(row_number, i + inc, item[0])
            inc += len(item[1]) - 1
            for j, subitem in enumerate(item[1]):
                sheet.write(row_number + 1, j + i, subitem)
        else:
            sheet.write(row_number, i + inc, item)
    row_number += 1

    sber = SberPaymentProvider()

    polises = Polis.objects.select_related('order', 'order__shopper').filter(order__isnull=False, created__gt=from_date, created__lt=to_date).order_by('from_date')
    if payed_status == 'all_payed':
        polises = polises.filter(state=2)

    print('polises count: %s' % len(polises), from_date, to_date)

    i = 0
    for polis in polises:
        order = polis.order
        passport = Passport.objects.filter(shopper=order.shopper).last()

        if payed_status != 'all_payed':
            # Проверяем, что оплачен
            order_status = sber.get_order_status(order.external_number, order.id)
            if order_status['orderStatus'] != 2:
                continue
            else:
                # Обновляем, что оплачен
                Polis.objects.filter(pk=polis.id).update(state=2)
                polis.state = 3 # чтобы отправка произошла
                #if not is_payed:
                #    order.send_email()

        if payed_status == 'payed':
            # отправили уже, если только что обновили, то модель с другим статусом
            if polis.state == 2:
                continue
        else:
            # Если payed - отправили уже (оплачен)
            # Если all - это переотправка всех
            if polis.state == 2:
                if payed_status != 'all_payed':
                    continue

        members = list(polis.polismember_set.all())
        if polis.already_safe:
            member = PolisMember(polis=polis, name=polis.name, birthday=polis.birthday)
            member.is_main = True
            members.insert(0, member)

        main_member = {}
        main_name, main_birthday = order.shopper.name, polis.birthday
        name_parts = main_name.split(' ')
        main_surname, main_first_name, main_middle_name = None, None, None
        for item in name_parts:
            if not item:
                continue
            if item and not main_surname:
                main_surname = item
                continue
            if item and not main_first_name:
                main_first_name = item
                continue
            if item and not main_middle_name:
                main_middle_name = item
                continue

        for member in members:
            name, birthday = member.name, member.birthday
            name_parts = name.split(' ')
            surname, first_name, middle_name = None, None, None
            for item in name_parts:
                if not item:
                    continue
                if item and not surname:
                    surname = item
                    continue
                if item and not first_name:
                    first_name = item
                    continue
                if item and not middle_name:
                    middle_name = item
                    continue
            i += 1
            params = {
                'i': i,
                'is_main': True if hasattr(member, 'is_main') else False,
                'number': polis.get_number7(),
                'order': order,
                'order_total': '%s' % order.total,
                'surname': surname,
                'first_name': first_name,
                'middle_name': middle_name,
                'fio': name,
                'purchases': [{
                    'code': 'G1' if 'G' in purchase.product_code else 'B',
                    'purchase': purchase,
                    'product_price': purchase.product_price,
                    'cost': purchase.cost,
                    'social_program': '-',
                    'social_insurance_limit': '-',
                    'law_program': '-',
                    'law_insurance_limit': '-',
                } for purchase in order.purchases_set.all() if purchase.product_code != 'markup'],
                'from_date': polis.from_date.strftime(DATE_FORMATTER) if polis.from_date else '',
                'to_date': polis.to_date.strftime(DATE_FORMATTER) if polis.to_date else '',
                'birthday': birthday.strftime(DATE_FORMATTER) if birthday else '',
                'days': polis.days,
                'program': '', # В purchase для каждого program = code
                'currency': 'EUR',
                'country': 'WORLD-WIDE',
                'code': 'AL',
                'coverage': '',
                'created': polis.created.strftime(DATE_FORMATTER),
                'franchise': '',
                'franchise_type': '',
                'franchise_value_type': '',
                'additional': '',
                'service_company': 'EVCALYPT GLOBAL',
                'insurance_person_type': 'ФЛ',
                'law_orgform': '',
                'law_name': '',
                'law_inn': '',
                'law_ogrn': '',
                'law_okved': '',
                'law_address': '',
                'doc_type': passport.get_ptype_display(),
                'doc_series': passport.series,
                'doc_number': passport.number,
                'doc_issued': passport.issued,
                'doc_issued_date': passport.issued_date.strftime(DATE_FORMATTER) if passport.issued_date else '',
                'doc_registration': passport.registration,
                'address': '',
                'variant': '',
                'total_cost': '',
                'total_cost_rub': '',
                'additional_name': '',
                'main_name': main_name,
                'main_surname': main_surname,
                'main_first_name': main_first_name,
                'main_middle_name': main_middle_name,
                'main_birthday': main_birthday.strftime(DATE_FORMATTER) if main_birthday else '',
            }

            row_number = fill_polis_row(
                indexes=indexes,
                row_number=row_number,
                sheet=sheet,
                ptype=ptype,
                params=params,
            )

    book.close()
    return dest

def fill_polis_row(indexes, row_number, sheet, ptype: str, params: dict):
    """Заполнение строчки полюса в xlsx
       :param indexes: индексы заголовков
       :param row_number: номер строчки
       :param sheet: лист xlsx
       :param ptype: тип полюса
       :param params: нужные параметры для заполнения полюса
    """
    if ptype == 'simple':
        for purchase in params['purchases']:
            sheet.write(row_number, indexes['number'], params['number'])
            sheet.write(row_number, indexes['surname'], params['surname'])
            sheet.write(row_number, indexes['first_name'], params['first_name'])
            sheet.write(row_number, indexes['from_date'], params['from_date'])
            sheet.write(row_number, indexes['to_date'], params['to_date'])
            sheet.write(row_number, indexes['birthday'], params['birthday'])
            sheet.write(row_number, indexes['days'], params['days'])
            sheet.write(row_number, indexes['program'], purchase['code'])
            sheet.write(row_number, indexes['insurance_limit'], purchase['product_price'])
            sheet.write(row_number, indexes['currency'], params['currency'])
            sheet.write(row_number, indexes['country'], params['country'])
            sheet.write(row_number, indexes['code'], params['code'])
            sheet.write(row_number, indexes['coverage'], params['coverage'])
            sheet.write(row_number, indexes['created'], params['created'])
            sheet.write(row_number, indexes['franchise'], params['franchise'])
            sheet.write(row_number, indexes['additional'], params['additional'])
            row_number += 1
    elif ptype == 'global':
        for purchase in params['purchases']:
            if purchase['code'] != 'B':
                continue
            sheet.write(row_number, indexes['i'], params['i'])
            sheet.write(row_number, indexes['number'], params['number'])
            sheet.write(row_number, indexes['created'], params['created'])
            sheet.write(row_number, indexes['service_company'], params['service_company'])
            sheet.write(row_number, indexes['fio'], params['fio'])
            sheet.write(row_number, indexes['birthday'], params['birthday'])
            sheet.write(row_number, indexes['from_date'], params['from_date'])
            sheet.write(row_number, indexes['to_date'], params['to_date'])
            sheet.write(row_number, indexes['days'], params['days'])
            sheet.write(row_number, indexes['country'], params['country'])
            sheet.write(row_number, indexes['code'], params['code'])
            sheet.write(row_number, indexes['program'], purchase['code'])
            sheet.write(row_number, indexes['insurance_limit'], purchase['product_price'])
            sheet.write(row_number, indexes['franchise'], params['franchise'])
            sheet.write(row_number, indexes['cost'], purchase['cost'])
            sheet.write(row_number, indexes['social_program'], purchase['social_program'])
            sheet.write(row_number, indexes['social_insurance_limit'], purchase['social_insurance_limit'])
            sheet.write(row_number, indexes['law_program'], purchase['law_program'])
            sheet.write(row_number, indexes['law_insurance_limit'], purchase['law_insurance_limit'])

            sheet.write(row_number, indexes['currency'], params['currency'])
            sheet.write(row_number, indexes['additional'], params['additional'])
            row_number += 1
    elif ptype == 'dsu':
        total = {'b': 0, 'g1': 0}
        for purchase in params['purchases']:
            purchase_cost = purchase['cost']
            product_price = purchase['product_price'] or 0
            if purchase['code'] == 'B' and not total['b']:
                total['b'] += purchase_cost
            elif purchase['code'] == 'G1' and not total['g1']:
                total['g1'] += purchase_cost

            sheet.write(row_number, indexes['i'], params['i'])
            sheet.write(row_number, indexes['number'], params['number'])
            sheet.write(row_number, indexes['created'], params['created'])
            sheet.write(row_number, indexes['service_company'], params['service_company'])
            sheet.write(row_number, indexes['insurance_person_type'], params['insurance_person_type'])
            sheet.write(row_number, indexes['law_orgform'], params['law_orgform'])
            sheet.write(row_number, indexes['law_name'], params['law_name'])
            sheet.write(row_number, indexes['law_inn'], params['law_inn'])
            sheet.write(row_number, indexes['law_ogrn'], params['law_ogrn'])
            sheet.write(row_number, indexes['law_okved'], params['law_okved'])
            sheet.write(row_number, indexes['law_address'], params['law_address'])
            sheet.write(row_number, indexes['main_surname'], params['main_surname'])
            sheet.write(row_number, indexes['main_first_name'], params['main_first_name'])
            sheet.write(row_number, indexes['main_middle_name'], params['main_middle_name'])
            sheet.write(row_number, indexes['main_birthday'], params['main_birthday'])
            #if params['is_main']: # - по сути его паспорт
            sheet.write(row_number, indexes['doc_type'], params['doc_type'])
            sheet.write(row_number, indexes['doc_series'], params['doc_series'])
            sheet.write(row_number, indexes['doc_number'], params['doc_number'])

            sheet.write(row_number, indexes['address'], params['address'])
            sheet.write(row_number, indexes['surname'], params['surname'])
            sheet.write(row_number, indexes['first_name'], params['first_name'])
            sheet.write(row_number, indexes['birthday'], params['birthday'])
            sheet.write(row_number, indexes['from_date'], params['from_date'])
            sheet.write(row_number, indexes['to_date'], params['to_date'])
            sheet.write(row_number, indexes['days'], params['days'])
            sheet.write(row_number, indexes['variant'], params['variant'])
            sheet.write(row_number, indexes['country'], params['country'])
            if 'G' not in purchase['code']:
                sheet.write(row_number, indexes['program'], purchase['code'])
                sheet.write(row_number, indexes['insurance_sum'], product_price)
                sheet.write(row_number, indexes['cost'], purchase_cost)
            sheet.write(row_number, indexes['franchise_type'], params['franchise_type'])
            sheet.write(row_number, indexes['franchise_value_type'], params['franchise_value_type'])
            sheet.write(row_number, indexes['franchise'], params['franchise'])
            if 'G' in purchase['code']:
                sheet.write(row_number, indexes['cancel_program'], purchase['code'])
                sheet.write(row_number, indexes['cancel_insurance_sum'], product_price)
                sheet.write(row_number, indexes['cancel_cost'], purchase_cost)
            sheet.write(row_number, indexes['cancel_franchise_type'], params['franchise_type'])
            sheet.write(row_number, indexes['cancel_franchise_value_type'], params['franchise_value_type'])
            sheet.write(row_number, indexes['cancel_franchise'], params['franchise'])
            sheet.write(row_number, indexes['currency'], params['currency'])
            sheet.write(row_number, indexes['total_cost'], total['g1'] + total['b'])
            sheet.write(row_number, indexes['total_cost_rub'], params['total_cost_rub'])
            sheet.write(row_number, indexes['additional_code'], params['code'])
            sheet.write(row_number, indexes['additional_name'], params['additional_name'])
            sheet.write(row_number, indexes['additional_comments'], params['additional'])
        # Тут по-дурацки - сначала все покупки обходим т/к в одной строчке продукты
        row_number += 1

    elif ptype == 'dsu_hockey':
        total = {'b': 0, 'g1': 0}
        for purchase in params['purchases']:
            purchase_cost = purchase['cost']
            product_price = purchase['product_price'] or 0
            if purchase['code'] == 'B' and not total['b']:
                total['b'] += purchase_cost
            elif purchase['code'] == 'G1' and not total['g1']:
                total['g1'] += purchase_cost

            sheet.write(row_number, indexes['i'], params['i'])
            sheet.write(row_number, indexes['number'], params['number'])
            sheet.write(row_number, indexes['created'], params['created'])

            # ФЛ
            sheet.write(row_number, indexes['main_name'], params['main_name'])
            sheet.write(row_number, indexes['main_birthday'], params['main_birthday'])
            sheet.write(row_number, indexes['doc_type'], params['doc_type'])
            sheet.write(row_number, indexes['doc_series'], params['doc_series'])
            sheet.write(row_number, indexes['doc_number'], params['doc_number'])
            sheet.write(row_number, indexes['doc_issued'], params['doc_issued'])
            sheet.write(row_number, indexes['doc_issued_date'], params['doc_issued_date'])
            sheet.write(row_number, indexes['doc_registration'], params['doc_registration'])

            # Застрахованный
            sheet.write(row_number, indexes['surname'], params['surname'])
            sheet.write(row_number, indexes['first_name'], params['first_name'])
            sheet.write(row_number, indexes['middle_name'], params['middle_name'])
            sheet.write(row_number, indexes['birthday'], params['birthday'])

            #if 'G' not in purchase['code']:
            #    sheet.write(row_number, indexes['program'], purchase['code'])
            #    sheet.write(row_number, indexes['insurance_sum'], product_price)
            #    sheet.write(row_number, indexes['cost'], purchase_cost)
            #if 'G' in purchase['code']:
            #    sheet.write(row_number, indexes['cancel_program'], purchase['code'])
            #    sheet.write(row_number, indexes['cancel_insurance_sum'], product_price)
            #    sheet.write(row_number, indexes['cancel_cost'], purchase_cost)

            sheet.write(row_number, indexes['order_total'], params['order_total'])
            sheet.write(row_number, indexes['days'], params['days'])
            sheet.write(row_number, indexes['from_date'], params['from_date'])
            sheet.write(row_number, indexes['to_date'], params['to_date'])

        # Тут по-дурацки - сначала все покупки обходим т/к в одной строчке продукты
        row_number += 1
    return row_number

def polis_report_hockey(start_date, end_date, ptype: str = 'simple'):
    """Формирование отчета по полисам"""
    dest = 'report_%s.xlsx' % ptype

    row_number = 0
    header = PolisCruisesReport.simple_header
    indexes = PolisCruisesReport.simple_indexes

    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)
    from_date = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
    to_date = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    if start_date:
        from_date = start_date
    if end_date:
        to_date = end_date

    if ptype == 'global':
        dest = 'Bordero on %s (Astoria Grande).xlsx' % to_date.strftime('%d-%m-%Y')

    book = xlsxwriter.Workbook(full_path(dest))
    sheet = book.add_worksheet('Лист 1')

    merge_format = book.add_format({'align': 'center'})
    # Формирование шапки
    if ptype == 'global':
        header = PolisCruisesReport.global_header
        indexes = PolisCruisesReport.global_indexes
        merges = PolisCruisesReport.global_header_merge
        for line in (
            'Список застрахованных СК "Согласие"',
            'Компания ассистанс : EVCALYPT GLOBAL',
            'Бордеро',
            'Дата: %s' % to_date.strftime(DATE_FORMATTER),
        ):
            sheet.write(row_number, 0, line)
            row_number += 1
        row_number += 1 # Пустая строка

        # Добавить в шапку мерж ячеек
        for merge in merges:
            sheet.merge_range(
                row_number + merge['srow'], # стартовая строка
                merge['col'], # стартовый столбик
                row_number + merge['srow'] + merge['hsize'], # конечная строка
                merge['col'] + merge['wsize'], # конечный столбик
                merge['name'], # содержимое ячейки
                merge_format,
            )
        row_number += 2 # учет мержей
        #row_number += 1 # Пустая строка
    elif ptype == 'dsu':
        header = PolisCruisesReport.dsu_header
        indexes = PolisCruisesReport.dsu_indexes
        merges = PolisCruisesReport.dsu_header_merge
        for line in ('Приложение №1', ):
            sheet.write(row_number, 0, line)
            row_number += 1

        # Добавить в шапку мерж ячеек
        for merge in merges:
            sheet.merge_range(
                row_number + merge['srow'], # стартовая строка
                merge['col'], # стартовый столбик
                row_number + merge['srow'] + merge['hsize'], # конечная строка
                merge['col'] + merge['wsize'], # конечный столбик
                merge['name'], # содержимое ячейки
                merge_format,
            )
        row_number += 2 # учет мержей

    elif ptype == 'dsu_hockey':
        header = PolisCruisesReport.dsu_header_hockey
        indexes = PolisCruisesReport.dsu_indexes_hockey
        merges = PolisCruisesReport.dsu_header_merge_hockey

        # Добавить в шапку мерж ячеек
        for merge in merges:
            sheet.merge_range(
                row_number + merge['srow'], # стартовая строка
                merge['col'], # стартовый столбик
                row_number + merge['srow'] + merge['hsize'], # конечная строка
                merge['col'] + merge['wsize'], # конечный столбик
                merge['name'], # содержимое ячейки
                merge_format,
            )
        row_number += 1 # Пустая строка

    inc = 0 # для увеличения i
    for i, item in enumerate(header):
        if isinstance(item, (list, tuple)):
            sheet.write(row_number, i + inc, item[0])
            inc += len(item[1]) - 1
            for j, subitem in enumerate(item[1]):
                sheet.write(row_number + 1, j + i, subitem)
        else:
            sheet.write(row_number, i + inc, item)
    row_number += 1

    sber = SberPaymentProvider()

    polises = Polis.objects.select_related('order', 'order__shopper').filter(order__isnull=False, created__gt=from_date, created__lt=to_date).order_by('from_date')

    print('polises count: %s' % len(polises), from_date, to_date)

    i = 0
    for polis in polises:
        order = polis.order
        passport = Passport.objects.filter(shopper=order.shopper).last()

        members = list(polis.polismember_set.all())
        if polis.already_safe:
            member = PolisMember(polis=polis, name=polis.name, birthday=polis.birthday)
            member.is_main = True
            members.insert(0, member)

        main_member = {}
        main_name, main_birthday = order.shopper.name or '', polis.birthday
        name_parts = main_name.split(' ')
        main_surname, main_first_name, main_middle_name = None, None, None
        for item in name_parts:
            if not item:
                continue
            if item and not main_surname:
                main_surname = item
                continue
            if item and not main_first_name:
                main_first_name = item
                continue
            if item and not main_middle_name:
                main_middle_name = item
                continue

        for member in members:
            name, birthday = member.name, member.birthday
            name_parts = name.split(' ')
            surname, first_name, middle_name = None, None, None
            for item in name_parts:
                if not item:
                    continue
                if item and not surname:
                    surname = item
                    continue
                if item and not first_name:
                    first_name = item
                    continue
                if item and not middle_name:
                    middle_name = item
                    continue
            i += 1
            params = {
                'i': i,
                'is_main': True if hasattr(member, 'is_main') else False,
                'number': polis.get_number7(),
                'order': order,
                'order_total': '%s' % order.total,
                'surname': surname,
                'first_name': first_name,
                'middle_name': middle_name,
                'fio': name,
                'purchases': [{
                    'code': 'G1' if 'G' in purchase.product_code else 'B',
                    'purchase': purchase,
                    'product_price': purchase.product_price,
                    'cost': purchase.cost,
                    'social_program': '-',
                    'social_insurance_limit': '-',
                    'law_program': '-',
                    'law_insurance_limit': '-',
                } for purchase in order.purchases_set.all() if purchase.product_code != 'markup'],
                'from_date': polis.from_date.strftime(DATE_FORMATTER) if polis.from_date else '',
                'to_date': polis.to_date.strftime(DATE_FORMATTER) if polis.to_date else '',
                'birthday': birthday.strftime(DATE_FORMATTER) if birthday else '',
                'days': polis.days,
                'program': '', # В purchase для каждого program = code
                'currency': 'EUR',
                'country': 'WORLD-WIDE',
                'code': 'AL',
                'coverage': '',
                'created': polis.created.strftime(DATE_FORMATTER),
                'franchise': '',
                'franchise_type': '',
                'franchise_value_type': '',
                'additional': '',
                'service_company': 'EVCALYPT GLOBAL',
                'insurance_person_type': 'ФЛ',
                'law_orgform': '',
                'law_name': '',
                'law_inn': '',
                'law_ogrn': '',
                'law_okved': '',
                'law_address': '',
                'doc_type': passport.get_ptype_display(),
                'doc_series': passport.series,
                'doc_number': passport.number,
                'doc_issued': passport.issued,
                'doc_issued_date': passport.issued_date.strftime(DATE_FORMATTER) if passport.issued_date else '',
                'doc_registration': passport.registration,
                'address': '',
                'variant': '',
                'total_cost': '',
                'total_cost_rub': '',
                'additional_name': '',
                'main_name': main_name,
                'main_surname': main_surname,
                'main_first_name': main_first_name,
                'main_middle_name': main_middle_name,
                'main_birthday': main_birthday.strftime(DATE_FORMATTER) if main_birthday else '',
            }

            row_number = fill_polis_row(
                indexes=indexes,
                row_number=row_number,
                sheet=sheet,
                ptype=ptype,
                params=params,
            )

    book.close()
    return dest
