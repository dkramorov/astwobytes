# -*- coding:utf-8 -*-
import os
import json
import datetime
import logging
import traceback
import base64

from xml.sax.saxutils import escape
from wsgiref.util import FileWrapper

from django.conf import settings
from django.db.models import Count
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from apps.main_functions.files import full_path, open_file, make_folder, check_path
from apps.main_functions.string_parser import kill_quotes
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

def append2file(fname='log.txt', msg: str = ''):
    """Добавляет текст в файл"""
    with open_file(fname, 'a+', encoding='utf-8') as f:
        f.write(msg)
        f.write('\n')

def base_auth(request):
    """Авторизация
       На хостинге в .htaccess:
       RewriteRule ^(.*)$ /index.wsgi/$1 [QSA,L,E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
       SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1
    """
    http_auth = None
    # Проверка авторизации
    http_auth = request.META.get('HTTP_AUTHORIZATION') or request.META.get('REDIRECT_HTTP_AUTHORIZATION')
    if http_auth:
        auth_type, data = http_auth.split(' ', 1)
        try:
            data = base64.b64decode(data)
            login, passwd = data.decode('utf-8').split(':', 1)
            user = authenticate(username=login, password=passwd)
            logger.info('user is %s' % user)
            if user:
                return True
        except Exception:
            tb = traceback.format_exc()
            logger.error(tb)
            append2file(msg=tb)
    return False

@csrf_exempt
def exchange1c(request):
    """Выгрузка из 1с (прием файлов выгрузки)"""
    try:
        return full_process(request)
    except Exception:
        tb = traceback.format_exc()
        logger.error(tb)
        append2file(msg=tb)
    return HttpResponse('error\n')

def full_process(request):
    """Выгрузка из 1с (прием файлов выгрузки)"""
    print('QUERY STRING: %s' % request.META['QUERY_STRING'])
    print('GET: %s' % (json.dumps(request.GET), ))
    print('POST: %s' % (json.dumps(request.POST), ))
    print('FILES: %s' % (json.dumps(request.FILES), ))
    #print('HEADERS: %s' % request.headers)

    errors = []
    cur_type = None
    cur_mode = None
    cur_filename = None
    result = ''
    isNewFile = 1
    path = 'exchange'
    by = 100

    method = request.method
    logger.info('method: %s' % method)

    if request.GET.get('type'):
        cur_type = kill_quotes(request.GET['type'])
        msg = 'cur_type: %s' % cur_type
        logger.info(msg)
        append2file(msg=msg)
    if request.GET.get('mode'):
        cur_mode = kill_quotes(request.GET['mode'])
        logger.info('cur_mode: %s' % cur_mode)
    if request.GET.get('filename'):
        cur_filename = kill_quotes(request.GET['filename'])
        logger.info('cur_filename: %s' % cur_filename)

    auth = base_auth(request)
    if not auth:
        return HttpResponse('error\n')

    # ---
    # GET
    # ---
    if method == 'GET':
        #############################################
        # A. Начало сеанса
        # "1С:Предприятие" отправляет http-запрос следующего вида:
        # http://<сайт>/<путь> /1c_exchange.php?type=catalog&mode=checkauth
        # В ответе «1С:Предприятие» три строки (используется разделитель строк "\n"):
        # слово "success";
        # имя Cookie;
        # значение Cookie.
        # Примечание. Все последующие запросы со стороны "1С:Предприятия"
        # содержат в заголовке запроса имя и значение Cookie
        #############################################
        if cur_mode == 'checkauth':
            result = 'success\n'
            request.session['exchange'] = 'exchange'
            result += 'cookine_name\ncookie_value\n'

        #############################################
        # B. Запрос параметров от сайта
        # Далее следует запрос следующего вида:
        # http://<сайт>/<путь> /1c_exchange.php?type=catalog&mode=init
        # В ответ система управления сайтом передает две строки:
        # 1. zip=yes, если сервер поддерживает обмен в zip-формате
        # zip=no - в этом случае файлы передаются каждый по отдельности.
        # 2. file_limit=<число>
        # где <число> - максимально допустимый размер файла в байтах за один запрос.
        #############################################
        elif cur_mode == 'init':
            result = 'zip=no\n'
            result += 'file_limit=%s\n' % (250 * 1024 * 1024, )

        elif cur_mode in ('query', 'success'):
            result = 'success\n'

        #############################################
        # C. Получение файла обмена с сайта
        # Затем на сайт отправляется запрос вида
        # http://<сайт>/<путь> /1c_exchange.php?type=sale&mode=query
        # Сайт передает сведения о заказах в формате CommerceML 2.
        # В случае успешного получения и записи заказов
        # "1С:Предприятие" передает на сайт запрос вида
        # http://<сайт>/<путь> /1c_exchange.php?type=sale&mode=success
        #############################################
        if cur_type == 'sale' and cur_mode == 'query':
            # ------------------------------
            # Магазин должен быть установлен
            # ------------------------------
            if not is_shop:
                assert False

            # http://v8.1c.ru/edi/edi_stnd/90/%D0%9B%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5%20%D0%BE%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5%20CommerceML_2.09.pdf
            now = datetime.datetime.today()
            orders = Orders.objects.select_related('shopper').all()
            ids_orders = {}
            for order in orders:
                ids_orders[order.id] = order
            ids_purchases = {}
            purchases = Purchase.objects.filter(order__in=ids_orders.keys())
            for purchase in purchases:
                ids_purchases[purchase.price_id] = purchase
                if not hasattr(ids_orders[purchase.order_id], 'purchases'):
                    ids_orders[purchase.order_id].purchases = []
                purchase.info = purchase.get_info()
                purchase.total = purchase.total()
                ids_orders[purchase.order_id].purchases.append(purchase)
            # ------------
            # TODO: рефакторинг
            # Достаем коды
            # ------------
            prices_codes = TMPExchange.objects.filter(pk_db__in=ids_purchases.keys(), ctype=2)
            for item in prices_codes:
                ids_purchases[item.pk_db].code = item.pk_xml
            cat_codes = TMPExchange.objects.filter(pk_db__in=ids_purchases.keys(), ctype=2)
            for item in prices_codes:
                ids_purchases[item.pk_db].code = item.pk_xml

            orders_from_site = 'from.xml'
            template = 'exchange_orders_from_site.html'
            # ------------------------
            # Впинываем все по шаблону
            # ------------------------
            c = Context({
                'now': now,
                'orders': orders,
                'request': request,
            })
            content = loader.render_to_string(template, c)
            with open_file(orders_from_site, 'w+', encoding='cp1251') as f:
                content = content.encode('cp1251')
                f.write(content)

            # В конфигураторе, в дереве метаданных развернуть "Обработки". Там найти "ОбменССайтом". Правой кнопкой на ней -> открыть модуль объекта. Там найти процедуру "HTTPЗагрузитьССервера". Поставить точку останова в ней.
