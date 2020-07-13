#-*- coding:utf-8 -*-
import json
import logging
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.flatcontent.models import Blocks, Containers
from apps.products.models import (Products,
                                  CostsTypes,
                                  Costs,
                                  ProductsPhotos,
                                  ProductsCats,
                                  Property,
                                  PropertiesValues,
                                  ProductsProperties, )

logger = logging.getLogger(__name__)

def prepare_value(value):
    """Подготавливаем данные,
       чтобы не было всякой говнины в них
       :param value: подготавливаемое значение
    """
    if not value:
        return None
    try:
        float_value = float(value)
        int_value = int(float_value)
        if float_value - int_value > 0:
            return float_value
        return int_value
    except ValueError:
        float_value = None
    value = '%s' % value
    value = value.replace('\r', '')
    value = value.replace('\n', '')
    value = value.strip()
    return value

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--start',
            action = 'store',
            dest = 'start',
            type = str,
            default = False,
            help = 'Set start date')
        parser.add_argument('--pass_img',
            action = 'store_true',
            dest = 'pass_img',
            default = False,
            help = 'Do not load images')

    def handle(self, *args, **options):
        """Импорт со старой админки
        """
        pass_img = options.get('pass_img')

        host = 'http://pizzahot.me'
        endpoint = '/media/unloading.json'
        r = requests.get('%s%s' % (host, endpoint))
        content = json.loads(r.text)

        costs_types = content.get('costs_types', {})
        for pk, cost_type in costs_types.items():
            analog = CostsTypes.objects.filter(pk=pk).first()
            if not analog:
                analog = CostsTypes(pk=pk)
            for field in ('name', 'tag', 'currency'):
                setattr(analog, field, prepare_value(cost_type[field]))
            analog.save()
            costs_types[pk]['analog'] = analog

        products = content.get('products')
        for pk, product in products.items():
            analog = Products.objects.filter(pk=pk).first()
            if not analog:
                analog = Products(pk=pk)
            product['code'] = product['kod']
            for field in ('name', 'altname', 'manufacturer',
                          'measure', 'price', 'dj_info',
                          'mini_info', 'info', 'code',
                          'count', 'position'):
                setattr(analog, field, prepare_value(product[field]))
            analog.save()
            if product['img'] and not pass_img:
                analog.upload_img('%s%s' % (host, product['img']))
            products[pk]['analog'] = analog

        costs = content.get('costs')
        for pk, cost in costs.items():
            analog = Costs.objects.filter(pk=pk).first()
            if not analog:
                analog = Costs(pk=pk)
            for field in ('measure', 'cost'):
                setattr(analog, field, prepare_value(cost[field]))
            analog.product = products[str(cost['product'])]['analog']
            analog.cost_type = costs_types[str(cost['cost_type'])]['analog']
            analog.save()
            costs[pk]['analog'] = analog

        photos = content.get('photos')
        for pk, photo in photos.items():
            analog = ProductsPhotos.objects.filter(pk=pk).first()
            if not analog:
                analog = ProductsPhotos(pk=pk)
            photo['name'] = photo['description']
            for field in ('name', ):
                setattr(analog, field, prepare_value(photo[field]))
            analog.product = products[str(photo['product'])]['analog']
            analog.save()
            if photo['img'] and not pass_img:
                analog.upload_img('%s%s' % (host, photo['img']))
            photos[pk]['analog'] = analog

        rubrics = content.get('rubrics')
        catalogue = Containers.objects.filter(tag='catalogue').first()
        for pk, rubric in rubrics.items():

            if not rubric['parents']:
                continue

            analog = Blocks.objects.filter(container=catalogue, tag='cat_%s' % pk).first()
            if not analog:
               analog = Blocks(container=catalogue, state=4, tag='cat_%s' % pk)
            rubric['title'] = rubric['altname']
            for field in ('name', 'title', 'keywords', 'position'):
                setattr(analog, field, prepare_value(rubric[field]))

            analog.parents = None
            analog.container = catalogue
            analog.state = 4
            analog.link = None
            analog.save()
            if rubric['img'] and not pass_img:
                analog.upload_img('%s%s' % (host, rubric['img']))
            rubrics[pk]['analog'] = analog
            rubrics[pk]['tags_parents'] = ['cat_%s' % item for item in rubric['parents'].split('_') if item]
            print(rubrics[pk]['tags_parents'])
        # TODO: Пофиксить parents
        # Первый tags_parents надо пропустить,
        # т/к мы верхний уровень игнорим,
        # потому что в старой админке это была рубрика Каталог,
        # далее надо по каждому tags_parents достать рубрику
        # и обновить parents


        cats = content.get('cats')
        for pk, cat in cats.items():
            analog = ProductsCats.objects.filter(pk=pk).first()
            if not analog:
                analog = ProductsCats(pk=pk)
            analog.product = products[str(cat['product'])]['analog']
            analog.container = catalogue
            analog.cat = rubrics[str(cat['cat'])]['analog']
            analog.save()
            cats[pk]['analog'] = analog

        properties = content.get('properties')
        for pk, prop in properties.items():
            analog = Property.objects.filter(pk=pk).first()
            if not analog:
                analog = Property(pk=pk)
            prop['code'] = prop['tag']
            for field in ('name', 'code', 'ptype'):
                setattr(analog, field, prepare_value(prop[field]))
            analog.save()
            properties[pk]['analog'] = analog

        pvalues = content.get('pvalues')
        for pk, pvalue in pvalues.items():
            analog = PropertiesValues.objects.filter(pk=pk).first()
            if not analog:
                analog = PropertiesValues(pk=pk)
            pvalue['str_value'] = pvalue['t_value']
            pvalue['digit_value'] = pvalue['i_value']
            for field in ('str_value', 'digit_value'):
                setattr(analog, field, prepare_value(pvalue[field]))
            analog.prop = properties[str(pvalue['prop'])]['analog']
            analog.save()
            pvalues[pk]['analog'] = analog

        products_props = content.get('products_props')
        for pk, product_prop in products_props.items():
            analog = ProductsProperties.objects.filter(pk=pk).first()
            if not analog:
                analog = ProductsProperties(pk=pk)
            analog.product = products[str(product_prop['product'])]['analog']
            analog.prop = pvalues[str(product_prop['pvalue'])]['analog']
            analog.save()
            products_props[pk] = analog


