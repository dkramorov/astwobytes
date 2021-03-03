#-*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
import os
import datetime
import logging
from xml.sax.saxutils import escape

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Count

from apps.main_functions.files import full_path
from apps.personal.models import Shopper
from apps.products.models import Products

from apps.shop.models import Orders, Purchases

logger = logging.getLogger('main')

def notify_about_unloading(msg: str = ''):
    """Оповещение о выгрузке через телеграм
    """
    if not settings.TELEGRAM_ENABLED:
        logger.info('TELEGRAM DISABLED')
        return
    from apps.telegram.telegram import TelegramBot
    bot = TelegramBot()
    bot.send_message('Выгрузка заказов %s' % (
        msg,
    ), parse_mode='html', disable_web_page_preview=True)

def create_orders_xml(dest: str = 'orders.xml',
                      scheme_version: str = '2.03'):
    """Создание xml с заказами
       :param dest: выходной файл (абсолютный путь)
       :param scheme_version: версия схемы xml
    """
    now = datetime.datetime.today()
    content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    #content += '\n<КоммерческаяИнформация ВерсияСхемы="%s" ДатаФормирования="%s">\n' % (scheme_version, now.strftime('%Y-%m-%d %H:%M:%S'))

    by = 50
    tab = '  '

    query = Orders.objects.select_related('shopper').all()
    total_records = query.aggregate(Count('id'))['id__count']
    pages = int(total_records / by) + 1
    for i in range(pages):
        orders = query[i*by:i*by+by]
        for order in orders:
            content += fill_document(order) + '\n'

    if not dest.startswith('/'):
        dest = full_path(dest)

    #content += '\n</КоммерческаяИнформация>'

    with open(dest, 'w+', encoding='utf-8') as f:
        f.write(content)

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
    content.append('%s<Код>%s</Код>' % (tab4, purchase['id']))
    content.append('%s<Артикул>%s</Артикул>' % (tab4, purchase['code']))
    content.append('%s<Наименование>%s</Наименование>' % (tab4, escape(purchase['name'])))
    content.append('%s<Количество>%s</Количество>' % (tab4, purchase['count']))
    content.append('%s<Сумма>%s</Сумма>' % (tab4, purchase['total']))

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

    content.append('%s<Код>%s</Код>' % (tab2, order.id))
    content.append('%s<Номер>%s</Номер>' % (tab2, order.number or order.id))
    content.append('%s<Дата>%s</Дата>' % (tab2, order.created.strftime('%d.%m.%Y %H:%M:%S')))
    content.append('%s<Сумма>%s</Сумма>' % (tab2, order.total))
    content.append('%s<Время>%s</Время>' % (tab2, order.created.strftime('%d.%m.%Y %H:%M:%S')))
    content.append('%s<Комментарий>%s</Комментарий>' % (tab2, order.comments))

    purchases = order.get_purchases()
    content.append('%s<Товары>' % tab2)
    for purchase in purchases:
        content += fill_document_product(purchase)
    content.append('%s</Товары>' % tab2)

    content.append('%s</Документ>' % tab)
    return '\n'.join(content)


class Command(BaseCommand):
    """Проверка формирования файла с заказами"""
    def add_arguments(self, parser):
        parser.add_argument('--dest',
            action = 'store',
            dest = 'dest',
            type = str,
            default = False,
            help = 'Set dest file (absolute path)')
    def handle(self, *args, **options):
        dest = 'orders.xml'
        if options.get('dest'):
            dest = options['dest']

        try:
            create_orders_xml(dest=dest)
        except Exception as e:
            notify_about_unloading(str(e))