#Первым делом просмотреть переменную "СтрокаCML" (или ОтветСервера, если обмен идет без zip архивов) (начиная приблизительно со строчки СтрокаCML = "";, у меня это 85 строка в указанной обработке, у вас номер строки может быть другой).
#Если в нее действительно попадают крякозябры, то дело все-таки в кодировке. Пробуйте меняйте на utf-8 и опять анализируйте.
#Если же не кракозябры а читаемый текст, значит надо идти отладчиком глубже (в процедуру РазобратьCML(), и смотреть где конкретно спотыкается).

            filename = full_path(orders_from_site)
            wrapper = FileWrapper(file(filename))
            # ---------------------
            # Обязательно кодировку
            # ---------------------
            response = HttpResponse(wrapper, content_type='text/plain; charset=windows-1251')
            response['Content-Length'] = os.path.getsize(filename)
            return response

    # ----
    # POST
    # ----
    elif method == 'POST':
        if cur_filename:
            if check_path(path):
                make_folder(path)
            cur_filename = kill_quotes(cur_filename).split('/')[-1]

        #############################################
        # C. Выгрузка на сайт файлов обмена
        # Затем "1С:Предприятие" запросами с параметрами вида
        # 1c_exchange.php?type=catalog&mode=file&filename=<имя файла>
        # выгружает на сайт файлы в CommerceML 2, посылая файл или части в виде POST.
        # В случае успешной записи файла ПУ сайтом выдает строку "success".
        #############################################
        if cur_mode == 'file':
            file_data = request.body
            path_file = os.path.join(path, cur_filename)
            with open_file(path_file, 'wb+') as f:
                f.write(file_data)
            result = 'success\n'

    if method == 'GET':
        #############################################
        # D. Пошаговая загрузка каталога
        # На последнем шаге по запросу из "1С:Предприятия"
        # производится пошаговая загрузка каталога по запросу
        # 1c_exchange.php?type=catalog&mode=import&filename=<имя файла>
        # Во время загрузки ПУ может отвечать в одном из следующих вариантов.
        # 1. Если в первой строке содержится слово "progress"
        # означает необходимость послать тот же запрос еще раз.
        # В этом случае во второй строке будет возвращен
        # текущий статус обработки, объем  загруженных данных, статус импорта
        # 2. Если в ответ передается строка со словом "success"
        # то это будет означать сообщение об успешном окончании обработки файла.
        # Примечание. Если в ходе какого-либо запроса произошла ошибка
        # то в первой строке ответа ПУ сайтом будет содержаться слово "failure"
        # а в следующих строках - описание ошибки
        # Если произошла необрабатываемая ошибка, то будет возвращен html-код.
        if cur_mode == 'import':
            # Мы не будем заставлять 1с ожидать завершения процесса,
            # а запустим его фоном, 1с скажем, что все оки
            result = 'success\n'
            if cur_filename == 'offers.xml':
                Tasks.objects.create(command='exchange1c', description='Выгрузка из 1с')

    logger.info('result: %s' % result)
    return HttpResponse(result)