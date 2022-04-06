import xapian

from django.conf import settings
from django.core.cache import cache
from django.db.models import Q

from apps.flatcontent.models import Blocks
from apps.products.models import (Products,
                                  ProductsCats,
                                  ProductsPhotos,
                                  Property,
                                  PropertiesValues,
                                  ProductsProperties,
                                  CostsTypes,
                                  Costs, )

"""
Выбор стратегии поиска: индексный или по базе
"""

class SearchStrategy:
    def check_cache(self, cache_var: str, force_new: bool = False):
        """Вытаскиваем значение по ключу кэша
           :param cache_var: ключ кэша
           :param force_new: не использовать кэш, если True
        """
        inCache = cache.get(cache_var)
        if inCache and not force_new:
            inCache['from_cache'] = True
            return inCache

    def get_block(self, block_id: int):
        """Находим блок - Blocks
           например, нужно найти рубрику
           :param block_id: ид блока
        """
        return Blocks.objects.filter(pk=block_id).only('id', 'parents').first()

    def get_parents(self, block: Blocks):
        """Получить parents для блока
           например, нужно найти parents рубрики
           :param block: экземпляр блока (Blocks)
        """
        parents = '_%s' % block.id
        if block.parents:
            parents ='%s_%s' % (block.parents, block.id)
        return parents

    def get_subblocks(self, block: Blocks):
        """Найти подблоки блока
           :param block: блок подблоки которого будем искать
        """
        parents = self.get_parents(block)
        return Blocks.objects.filter(is_active=True).filter(Q(parents=parents)|Q(parents__startswith='%s_' % parents)).values_list('id', flat=True)

    def get_facet_filters_from_request(self, request):
        """Получаем фасетные фильтры из запроса
           :param request: HttpRequest
        """
        facet_filters = {}
        method = request.GET if request.method == 'GET' else request.POST
        for k in method.keys():
            if not k.startswith('prop_'):
                continue
            try:
                key = int(k.replace('prop_', ''))
            except ValueError:
                continue
            values = request.GET.getlist(k)

            # Если значение пустое, то лучше пропустить
            if not values or (len(values) == 1 and not values[0]):
                continue

            if not key in facet_filters:
                facet_filters[key] = []

            for value in values:
                try:
                    value = int(value)
                except ValueError:
                    continue
                facet_filters[key].append(value)
        return facet_filters


class DBSearchStrategy(SearchStrategy):
    """Класс для поиска по базе данных"""

    def get_filters_for_cat(self,
                            cat_id: int,
                            search_facet: bool = True,
                            cache_time: int = 300,
                            force_new: bool = False):
        """Получение фильтров по рубрике
           :param cat_id: ид выбранной категории
           :param search_facet: только фасеты для поиска (search_facet)
           :param cache_time: время кэширования
           :param force_new: игнорить кэш
           :return result: словарь фильтров
        """
        result = {}
        # 0) Проверяем в кэше
        cache_var = 'get_filters_for_cat_%s_%s_%s' % (
            settings.PROJECT_NAME,
            cat_id,
            1 if search_facet else 0,
        )
        inCache = self.check_cache(cache_var=cache_var, force_new=force_new)
        if inCache:
            return inCache

        # 1) Находим рубрику
        cat = self.get_block(block_id=cat_id)
        if not cat:
            return
        # 2) Находим вложенные рубрики
        subcats = self.get_subblocks(block=cat)
        cats = list(subcats)
        cats.append(cat.id)
        # 3) Находим товары привязанные к рубрике и подрубрикам
        products = ProductsCats.objects.filter(cat__in=cats).values_list('product', flat=True)
        # 4) Находим привязанные значения свойств для товаров
        products = list(products)
        ids_values = ProductsProperties.objects.filter(product__in=products)
        # Только фасеты поиска
        if search_facet:
            ids_search_props = Property.objects.filter(search_facet=True, is_active=True).values_list('id', flat=True)
            ids_values = ids_values.filter(prop__prop__search_facet=True)

        ids_values = ids_values.values_list('prop', flat=True) # это PropertiesValues

        ids_values = set(ids_values)
        # 5) Находим значения свойств
        pvalues = PropertiesValues.objects.filter(pk__in=ids_values, is_active=True)
        # 6) Находим свойства по значениям
        ids_props = set([pvalue.prop_id for pvalue in pvalues])
        # TODO завести признак фасета для свойства (выводится в фильтрах)
        props = Property.objects.filter(pk__in=ids_props)
        for prop in props:
            result[prop.id] = {
                'id': prop.id,
                'name': prop.name,
                'code': prop.code,
                'ptype': prop.ptype,
                'measure': prop.measure,
                'values': [],
            }
        for pvalue in pvalues:
            if pvalue.prop_id in result:
                prop = result[pvalue.prop_id]
                prop['values'].append({
                    'id': pvalue.id,
                    'value': pvalue.str_value,
                })
        for key in result.keys():
            result[key]['values'].sort(key=lambda x: x['value'])
        cache.set(cache_var, result, cache_time)
        return result

    def get_filters_for_search(self, facet_filters: dict):
        """Получаем результат по фасетным фильтрам
           находим по ним товары
           :param facet_filters: словарь с фильтрами, которые выбраны,
                                 например, {2581: [147359, ...], ...}
                                 по принципу {property_id: [value_id, ]}
        """
        if not facet_filters:
            return {}
        # Тут не получится собрать AND/OR запросами,
        # т/к при выборке 2х значений, мы не сможем
        # выбрать запись, где оба значения удволетворены,
        # поэтому отфильтровываем по каждому
        facet_query = Q()
        ids_products = []
        first_filter = True
        for k, v in facet_filters.items():
            prop_query = Q()
            for item in v:
                prop_query.add(Q(prop__id=item), Q.OR)
            if first_filter:
                ids_products = ProductsProperties.objects.filter(prop_query).values_list('product', flat=True)
            else:
                # Уже первый фильтр нихера не вернул,
                # можно не продолжать
                if not ids_products:
                    return {
                        'ids_products': [],
                        'facet_filters': facet_filters,
                    }
                ids_products = ProductsProperties.objects.filter(prop_query).filter(product__in=ids_products).values_list('product', flat=True)
        return {
            'ids_products': list(ids_products),
            'facet_filters': facet_filters,
        }

