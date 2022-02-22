# -*- coding:utf-8 -*-
import logging
import requests

from django.conf import settings

from apps.shop.models import Orders, Transactions

logger = logging.getLogger('main')

class SberPaymentProvider():
    """Сбербанк эквайринг

       Тестовый личный кабинет - https://3dsec.sberbank.ru/mportal3
       Боевой личный кабинет - https://securepayments.sberbank.ru/mportal3

       https://securepayments.sberbank.ru/wiki/doku.php/integration:api:start
       https://securepayments.sberbank.ru/wiki/doku.php/integration:simple
       https://securepayments.sberbank.ru/wiki/doku.php/mportal3:auth

       Тестовые банковские карты
       https://securepayments.sberbank.ru/wiki/doku.php/test_cards
       VISA:
           Номер карты 	4111 1111 1111 1111
           Дата истечения срока действия 2024/12
           Проверочный код на обратной стороне 123
           3-D Secure veres=y, pares=y
           Проверочный код 3-D Secure 12345678 
    """
    def __init__(self):
        self.api_url = 'https://securepayments.sberbank.ru/payment/rest/'
        if settings.SBRF_DEBUG:
            self.api_url = 'https://3dsec.sberbank.ru/payment/rest/'

        self.username = settings.SBRF_USERNAME_API
        self.password = settings.SBRF_PASSWORD_API
        self.ORDER_STATUSES = {
            0: 'заказ зарегистрирован, но не оплачен',
            1: 'предавторизованная сумма удержана (для двухстадийных платежей)',
            2: 'проведена полная авторизация суммы заказа',
            3: 'авторизация отменена',
            4: 'по транзакции была проведена операция возврата',
            5: 'инициирована авторизация через сервер контроля доступа банка-эмитента',
            6: 'авторизация отклонена',
        }


    def auth_params(self):
        """Параметры для запросов: логин и пароль
        """
        return {
            'userName': self.username,
            'password': self.password,
        }

    def register_do(self, **kwargs):
        """Регистрация заказа
           https://3dsec.sberbank.ru/payment/rest/register.do
        """
        endpoint = 'register.do'
        params = self.auth_params()
        params.update({
            'orderNumber': None, # Номер заказа генерировать должен у нас
            'amount': None, # Сумма возврата в минимальных единицах валюты
            'currency': 643, # Код валюты платежа ISO 4217
            'returnUrl': None, # Перенаправление при успешной оплате
            'failUrl': None, # Перенаправление при неуспешной оплате
            'description': None, # Описание заказа (не более 24 символов)
            'language': 'ru', # Язык в кодировке ISO 639-1
            'pageView': 'DESKTOP', # DESKTOP/MOBILE
            'clientId': '', # Идентификатор клиента в магазине
            'sessionTimeoutSecs': 1200, # Время жизни заказа в секундах
            'email': None, # Адрес электронной почты покупателя
            'phone': None, # Номер телефона клиента (цифры)
        })
        params.update(**kwargs)
        urla = '%s%s' % (self.api_url, endpoint)

        r = requests.get(urla, params=params)
        if not r.status_code == 200:
            logger.info('[ERROR]: sbrf register_do: %s' % r.status_code)
            return {}
        resp = r.json()
        result = {
            'orderId': resp['orderId'], # Номер заказа в платежной системе
            'formUrl': resp['formUrl'], # URL-адрес платёжной формы
            'errorCode': resp.get('errorCode'), # Код ошибки (может не быть)
            'errorMessage': resp.get('errorMessage'),
        }
        return result

    def get_order_status(self, order_id: str, order_number: int = None):
        """Проверка статуса заказа
           :param order_id: Номер заказа в платежной системе
           :param order_number: Номер заказа в магазине
        """
        endpoint = 'getOrderStatusExtended.do'
        params = self.auth_params()
        params.update({
            'orderId': order_id,
            'orderNumber': order_number,
            'language': 'ru', # Язык в кодировке ISO 639-1
        })

        r = requests.get('%s%s' % (self.api_url, endpoint), params=params)
        if not r.status_code == 200:
            logger.info('[ERROR]: sbrf get_order_status: %s' % r.status_code)
            return {}
        resp = r.json()
        result = {
            'orderNumber': resp.get('orderNumber'), # Номер заказа в магазине
            'orderStatus': resp.get('orderStatus'), # Cостояние заказа в платёжной системе (нет, если заказ не найден)
            'actionCode': resp.get('actionCode'), # Код ответа процессинга
            'actionCodeDescription': resp.get('actionCodeDescription'),
            'errorCode': resp.get('errorCode'), # Код ошибки (может не быть)
            'errorMessage': resp.get('errorMessage'),
            'amount': resp.get('amount'), # Сумма в минимальных единицах валюты
            'currency': resp.get('currency'), # Код валюты платежа ISO 4217
            'date': resp.get('date'), # Дата регистрации заказа (POSIX)
            'depositedDate': resp.get('depositedDate'), # Дата оплаты (POSIX)
            'orderDescription': resp.get('orderDescription'), # Описание заказа
            'ip': resp.get('ip'), # IP-адрес покупателя (может IPv6)
            'authRefNum': resp.get('authRefNum'), # Номер авторизации платежа
            'refundedDate': resp.get('refundedDate'), # Дата возврата средств
            'paymentWay': resp.get('paymentWay'), # Способ платежа
            # Вложенные списки:
            'cardAuthInfo': resp.get('cardAuthInfo'),
            'secureAuthInfo': resp.get('secureAuthInfo'),
            'bindingInfo': resp.get('bindingInfo'),
            'paymentAmountInfo': resp.get('paymentAmountInfo'),
            'bankInfo': resp.get('bankInfo'),
            'payerData': resp.get('payerData'),
            'refunds': resp.get('refunds'), # Информация по возвратам
        }
        if 'orderStatus' in result and result['orderStatus']:
            status = int(result['orderStatus'])
            result['status'] = self.ORDER_STATUSES.get(status)
            self.process_order_status(order_id, result)
        return result

    def process_order_status(self, order_id: str, order_status: dict):
        """Обновить статус заказа в магазине
           :param order_id: Номер заказа в платежной системе
           :param order_status: результат от get_order_status
        """
        if not 'orderStatus' in order_status:
            return
        if order_status['orderStatus'] == 2:
            order = Orders.objects.filter(external_number=order_id).first()
            if order and not order.payed:
                amount = order_status['amount']
                Orders.objects.filter(pk=order.id).update(payed=amount/100)
