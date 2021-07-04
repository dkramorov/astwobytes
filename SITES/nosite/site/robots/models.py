# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

class Robots(Standard):
    """Роботы"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    selenium_version = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    chrome_version = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    ip = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    server_name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    server_free_space = models.IntegerField(blank=True, null=True, db_index=True)
    info = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Роботы - Робот'
        verbose_name_plural = 'Роботы - Роботы'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(Robots, self).save(*args, **kwargs)

class RobotProfiles(Standard):
    """Профили роботов для yandex/google"""
    robot = models.ForeignKey(Robots, on_delete=models.CASCADE,
        blank=True, null=True)
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Название профиля (папки)')
    user_agent = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Строка user_agent (браузер)')
    resolution = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Разрешение экрана')
    yandex_login = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    yandex_passwd = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)

    class Meta:
        verbose_name = 'Роботы - Профиль'
        verbose_name_plural = 'Роботы - Профили'


class Sites(Standard):
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Название сайта')
    url = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Ссылка на главную страницу сайта')

    class Meta:
        verbose_name = 'Роботы - Сайт'
        verbose_name_plural = 'Роботы - Сайты'

    def fix_url(self, link: str):
        """Обрабатываем ссылку до домена
           :param link: ссылка
        """
        if not link:
            return link
        schema, url = link.split('//')
        url = url.split('/')[0]
        return '%s//%s' % (schema, url)

    def save(self, *args, **kwargs):
        #self.url = self.fix_url(self.url)
        super(Sites, self).save(*args, **kwargs)


class SearchQueries(Standard):
    """Поисковые запросы для сайтов"""
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True,
        verbose_name='Поисковой запрос')
    site = models.ForeignKey(Sites, on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name='Сайт')

    class Meta:
        verbose_name = 'Роботы - Поисковой запрос'
        verbose_name_plural = 'Роботы - Поисковые запросы'


class TestScenarios(Standard):
    """Сценарии, состоящие из команд
       для выполнения роботами
       список возможных команд
    """
    robot = models.ForeignKey(Robots, on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name='Робот')
    site = models.ForeignKey(Sites, on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name='Сайт')
    name = models.CharField(max_length=255,
        blank=True, null=True, db_index=True)
    commands = models.TextField(blank=True, null=True,
        verbose_name='Команды в json')

    class Meta:
        verbose_name = 'Роботы - Сценарий'
        verbose_name_plural = 'Роботы - Сценарии'


# Команда, описание, параметры
TEST_COMMANDS = (
    ('goto', 'Перейти по ссылке', ['url']),
    ('refresh', 'Обновить страничку', None),
    ('window_handles', 'Список открытых вкладок', None),
    ('current_window_handle', 'Ид активной вкладки', None),
    ('close_current_window', 'Закрыть активную вкладку', None),
    ('switch_to_window', 'Переключает на окно/вкладку', None),
    ('close_other_tabs', 'Закрыть все вкладки, кроме активной', None),
    ('get_capabilities', 'Настройки браузера', None),
    ('maximize_window', 'Максимизировать размер окна', None),
    ('get_current_url', 'Получить текущий url браузера', ['unquote']),
    ('get_window_size', 'Получить размер окна', None),
    ('find_element_by_id', 'Поиск элемента по ид', ['id_selector']),
    ('find_element_by_name', 'Поиск элемента по имени', ['name']),
    ('find_element_by_xpath', 'Поиск элемента по xpath', ['xpath']),
    ('find_element_by_tag_name', 'Поиск элемента по тегу', ['tag']),
    ('find_element_by_css_selector', 'Поиск элемента по css селектору', ['selector']),
    ('find_element_by_link_text', 'Поиск элемента по тексту ссылки', ['link_text']),
    ('find_elements_by_name', 'Поиск элементов по имени', ['name']),
    ('find_elements_by_tag_name', 'Поиск элементов по тегу', ['tag']),
    ('find_elements_by_xpath', 'Поиск элементов по xpath', ['xpath']),
    ('find_elements_by_css_selector', 'Поиск элементов по css селектору', ['selector']),
    ('history_back', 'Возвращаемся на предыдущую страничку', None),
    ('screenshot2telegram', 'Отправить скриншот в телегу', ['msg']),
    # Сложные методы
    ('pretend_user', 'Притвориться пользователем', None),
)
