#-*- coding:utf-8 -*-
import json
import logging
import datetime
import requests

from apps.main_functions.files import open_file, check_path
from apps.main_functions.catcher import json_pretty_print

logger = logging.getLogger(__name__)

"""
  По истечению срока нужно перезапросить access_token по refresh_token
  POST /oauth2/access_token
    client_id ID интеграции
    client_secret Секрет интеграции
    grant_type Тип авторизационных данных (для refresh токена – refresh_token)
    refresh_token Refresh токен
    redirect_uri Redirect URI указанный в настройках интеграции
"""

class AmoCRM:
    def __init__(self, **kwargs):
        """На примере mir-ins.ru
           https://directmir163ru.amocrm.ru
           Документация:
           https://www.amocrm.ru/developers/content/oauth/step-by-step
        """
        self.file = 'amocrm_credentials.txt'
        self.redirect_uri = 'https://mir-ins.ru/amocrm/'
        self.host = 'https://directmir163ru.amocrm.ru'
        self.s = requests.Session()
        self.client_secret = 'Tpi94PsVqnwF7JRoJsi0KnnAG4Od3msqlqzGyflONkl5MZtyfCY5SPMQE49kLaSe'
        self.client_id = 'cd184f47-26b3-4011-9820-83f3ef5232e5'
        # Код из админки для получения access_token
        self.code = 'def502002981f459578c7f343c5e31acfa11de7e642733e27ca945a58e9b66b2ce44b5a993d2569422aa4c1c80d02e2936dfca0981870683e4ad40841cba1f6eff165349e2f8cca73097f970f8e676e0343de5526f1c071ee134b735e65592252e15a9e6ecb9271769c45b2e5f65f67d92d456a056773bdba0fa19f9392b01e7c2c7ea3ac67ccc7b7fafa17a916031cbf49bdee372d7d6544668740aa070500aced0e0d5453d2381cd7f305495670ce828386229fed61a7d86fb23329e8d399869f0eb187aaae39a6b7578049b1d3d9c86cb3277c1ce02c33d8e89d1e342997cceddd48cc93f3fc06f87320e6874b9e17b555003fa5cb153e056900753d79c797fa76e6dc94130d866a5f63e5ea414f239c9afc17c06c847c809ed305678e7d38d1979639c1c3cd36db77e703f93901f21c9998e2b2e4b27273aaaa00a9114e7f8e7faa7fb83938b8838bf368a1ee73b1e7941206c70eab4e3585b48708504ee0345878fc09cd6880fbfcaac65a274ee2024d3da337703c0b45007c8e924132231e98a924a90de2ebc8c9a4d0b50b2e7636a68e030d29fd7a7c2df2b61396cf008c407a3752478cac5cb15871a81c0083b7a78cb645f95ec973aa58e7bc65f2a9392a6ba25'
        self.access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjNjOTY2ZmMxY2NmOGZmMzdmMGFmNzQwNGRmMDc2Njk2MTMwMjNjYWQwMzRhMWNjM2RkZmU5MmJiNjI1MTAxNTE3NWQ2NjAzMzBjOGI5MWJjIn0.eyJhdWQiOiJjZDE4NGY0Ny0yNmIzLTQwMTEtOTgyMC04M2YzZWY1MjMyZTUiLCJqdGkiOiIzYzk2NmZjMWNjZjhmZjM3ZjBhZjc0MDRkZjA3NjY5NjEzMDIzY2FkMDM0YTFjYzNkZGZlOTJiYjYyNTEwMTUxNzVkNjYwMzMwYzhiOTFiYyIsImlhdCI6MTYwNDkxOTk0MywibmJmIjoxNjA0OTE5OTQzLCJleHAiOjE2MDUwMDYzNDMsInN1YiI6Ijk5NTQ0NiIsImFjY291bnRfaWQiOjE5NDgwODEzLCJzY29wZXMiOlsicHVzaF9ub3RpZmljYXRpb25zIiwiY3JtIiwibm90aWZpY2F0aW9ucyJdfQ.a-rejYPPlCmJT4-A8cQZGdaOC3XVBmNugxLcn0hxKGKagndE5Q-PD3q7PhPl2bhJcRhW6EJS1AvB8lao07KqIkj7MZ9nlxI170ily1sivJbKCSyqeL8Rhen6f8Kx2032VD0dWCv2Zwy4eP1m-fpusTdvPwt5eYKmyXo5ig6haH1mwEbM2QRXPXPmMjZLAO6F-T4eKdYJPI2waFYFCWvMm3xhAco4wKfhjmkckRBEPPzaT0aFA3Gi8ivg8SsKfnRzfNgCKxWXHkPPjpj5HuLt5svBYzHUejcHEbq7d_YF3TT0RLN98dmKTrzzkb8B0XYScci9mRIVEZve12tG1UKi7Q'
        self.refresh_token = 'def502006b01bcf4b70f3b4988642c13f5544c079671d0d06bbc68beab4cda5d692370014b059037b13678e51f87d393eeba2a12683c2e874503ae5e0abc7698e335024e635426ce2f25ba2daa5d083758743e0d40a43bb4548aa24d5c190c263b350b29a34c3fe506a911669b92c15ee9562f6d55b2344c2bf74fe977d9d7cb8244f8fe6cf8696a40a26de81e11c8e0aebe2b452bf4e3ccd8822768acb9837dffa175abf8cf9eaf3f5921db5f974d5fda7c26ea2c28e2ad73f67d98c2be4ce666d3dc43b1f8906366778cb367994e29020128caf44f05f63e6b8b1f5266b6533fe0e6456b3529594f3cb08da758f56081363215f04915198af0ccbfa5ab3861382c08eb4a7d3a641dd328dfabe3212421da46f21174ed7d70c6c84e27daabf7be37bb26538920cf1c97b936ea73165a2a0a3612505fd7a4a3e200240d34cf78a20ad5c43c7c4ff10f292eae99c4672cd75d02d6dece6c6b086e9e882e7c45299b2716641ea1c24e6e297562087e126aa07f29445cb45c772d86108b4f9d1a636e98462aac7bd810d2a753561c4892151b6a95094d1da7cd5dfab81b66c036c7e31cd0388874554153ae5ead082b26524a906f0655a605a00fd086051469783e09b7bc81ee2441e180'
        self.headers = {
            'Authorization': 'Bearer %s' % self.access_token
        }

        if not check_path(self.file):
            with open_file(self.file, 'r') as f:
                content = json.loads(f.read())
                self.set_credentials(content)

    def set_credentials(self, credentials: dict):
        """Полученные данные с access_token, refresh_token
           актуализируем в классе
        """
        self.access_token = credentials['access_token']
        self.refresh_token = credentials['refresh_token']
        self.headers = {
            'Authorization': 'Bearer %s' % self.access_token
        }

    def update_access_token(self):
        """Обновление access_token через refresh_token
        """
        endpoint = '/oauth2/access_token'
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'redirect_uri': self.redirect_uri,
        }
        r = self.s.post('%s%s' % (self.host, endpoint), data=params)
        resp = r.json()
        print(json_pretty_print(resp))
        self.set_credentials(resp)
        with open_file(self.file, 'w+') as f:
            f.write(json.dumps(resp))
        return resp

    def get_access_token(self):
        """Получение access_token и refresh_token
           Если 3 мес не пользоваться access_token, то он просрется
           access_token надо обновлять по refresh_token,
           поэтому надо хранить в базе их, потому что тоже просрать легко

           Далее делаем запросы к апи и добавляем к headers
             'Authorization: Bearer ' . $access_token
        """
        endpoint = '/oauth2/access_token'
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': self.code,
            'redirect_uri': self.redirect_uri,
        }
        r = self.s.post('%s%s' % (self.host, endpoint), data=params)
        print(json_pretty_print(r.json()))
        return r.json()

    def get_deals(self, **kwargs):
        """Получить сделки
             with string принимает строку, из нескольких значений, через запятую
                         catalog_elements связанные со сделками элементы списков
                         is_price_modified_by_robot изменен бюджет сделки роботом
                         loss_reason расширенная информация по причине отказа
                         contacts связанные со сделкой контакты
                         only_deleted удаленные сделки в корзину
                         source_id Добавляет в ответ ID источника
             page int Страница выборки
             limit int Количество за один запрос (Максимум – 250)
             query string|int Поисковый запрос
             filter object Фильтр
             order object Сортировка результатов списка
                          created_at, updated_at, id
                          asc, desc
        """
        endpoint = '/api/v4/leads'
        params = {
            'page': 1,
            'limit': 50,
        }
        params = {k: v for k, v in kwargs.items()}
        r = self.s.get('%s%s' % (self.host, endpoint), params=params, headers=self.headers)
        #print(json_pretty_print(r.json()))
        return r.json()

    def get_deal(self, deal_id: int):
        """Получить сделку"""
        endpoint = '/api/v4/leads/%s' % deal_id
        params = {}
        r = self.s.get('%s%s' % (self.host, endpoint), params=params, headers=self.headers)
        print(json_pretty_print(r.json()))
        return r.json()

    def create_deals(self, deals: list):
        """Добавить сделку
           name string Название сделки
           price int Бюджет сделки
           status_id int ID статуса
           pipeline_id int ID воронки
           created_by int ID пользователя, создающий сделку 0=робот
           updated_by int ID пользователя, изменяющий сделку 0=робот
           closed_at int Дата закрытия сделки, передается в Unix Timestamp
           created_at int Дата создания сделки, передается в Unix Timestamp
           updated_at int Дата изменения сделки, передается в Unix Timestamp
           loss_reason_id int ID причины отказа
           responsible_user_id int ID пользователя, ответственного за сделку
           custom_fields_values array Массив по дополнительным полям
                                      _embedded object вложенные теги
                                      _embedded[tags] array|null данные тегов
                                      _embedded[tags][0] object Модель тега id или name
                                      _embedded[tags][0][id] int ID тега
                                      _embedded[tags][0][name] string Название тега
           https://www.amocrm.ru/developers/content/crm_platform/custom-fields#cf-fill-examples

           request_id string вернется в ответе без изменений
           :param deals: список сделок
        """
        endpoint = '/api/v4/leads'
        r = self.s.post('%s%s' % (self.host, endpoint), json=deals, headers=self.headers)
        print(json_pretty_print(r.json()))
        return r.json()

    def get_custom_fields(self, model: str, **kwargs):
        """Получение полей для сделки
        """
        endpoint = '/api/v4/leads/custom_fields'
        models = ('leads', 'contacts')
        if not model in models:
            assert False
        endpoint = '/api/v4/%s/custom_fields' % model
        params = {
            'page': 1,
            'limit': 50,
        }
        params = {k: v for k, v in kwargs.items()}
        r = self.s.get('%s%s' % (self.host, endpoint), headers=self.headers)
        #print(json_pretty_print(r.json()))
        return r.json()

    def create_contacts(self, contacts: list):
        """Добавление контактов
           name string Название контакта
           first_name string Имя контакта
           last_name string Фамилия контакта
           responsible_user_id int ID пользователя, ответственного за контакт
           created_by int ID пользователя, создавший контакт
           updated_by int ID пользователя, изменивший контакт
           created_at int Дата создания контакта, передается в Unix Timestamp
           updated_at int Дата изменения контакта, передается в Unix Timestamp
           custom_fields_values array Массив дополнительных полей
           request_id string Поле, которое вернется вам в ответе без изменений
        """
        endpoint = '/api/v4/contacts'
        r = self.s.post('%s%s' % (self.host, endpoint), json=contacts, headers=self.headers)
        print(json_pretty_print(r.json()))
        return r.json()

    def link_deal2contact(self, deal_id: int, contact_id: int):
        """Привязать сделку к контакту
           to_entity_id int ID связанной сущности
           to_entity_type string Тип связанной сущности (leads, contacts)
           metadata object|null Метаданные связанной сущности
           metadata[catalog_id] int ID каталога
           metadata[quantity] int Количество прикрепленных элементов каталогов
           metadata[is_main] bool Является ли контакт главным
           metadata[updated_by] int ID пользователя, который прикрепил
           :param deal_id: id сделки
           :param contact_id: ид контакта
        """
        endpoint = '/api/v4/leads/%s/link' % deal_id
        params = [{
            'to_entity_id': contact_id,
            'to_entity_type': 'contacts',
        }]
        r = self.s.post('%s%s' % (self.host, endpoint), json=params, headers=self.headers)
        print(json_pretty_print(r.json()))
        return r.json()
