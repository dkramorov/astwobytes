# -*- coding:utf-8 -*-
from django.db.models import Count
from django.conf import settings
from django.urls import reverse

from .models import Containers, Blocks, get_ftype
from .views import CUR_APP, blocks_vars

is_products = False
if 'apps.products' in settings.INSTALLED_APPS:
    is_products = True
    from apps.products.models import Products, ProductsCats

def check_titles_and_metatags(additional_menus: list = None):
    """Проверка заголовок title и мета-теги ссылки сайта
       длина не более 70 и не менее 50 знаков с пробелами +-10
       для карточек товаров начинать со слов Купить, Продажа"
    """
    result = {'problems': [], 'success': 'Проблемы найдены'}
    if not additional_menus:
        additional_menus = []
    menus = ['mainmenu', 'bottommenu'] + additional_menus
    # 1) Проверка названия сайта
    main_type = get_ftype('flatmain')
    main_container = Containers.objects.filter(tag='main', state=main_type).first()
    if main_container:
        company_name = main_container.blocks_set.filter(tag='company_name').first()
    if not company_name:
        company_name = Blocks.objects.create(tag='company_name',
                                             state=1,
                                             name='Название компании',
                                             container=main_container, )
    if not company_name.title:
        result['problems'].append({
            'name': 'Не заполнено название компании (поле title)',
            'description': 'Название компании подставляется во всех title в конце, внесите в поле title название компании',
            'link': reverse('%s:%s' % (CUR_APP, blocks_vars['edit_urla']), kwargs={
                'ftype': 'flatmain',
                'container_id': main_container.id,
                'action': 'edit',
                'row_id': company_name.id,
            }),
        })
    if not result['problems']:
        result['success'] = 'Проблемы не найдены'
    return result





