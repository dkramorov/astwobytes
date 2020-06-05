# -*- coding:utf-8 -*-
import logging
import requests

from django.conf import settings

logger = logging.getLogger('main')

# Usage: ссылки на авторизацию пользователем надо положить в контекст
# context['vk_link'] = VK().get_auth_user_link()
# context['yandex_link'] = Yandex().get_auth_user_link()

class VK:
    def __init__(self, access_token: str = None, user_id: int = None):
        self.oauth_url = 'https://oauth.vk.com'
        self.api_url = 'https://api.vk.com/method/'
        self.api_version = '5.107'
        self.access_token = access_token
        self.user_id = user_id
        self.user_email = None

    def get_auth_user_link(self, scope: str = 'email'):
        """Строим ссылку для авторизации пользователя"""
        url = '%s/authorize' % self.oauth_url
        params = {
            'client_id': settings.VK_OAUTH_APP_ID,
            'display': 'page',
            'redirect_uri': settings.VK_OAUTH_REDIRECT_URL,
            'scope': scope,
            'response_type': 'code',
            'v': self.api_version,
        }
        return '%s?%s' % (url, '&'.join(['%s=%s' % (k, v) for k, v in params.items()]))

    def get_access_token(self, code: str):
        """Получение токена для запросов по коду пользователя"""
        if self.access_token:
            logger.info('token already exists %s' % self.access_token)
            return
        url = '%s/access_token' % self.oauth_url
        params = {
            'client_id': settings.VK_OAUTH_APP_ID,
            'client_secret': settings.VK_OAUTH_SECRET,
            'redirect_uri': settings.VK_OAUTH_REDIRECT_URL,
            'code': code,
        }
        r = requests.get(url, params=params)
        resp = r.json()
        if 'access_token' in resp:
            self.access_token = resp['access_token']
        if 'user_id' in resp:
            self.user_id = resp['user_id']
        return resp

    def user_fields(self):
        """Возвращает все поля пользователя (для запроса)"""
        return 'photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group'

    def api_request(self, method: str = 'users.get', **kwargs):
        """Запрос к апи VK
           :param method: маршрут апи
           :param kwargs: параметры для запроса, например,
                          params = {
                              'user_ids': 210700286,
                              'fields': self.user_fields(),
                          }
        """
        if not self.access_token:
            logger.info('token does not exists')
            return
        url = '%s%s' % (self.api_url, method)
        params = {
            'access_token': self.access_token,
            'v': self.api_version,
        }
        params.update(kwargs)
        r = requests.get(url, params=params)
        resp = r.json()
        return resp['response'][0]

class Yandex:
    def __init__(self, access_token: str = None):
        self.oauth_url = 'https://oauth.yandex.ru'
        self.passport_url = 'https://login.yandex.ru/info'
        self.access_token = access_token

    def get_auth_user_link(self, scope: str = 'email'):
        """Строим ссылку для авторизации пользователя"""
        url = '%s/authorize' % self.oauth_url
        params = {
            'client_id': settings.YANDEX_OAUTH_APP_ID,
            'redirect_uri': settings.YANDEX_OAUTH_REDIRECT_URL,
            'response_type': 'code',
        }
        return '%s?%s' % (url, '&'.join(['%s=%s' % (k, v) for k, v in params.items()]))

    def get_access_token(self, code: str):
        """Получение токена для запросов по коду пользователя"""
        if self.access_token:
            logger.info('token already exists %s' % self.access_token)
            return
        url = '%s/token' % self.oauth_url
        params = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': settings.YANDEX_OAUTH_APP_ID,
            'client_secret': settings.YANDEX_OAUTH_SECRET,
        }
        r = requests.post(url, data=params)
        resp = r.json()
        if 'access_token' in resp:
            self.access_token = resp['access_token']
        return resp

    def passport_request(self, **kwargs):
        """Запрос к апи-паспорта Yandex
           :param kwargs: параметры для запроса
        """
        if not self.access_token:
            logger.info('token does not exists')
            return
        params = {
            'oauth_token': self.access_token,
            'format': 'json',
        }
        params.update(kwargs)
        r = requests.get(self.passport_url, params=params)
        resp = r.json()
        return resp

