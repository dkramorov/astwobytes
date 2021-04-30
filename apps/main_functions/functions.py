# -*- coding:utf-8 -*-
import datetime
import json

from django.http import HttpResponse
from django.db.models import Max, Count, fields

def get_total_pages(query, by):
    """Рассчитать общее кол-во страничек
       для выполнения большого запроса"""
    result = None
    total_records = query.aggregate(Count('id'))['id__count']
    (total_pages, remain) = divmod(total_records, by)
    if remain:
        total_pages += 1
    return {
               'total_records': total_records,
               'total_pages': total_pages,
           }

def json_error(msg=None):
    """Ошибка json HttpResponse"""
    result = {'error': 1}
    if msg:
        result['msg'] = msg
    result = json.dumps(result)
    response = HttpResponse(result, mimetype='application/json')
    response['status_code'] = 'HTTP/1.0 200 OK';
    return response

def object_foreign_keys(row):
    """ForeignKey's в row"""
    result = {}
    for field in row.__class__._meta.fields:
        if isinstance(field, (fields.related.ForeignKey, )):
            #result[field.name] = field.rel.to
            result[field.name] = field.related_model
    return result

def fetched_foreign_key(row, relation_name):
    """Проверяем, вытащено ли поле из базы по Foreign key"""
    return row._state.fields_cache.get(relation_name)

def object_default_values(model):
    """Значения в моделе для БД по умолчанию"""
    result = {}
    for field in model._meta.fields:
        result[field.name] = field.get_default()
    return result

def object_auto_now_fields(model):
    """Поля с автоматическим обновлением даты"""
    result = []
    for field in model._meta.fields:
        if hasattr(field, "auto_now_add"):
            if field.auto_now_add:
                result.append(field.name)
                continue
        if hasattr(field, "auto_now"):
            if field.auto_now:
                result.append(field.name)
                continue
    return result

def object_fields_types(row):
    """Все типы полей в объекте
       :param row: экземпляр модели
    """
    result = {}
    types = {
        #'one_to_one': (fields.related.OneToOneRel, ), # row.__class__._meta.get_fields()
        'primary_key': (fields.AutoField, ),
        'str': (fields.CharField, fields.TextField, fields.EmailField),
        'int': (fields.IntegerField, fields.BigIntegerField),
        'boolean': (fields.BooleanField, ),
        'float': (fields.DecimalField, ),
        'datetime': (fields.DateTimeField, ),
        'date': (fields.DateField, ),
        'foreign_key': (fields.related.ForeignKey, fields.related.OneToOneField),
    }
    for field in row.__class__._meta.fields:
        ###print(field.get_internal_type(), field)
        found = False
        for key, ftypes in types.items():
            if found:
                break
            for ftype in ftypes:
                #if ftype == type(field):
                # Если date будет выше datetime,
                # то будет беда
                if isinstance(field, ftype):
                    result[field.name] = key
                    found = True
                    break
    # OneToOneRel отношения заносим
    #if related_fields:
    #    for item in row.__class__._meta.related_objects:
    #        if isinstance(item, fields.related.OneToOneRel):
    #            result[item.name] = 'foreign_key'
    return result

def object_fields_names(row):
    """Достаем названия полей +
       db_column названия полей => [('id', 'id'), ...]
       :param row: экземпляр модели
    """
    return [field.get_attname_column() for field in row.__class__._meta.fields]

def object_fields(row,
                  pass_fields: tuple = (),
                  only_fields: tuple = (),
                  fk_only_keys: dict = None,
                  related_fields: list = (), ):
    """Все параметры объекта (id, state, created...)
       :param pass_fields: ('пропускаем', 'эти', 'поля')
       :param only_fields: ('достаем', 'только', 'эти', 'поля')
       :param fk_only_fields: {'fk_field': ('достаем', 'только', 'эти', 'поля'), ...}
       :param related_fields: поля ссылающиеся на этот объект (OneToOneRel)
       Можно сделать row.full_clean(), что приведет
       все данные к нужному типу/виду"""
    result = {}
    if not fk_only_keys:
        fk_only_keys = {}
    #row.full_clean()
    default_values = object_default_values(row)
    ftypes = object_fields_types(row)

    # -----------------------------
    # OneToOneRel отношения заносим
    # -----------------------------
    if related_fields:
        for item in row.__class__._meta.related_objects:
            if item.name in related_fields and isinstance(item, fields.related.OneToOneRel):
                # ---------------------------------------------
                # Если связанный объект вытащен - заполняем его
                # ---------------------------------------------
                fk = fetched_foreign_key(row, item.name)
                if fk:
                    value = object_fields(fk,
                        only_fields=fk_only_keys.get(item.name),
                        fk_only_keys=fk_only_keys,
                    )
                    result[item.name] = value

    for field in row.__class__._meta.fields:
        if pass_fields and field.name in pass_fields:
            continue
        elif field.name in fk_only_keys:
            pass # Не пропускаем поля, если они указаны явно как foreign_keys
        elif only_fields and not field.name in only_fields:
            continue

        if field.name in ftypes:
            if ftypes[field.name] == 'foreign_key':
                value = getattr(row, '%s_id' % field.name)
                # ---------------------------------------------
                # Если связанный объект вытащен - заполняем его
                # ---------------------------------------------
                fk = fetched_foreign_key(row, field.name)
                if fk:
                    value = object_fields(fk,
                        only_fields=fk_only_keys.get(field.name),
                        fk_only_keys=fk_only_keys,
                    )
            else:
                value = getattr(row, field.name)

            if ftypes[field.name] == 'int':
                if value:
                    value = int(value)
                else:
                    value = None
            elif ftypes[field.name] == 'date':
                if value:
                    value = value.strftime('%d-%m-%Y')
            elif ftypes[field.name] == 'datetime':
                if value:
                    value = value.strftime('%d-%m-%Y %H:%M:%S')
            elif ftypes[field.name] == 'float':
                if value:
                    value = str(value)
            elif ftypes[field.name] == 'boolean':
                if value:
                    value = True
                else:
                    value = False
            elif not value and field.name in default_values:
                value = default_values[field.name]
        else:
            value = getattr(row, field.name)
            # -----------------------------------------
            # Тут нужно проверить - возможно поле json?
            # -----------------------------------------
            if value:
                if type(value) == str:
                  if ('{' in value and '}' in value) or ('[' in value and ']' in value):
                      try:
                          value = json.loads(value)
                      except:
                          pass
        result[field.name] = value
    return result

