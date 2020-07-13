# -*- coding:utf-8 -*-
import requests
import uuid

class YandexKassa:
    def __init__(self):
        self.endpoint = 'https://payment.yandex.net/api/v3/'
        self.shopId = 722943
        self.secretKey = 'test_M3t_5kFET-O1WQ8yTL3l7CuTFT37NIFTqCcr-Sk6Z3w'
        self.auth = requests.auth.HTTPBasicAuth(self.shopId, self.secretKey)

    def create_payment(self,
                       domain: str = 'https://localhost:8000',
                       summa: str = '10.00',
                       desc: str = 'тестовая оплата'):
        """Создание нового платежа
           :param summa: сумма заказа
           :param desc: описание заказа
           тестовые карты
           https://kassa.yandex.ru/developers/using-api/testing#test-bank-card
        """
        urla = '%spayments' % self.endpoint
        params = {
            'amount': {
                'value': summa,
                'currency': 'RUB',
            },
           'description': desc,
            'confirmation': {
                'type': 'redirect',
                'return_url': '%s/shop/transactions/success/' % domain,
            },
        }
        headers = {
            'Idempotence-Key': str(uuid.uuid4()),
        }
        r = requests.post(urla, headers=headers, json=params, auth=self.auth)
        resp = r.json()
        return resp

    def get_payment_info(self, payment_id: str):
        """Получить информацию о платеже"""
        urla = '%spayments/%s' % (self.endpoint, payment_id)
        r = requests.get(urla, auth=self.auth)
        resp = r.json()
        return resp

if __name__ == '__main__':
    new_payment = YandexKassa().create_payment()
    print(new_payment['id'], new_payment['confirmation']['confirmation_url'])
    payment_info = YandexKassa().get_payment_info('268eb570-000f-5000-9000-1d6e6a8f4b9a')
    print(payment_info)