class IndexSearchStrategy(SearchStrategy):
    """Класс для поиска по индексу
       list(Property.indexer.search(xapian.Query.MatchAll))[0].tags
       list(Property.indexer.search('id:2579 OR id:2679'))
    """
    def get_filters_for_cat(self,
                            cat_id: int,
                            search_facet: bool = True,
                            cache_time: int = 300,
                            force_new: bool = False):
        # TODO: is_active
        result = {}

        # 0) Проверяем в кэше
        cache_var = 'get_filters_for_cat_%s_%s_%s' % (
            settings.PROJECT_NAME,
            cat_id,
            1 if search_facet else 0,
        )
        inCache = self.check_cache(cache_var=cache_var, force_new=force_new)
        if inCache:
            return inCache

        # 1) Находим рубрику
        cat = self.get_block(block_id=cat_id)
        if not cat:
            return
        # 3) Находим товары привязанные к рубрике и подрубрикам
        #search_products = Products.indexer.search('get_rubrics:%s' % cat_id)

        # 4) Находим привязанные значения свойств для товаров
        if search_facet:
            # Только фасеты поиска
            ids_pvalues = ProductsProperties.indexer.search('get_rubrics:%s AND get_prop_search_facet:%s' % (cat_id, True))
        else:
            ids_pvalues = ProductsProperties.indexer.search('get_rubrics:%s' % (cat_id, ))

        collapsed_pvalues = ids_pvalues.collapse_by('get_prop_id')
        ids_props = [pvalue.tags['get_prop_id'] for pvalue in collapsed_pvalues]
        # 6) Находим свойства по значениям
        query = ' OR '.join(['id:%s' % int(item) for item in ids_props])
        props = Property.indexer.search(query)
        # 5) Находим значения свойств
        query = ' OR '.join(['get_prop_id:%s' % int(item) for item in ids_props])
        pvalues = PropertiesValues.indexer.search(query)

        for hit in props:
            prop = hit.tags
            prop_id = int(prop['id'])
            result[prop_id] = {
                'id': prop_id,
                'name': prop['name'].decode('utf-8'),
                'code': prop['code'].decode('utf-8'),
                'ptype': int(prop['ptype']),
                'measure': prop['measure'].decode('utf-8'),
                'values': [],
            }
        for hit in pvalues:
            pvalue = hit.tags
            prop_id = int(pvalue['get_prop_id'])
            if prop_id in result:
                prop = result[prop_id]
                prop['values'].append({
                    'id': int(pvalue['id']),
                    'value': pvalue['str_value'].decode('utf-8'),
                })
        for key in result.keys():
            result[key]['values'].sort(key=lambda x: x['value'])
        cache.set(cache_var, result, cache_time)
        return result

    def get_filters_for_search(self, facet_filters: dict):
        """Получаем результат по фасетным фильтрам
           находим по ним товары
           :param facet_filters: словарь с фильтрами, которые выбраны,
                                 например, {2581: [147359, ...], ...}
                                 по принципу {property_id: [value_id, ]}
        """
        if not facet_filters:
            return {}
        ids_products = []
        # По одному фильтру при нескольких значениях делаем OR
        # По разным филтрам делаем AND
        query = ''
        for key, value in facet_filters.items():
            subquery = ' OR '.join(['get_values:%s' % int(item) for item in value])
            query += '(%s)' % subquery
        search_result = Products.indexer.search(query)
        for item in search_result:
            # Нужно записать какие фасеты с результатами
            # TODO: enquire.add_matchspy(xapian.ValueCountMatchSpy(index))

            ids_products.append(item.pk)

        return {
            'ids_products': ids_products,
            'facet_filters': facet_filters,
        }

def get_search_strategy():
    """Возвращает класс для поиска по товарам"""
    if 'djapian' in settings.INSTALLED_APPS:
        return IndexSearchStrategy()
    return DBSearchStrategy()