def recursive_fill(queryset,
                   result: list,
                   parents: str = ''):
    """Рекурсивное заполнение списка,
       элементы списка обычно queryset, но могут быть и dict
       работаем со списоком, queryset может что-то кэшить
       :param qyeryset: изначально результат запроса (например, model.filter)
       :param result: аккумулируемый результат в процессе обратки
       :param parents: какую вложенность сейчас обходим _x_y
    """
    if not isinstance(queryset, list):
        queryset = list(queryset)

    if not queryset:
        return
    is_dict = isinstance(queryset[0], dict)

    for item in queryset:
        item_parents = item['parents'] if is_dict else item.parents
        if not item_parents:
            item_parents = ''
        if parents == item_parents:
            item_id = item['id'] if is_dict else item.id
            if is_dict:
                item['sub'] = []
            else:
                item.sub = []
            result.append(item)
            item_id = item['id'] if is_dict else item.id
            next_parents = '%s_%s' % (item_parents, item_id)
            result_sub = item['sub'] if is_dict else item.sub
            recursive_fill(queryset, result_sub, next_parents)

def sort_voca(queryset, reverse: bool = False):
    """Сортировка списка после рекурсивного заполнения по position
       работаем как с экземплярами модели, так и со словарями
       sort in place ut.sort(key=lambda x: x.count, reverse=True)
       sort in new list newlist = sorted(ut, key=lambda x: x.count, reverse=True)
       {0: 17, 1: 12, 2: 47, 3: 32, 4: 74} =>
       sorted(d.items(), key=lambda (k, v): v, reverse=True)
       [(4, 74), (2, 47), (3, 32), (0, 17), (1, 12)] =>
       sorted(numbers, key=numbers.__getitem__)"""
    if not queryset:
        return queryset
    is_dict = isinstance(queryset[0], dict)
    if is_dict:
        for item in queryset:
            if 'sub' in item:
                item['sub'] = sort_voca(item['sub'], reverse=reverse)
        result = sorted(queryset, key=lambda x:x['position'], reverse=reverse)
        return result

    for item in queryset:
        if item.sub:
            item.sub = sort_voca(item.sub, reverse=reverse)
    result = sorted(queryset, key=lambda x:x.position, reverse=reverse)
    return result

def fill_parents(obj_array, model):
    """Принимаем список объектов, которые содержат
       parents like _1_2_3, затем достаем всех
       родителей и записываем в каждый объект
       иерархию родителей, причем делаем это в
       один запрос в базу"""
    ids_parents = {}
    # ------------------------------------
    # Сначала заполняем список айдишников,
    # которые надо достать скопом
    # ------------------------------------
    for obj in obj_array:
        if hasattr(obj, 'parents'):
            if obj.parents:
                if '_' in obj.parents:
                    obj.ids_parents = []
                    parents_array = obj.parents.split('_')
                    for parent in parents_array:
                        try:
                          p = int(parent)
                        except ValueError:
                          p = None
                        if p:
                          if not p in ids_parents:
                            ids_parents[p] = None
                          # --------------------------------------------
                          # Чтобы второй раз не приводить к нужному виду
                          # запоминанем иерархию айдишников
                          # --------------------------------------------
                          obj.ids_parents.append(p)
    # --------------------------------
    # Теперь нужно достать все объекты
    # и составить список по которому
    # будем заполнять иерархию parents
    # --------------------------------
    if ids_parents:
        model_objects = model.objects.filter(pk__in=ids_parents.keys())
        for item in model_objects:
            ids_parents[item.id] = item
    # ----------------------------------
    # Теперь все готово - нужно в каждый
    # объект насувать нужные parents
    # ----------------------------------
    for obj in obj_array:
        if hasattr(obj, 'ids_parents'):
            obj.parents_array = []
            for parent in obj.ids_parents:
                if parent in ids_parents:
                    obj.parents_array.append(ids_parents[parent])

