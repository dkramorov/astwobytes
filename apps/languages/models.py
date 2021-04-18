# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from apps.main_functions.models import Standard

class UITranslate(Standard):
    """Переводы для текста в интерфейсе админки
    """
    class_name = models.CharField(max_length = 255,
        blank = True, null = True, db_index = True,
        verbose_name = 'css класс элемента')
    domain_pk = models.IntegerField(blank = True, null = True, db_index = True,
        verbose_name = 'Домен на каждый сайт из settings.py')
    value = models.CharField(max_length = 255,
        blank = True, null = True,
        verbose_name = 'Перевод')

    class Meta:
        verbose_name = 'Перевод UI'
        verbose_name_plural = 'Переводы UI'

class Translate(Standard):
    """Переводы для моделей по полям
    """
    domain_pk = models.IntegerField(blank = True, null = True, db_index = True,
        verbose_name = 'Домен на каждый сайт из settings.py')
    content_type = models.CharField(max_length = 255,
        blank = True, null = True, db_index = True,
        verbose_name = 'Привязка к типу модели')
    model_pk = models.IntegerField(blank = True, null = True, db_index = True,
        verbose_name = 'ID экземпляра модели')
    field = models.CharField(max_length = 255,
        blank = True, null = True, db_index = True,
        verbose_name = 'Поле, которое переводим')
    value = models.CharField(max_length = 255,
        blank = True, null = True, db_index = True,
        verbose_name = 'Значение поля (перевод)')
    text = models.TextField(blank=True, null = True,
        verbose_name = 'Если поле большое, то это перевод без индекса')

    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'

def get_domains():
    """Получить список доменов"""
    return [{
        'pk': domain['pk'],
        'domain': domain['domain'],
        'lang': domain['domain'].split('.')[0],
        'name': domain['name'],
        'translations': {},
    } for domain in settings.DOMAINS if domain['pk']]

def get_content_type(row):
    """Выясняем content_type для экземпляра модели
       :param row: экземпляр модели
    """
    app_label = row._meta.app_label
    model_name = row._meta.model_name
    return '%s.%s' % (app_label, model_name)

def save_translate(row, row_vars: list, request_post: dict):
    """Сохранение перевода
       :param row: экземпляр модели, с которой работаем
       :param row_vars: список полей модели
       :param request_post: HttpRequest POST (request.POST)
       :return domains: домены с переводами полей
    """
    if not row.id:
        assert False
    content_type = get_content_type(row)
    domains = get_domains()
    for key, value in row_vars.items():
        for domain in domains:
            field_name = 'translate_%s_%s' % (key, domain['pk'])
            if not request_post.get(field_name):
                continue
            field_value = request_post[field_name]
            domain['translations'][key] = field_value
            kwargs = {
                'content_type': content_type,
                'model_pk': row.id,
                'domain_pk': domain['pk'],
                'field': key,
            }
            analog = Translate.objects.filter(**kwargs).first()
            new_values = {}
            if len(field_value) > 254:
                new_values['value'] = ''
                new_values['text'] = field_value
            else:
                new_values['value'] = field_value
                new_values['text'] = ''
            if not analog:
                kwargs.update(new_values)
                analog = Translate.objects.create(**kwargs)
            else:
                Translate.objects.filter(pk=analog.id).update(**new_values)
    return domains

def get_domain(request, domains: list = None):
    """Получить текущий язык/домен
       ---------------------------
       При переключении языка между доменами
       надо быть внимательным к сессии,
       eсли мы берем язык из сессии,
       то мы его берем на том домене, где мы находимся,
       однако, если мы находимся на китайской версии и переключаемся,
       то мы окажемся на новом домене, где сессия другая

       В сессию язык надо писать, чтобы в шаблонах логику не повторять
       ---------------------------
       :param request: HttpRequest
    """
    domain = None
    if not hasattr(request, 'META') or not 'HTTP_HOST' in request.META:
        return
    # -------------------
    # Домен/язык по хосту
    # -------------------
    if not domains:
        domains = get_domains()

    lang = request.META['HTTP_HOST'].split('.')[0]
    # ---------
    # По домену
    # ---------
    for item in domains:
        if item['domain'] == '%s.%s' % (lang, settings.MAIN_DOMAIN):
            request.session['lang'] = lang
            return item
        elif settings.DEFAULT_DOMAIN:
            if request.META['HTTP_HOST'] == settings.MAIN_DOMAIN:
                request.session['lang'] = settings.DEFAULT_DOMAIN
                return item
    # --------------
    # Либо по сессии
    # --------------
    if hasattr(request, 'session') and request.session.get('lang'):
        lang = request.session['lang']
        for item in domains:
            if item['lang'] == lang:
                return item
    # -------------
    # Либо основной
    # -------------
    if settings.DEFAULT_DOMAIN:
        for item in domains:
            if item['lang'] == settings.DEFAULT_DOMAIN:
                request.session['lang'] = lang
                return item
    return None

def get_translate(rows, domains: list, only_fields: list = None):
    """Заполняем переводы для queryset rows
       :param rows: объекты, которым надо достать перевод
       :param domains: результирующий объект, куда пишем переводы
       :param only_fields: только нужные поля
       :return domains: домены с переводами полей
    """
    if not rows:
        return
    content_type = get_content_type(rows[0])
    ids = {}
    for row in rows:
        row.translations = {}
        for item in domains:
            row.translations[item['lang']] = {}
        ids[row.id] = row

    translations = Translate.objects.filter(content_type=content_type, model_pk__in=ids.keys())
    if only_fields:
        translations = translations.filter(field__in=only_fields)
    for translate in translations:
        for item in domains:
            if item['pk'] == translate.domain_pk:
                value = translate.value or translate.text
                ids[translate.model_pk].translations[item['lang']][translate.field] = value
                # Это для админки, работает на 1 объект,
                # если объектов много, то ищем в instance.translations
                item['translations'][translate.field] = value
    return domains

def translate_rows(rows: list, domain: dict):
    """Заполняем переводы для queryset rows,
       заменяем основные поля на переводы
       domains = settings.DOMAINS
       :param rows: массив объектов, в которых есть translations,
                    после get_translate(objects, domains)
       :param domain: домен, обычно в translations он один"""
    for row in rows:
        if not hasattr(row, 'translations'):
            continue
        lang = domain['lang']
        if not lang in row.translations:
            continue
        for key, value in row.translations[lang].items():
            setattr(row, key, value)
