# -*- coding:utf-8 -*-
import os
import datetime
import logging
from xml.sax.saxutils import escape

from django.conf import settings
from django.db.models import Count

from apps.main_functions.files import full_path
from apps.personal.models import Shopper
from apps.products.models import Products

from apps.shop.models import Orders, Purchases

logger = logging.getLogger('main')

def create_orders_xml(dest: str = 'orders.xml',
                      scheme_version: str = '2.03'):
    """Создание xml с заказами
       :param dest: выходной файл (абсолютный путь)
       :param scheme_version: версия схемы xml
    """
    now = datetime.datetime.today()
    content = '<?xml version="1.0" encoding="UTF-8"?>'
    content += '\n<КоммерческаяИнформация ВерсияСхемы="%s" ДатаФормирования="%s">\n' % (scheme_version, now.strftime('%Y-%m-%d %H:%M:%S'))

    by = 50
    tab = '  '

    query = Orders.objects.select_related('shopper').all()
    total_records = query.aggregate(Count('id'))['id__count']
    pages = int(total_records / by) + 1
    for i in range(pages):
        orders = query[i*by:i*by+by]
        for order in orders:
            content += fill_document(order)

    content += '\n</КоммерческаяИнформация>'

    if not dest.startswith('/'):
        dest = full_path(dest)

    with open(dest, 'w+', encoding='utf-8') as f:
        f.write(content)

def get_base_unit(measure: str):
    """Базовая единица измерения
       По классификатору ОКЕИ
    """
    return {
        'id': 796, # Код
        'code': 'PCE', # МеждународноеСокращение
        'name': 'шт', # НаименованиеПолное
        'text': 'Штука',
    }

def fill_document_product(purchase: dict, tab: str = '  '):
    """Заполнение товара в xml
       :param purchase: словарь с товаром заказа
    """
    content = []
    tab3 = tab * 3
    tab4 = tab * 4
    tab5 = tab * 5
    tab6 = tab * 6
    content.append('%s<Товар>' % tab3)
    content.append('%s<Ид>%s</Ид>' % (tab4, purchase['id']))
    content.append('%s<Артикул>%s</Артикул>' % (tab4, purchase['code']))
    content.append('%s<Наименование>%s</Наименование>' % (tab4, escape(purchase['name'])))
    measure = get_base_unit(purchase['measure'])
    content.append('%s<БазоваяЕдиница Код="%s" НаименованиеПолное="%s" МеждународноеСокращение="%s">%s</БазоваяЕдиница>' % (tab4, measure['id'], measure['text'], measure['code'], measure['name']))
    content.append('%s<ЦенаЗаЕдиницу>%s</ЦенаЗаЕдиницу>' % (tab4, purchase['cost']))
    content.append('%s<Количество>%s</Количество>' % (tab4, purchase['count']))
    content.append('%s<Сумма>%s</Сумма>' % (tab4, purchase['total']))

    content.append('%s<ЗначенияРеквизитов>' % tab4)
    content.append('%s<ЗначениеРеквизита>' % tab5)
    content.append('%s<Наименование>ВидНоменклатуры</Наименование>' % tab6)
    content.append('%s<Значение>Товар</Значение>' % tab6)
    content.append('%s</ЗначениеРеквизита>' % tab5)
    content.append('%s<ЗначениеРеквизита>' % tab5)
    content.append('%s<Наименование>ТипНоменклатуры</Наименование>' % tab6)
    content.append('%s<Значение>Товар</Значение>' % tab6)
    content.append('%s</ЗначениеРеквизита>' % tab5)
    content.append('%s</ЗначенияРеквизитов>' % tab4)

    content.append('%s</Товар>' % tab3)
    return content

def fill_document(order, tab: str = '  '):
    """Заполняет заказа в xml
       :param order: Orders model instance
    """
    content = []
    tab2 = tab * 2
    tab3 = tab * 3
    tab4 = tab * 4
    tab5 = tab * 5
    tab6 = tab * 6
    content.append('%s<Документ>' % tab)

    content.append('%s<Ид>%s</Ид>' % (tab2, order.id))
    content.append('%s<Номер>%s</Номер>' % (tab2, order.number or order.id))
    content.append('%s<Дата>%s</Дата>' % (tab2, order.created.strftime('%d.%m.%Y %H:%M:%S')))
    content.append('%s<ХозОперация>Заказ товара</ХозОперация>' % tab2)
    content.append('%s<Роль>Продавец</Роль>' % tab2)
    content.append('%s<Валюта>RUB</Валюта>' % tab2)
    content.append('%s<Курс>1.0000</Курс>' % tab2)
    content.append('%s<Сумма>%s</Сумма>' % (tab2, order.total))
    content.append('%s<Время>%s</Время>' % (tab2, order.created.strftime('%d.%m.%Y %H:%M:%S')))
    content.append('%s<Комментарий>%s</Комментарий>' % (tab2, order.comments))

    # Контрагент
    content.append('%s<Контрагент>' % tab2)
    content.append('%s<Ид>%s</Ид>' % (tab3, order.shopper.id if order.shopper else 0))
    content.append('%s<Наименование>%s</Наименование>' % (tab3, order.shopper_name))
    content.append('%s<Роль>Покупатель</Роль>' % tab3)
    content.append('%s<ПолноеНаименование>%s</ПолноеНаименование>' % (tab3, order.shopper_name))

    # АдресРегистрации
    content.append('%s<АдресРегистрации>' % tab3)
    content.append('%s<Представление>%s</Представление>' % (tab4, order.shopper_address))

    # Контакты
    content.append('%s<Контакты>' % tab4)

    content.append('%s<Контакт>' % tab5)
    content.append('%s<Тип>Почта</Тип>' % tab6)
    content.append('%s<Значение>%s</Значение>' % (tab6, order.shopper_email))
    content.append('%s</Контакт>' % tab5)

    content.append('%s<Контакт>' % tab5)
    content.append('%s<Тип>Телефон</Тип>' % tab6)
    content.append('%s<Значение>%s</Значение>' % (tab6, order.shopper_phone))
    content.append('%s</Контакт>' % tab5)

    content.append('%s</Контакты>' % tab4)

    content.append('%s</АдресРегистрации>' % tab3)

    content.append('%s</Контрагент>' % tab2)
    purchases = order.get_purchases()
    content.append('%s<Товары>' % tab2)
    for purchase in purchases:
        content += fill_document_product(purchase)
    content.append('%s</Товары>' % tab2)

    content.append('%s</Документ>' % tab)
    return '\n'.join(content)



