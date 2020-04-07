# -*- coding: utf-8 -*-
import datetime
import logging

from django.contrib.auth.models import Permission
from django.db.models import Count, Q, Min, Max
from django.urls import reverse, resolve

from apps.main_functions.functions import (object_foreign_keys,
                                           object_fields_types,
                                           object_default_values,
                                           object_auto_now_fields, )
from apps.main_functions.string_parser import q_string_fill
from apps.main_functions.paginator import myPaginator, navigator
from apps.main_functions.date_time import str_to_date

logger = logging.getLogger()

class ModelHelper:
    """Покрываем одним классом всю рутину
       model - основная модель, с которой работаем"""
    def __init__(self, model, request=None):
        self.model = model
        self.context = {} # контекст для view
        # Метка модели, например, 'price'
        self.app_label = self.model._meta.app_label
        self.model_name = self.model._meta.model_name
        self.request = request
        self.q_string = {}
        if self.request:
            q_string_fill(self.request, self.q_string)
            if not "q" in self.q_string:
                self.q_string['q'] = {}
        # -----------------------------
        # Если мы вызываем без request,
        # задаем значения по-умолчанию
        # -----------------------------
        else:
            self.q_string['q'] = {}
            self.q_string['page'] = 1
            self.q_string['by'] = 50
        self.paginator_template = "core/admin_paginator.html"
        # -----------------------
        # Переменные для простого
        # вывода и редактирования
        # -----------------------
        self.singular_obj = 'Объект'
        self.plural_obj = 'Объекты'
        self.rp_singular_obj = 'Объекта' # Родительный падеж
        self.rp_plural_obj = 'Объектов' # Родительный падеж
        self.template_prefix = 'objects_'
        self.action_create = 'Новый'
        self.action_edit = 'Редактировать'
        self.action_drop = 'Удалить'
        self.action = None
        self.url_create = None
        self.url_edit = None
        # ----------------------
        # Постраничная навигация
        # ----------------------
        self.raw_paginator = {}
        self.paginator = None
        self.breadcrumbs = []
        # ----------------------------------
        # Можно передать разрешения (права),
        # и проверять здесь основные права,
        # ----------------------------------
        self.permissions = {
            'create': False,
            'edit': False,
            'drop': False,
            'view': False,
        }
        # -----------------
        # Произошла ошибка?
        # -----------------
        self.error = None
        # -------------------------
        # Запись с которой работаем
        # -------------------------
        self.row = None
        # -------------------
        # Переменные из формы
        # -------------------
        self.row_vars = {}
        self.files = []
        # ---------------
        # Поля для поиска
        # ---------------
        self.q = None
        self.search_fields = []
        # -------------------
        # Фильтры для выборки
        # -------------------
        self.filters = []
        self.excludes = []
        # ------------------------
        # Нестандартная сортировка
        # ------------------------
        self.custom_order = None
        # ----------------------------------
        # Фильтр неподдающийся логике модели
        # ----------------------------------
        self.custom_filter = None
        # -------------------------
        # select_related в запросах
        # -------------------------
        self.select_related = []
        # ----------
        # Сортировки
        # ----------
        self.order_by = []
        # -------------------
        # Слова для подсветки
        # -------------------
        self.words = []
        # ----------------------------------------
        # Ограничение, например, для ajax_search()
        # чтобы не выдирать все записи разом
        # ----------------------------------------
        self.limit = None
        # -------------------------
        # Заполняем права на модель
        # -------------------------
        self.get_permissions()

    def breadcrumbs_add(self, crumb:dict):
        """Добавление хлебных крошек"""
        self.breadcrumbs.append(crumb)

    def filter_add(self, cond):
        """Добавление .filter()"""
        self.filters.append(cond)

    def exclude_add(self, cond):
        """Добавление .exclude()"""
        self.excludes.append(cond)

    def select_related_add(self, field):
        """Добавление .select_related()"""
        self.select_related.append(field)

    def order_by_add(self, field):
        """Добавление .order_by()"""
        self.order_by.append(field)

    def files_add(self, fname):
        """Список файлов модели"""
        self.files.append(fname)

    def get_permissions(self, model=None):
        """Запрашиваем все права и запоминаем их
           :param model: Если надо запросить права от другой модели,
           которая определяет права для текущей модели
        """
        if self.request:
            user = self.request.user

            self.permissions = {
                # add_ instead create_
                'create': user.has_perm('%s.add_%s' % (self.app_label, self.model_name)),
                'edit': user.has_perm('%s.change_%s' % (self.app_label, self.model_name)),
                'drop': user.has_perm('%s.delete_%s' % (self.app_label, self.model_name)),
                'view': user.has_perm('%s.view_%s' % (self.app_label, self.model_name)),
            }

    def get_row(self, row_id):
        """Получаем запись по айдишнику"""
        if row_id:
            try:
                row = self.model.objects
                if self.select_related:
                    row = row.select_related(*self.select_related)
                self.row = row.get(pk=row_id)
            except self.model.DoesNotExist:
                self.error = 1
        return self.row

    def get_all_related_objects(self, pass_related:tuple = ('somemodel_set', )):
        """Получаем все связанные модели
           Например, чтобы не удалять их"""
        related_queries = []
        if self.row:
            # ------------------------------------------------
            # Смотрим все objects_set модели, ссылающиеся сюда
            # ------------------------------------------------
            related_models = self.row._meta.get_all_related_objects()
            for item in related_models:
                accessor_name = item.get_accessor_name() # somemodel_set
                if accessor_name in pass_related:
                    continue
                else:
                    # ---------------------------------------
                    # Тут лупится по базе по всем объектам???
                    # objects - все объекты из ForeignKey
                    # field - название поля ForeignKey
                    # ---------------------------------------
                    related_queries.append({
                        'objects': getattr(self.row, accessor_name).all(),
                        'field': item.field.name,
                        'accessor_name':accessor_name
                    })
                   # -------------------------------------
                    # Просто заполняем accessor_name: count
                    # - затем, сможем уже во view сделать
                    # getattr(l.row, accessor_name).all())
                    # -------------------------------------
                    #related_queries[accessor_name] = getattr(self.row, accessor_name).all().aggregate(Count("id"))['id__count']
        return related_queries

    def max_position(self, field:str = "parents", value:str = ""):
        """Максимальная позиция в базе"""
        obj = self.objects.all()
        if field:
            obj = self.objects.filter( **{ field:value } )
        obj = obj.aggregate(Max('position'))
        pos = obj['position__max']
        return pos or 1

    def post_vars(self, pass_fields: list = None):
        """Получаем переменные из формы
           pass_fields - пропускаем поля"""
        if not self.request:
            self.error = 1
            return None

        if not pass_fields:
            pass_fields = []

        types = object_fields_types(self.model())
        auto_now_fields = object_auto_now_fields(self.model)
        pass_fields += ("id", "created", "updated", "img")
        row_vars = {}

        form_fields = [field.name for field in self.model().__class__._meta.fields
                       if not field.name in pass_fields]
        for key in form_fields:
            value = self.request.POST.get(key, '')
            # ---------------------------------------------------
            # Обработка данных в соответствии с типом поля модели
            # данные из POST, там None НЕТУ
            # ---------------------------------------------------
            if key in types:
                if types[key] in ('int', 'foreign_key'):
                    try:
                        value = int(value)
                    except ValueError:
                        value = None
                elif types[key] == 'boolean':
                    try:
                        value = int(value)
                    except ValueError:
                        value = False
                    if value:
                        value = True
                elif types[key] == 'float':
                    try:
                        value = float(value)
                    except ValueError:
                        value = None
                elif types[key] in ('date', 'datetime'):
                    if key in auto_now_fields:
                        continue
                    value = str_to_date(value)
            else:
                logger.warning('there is no field %s in %s model types' % (key, self.model))
            row_vars[key] = value
        if self.request.FILES:
            if self.request.FILES.get('img'):
                row_vars['img'] = self.request.FILES['img']

        # Если мы хотим загрузить изображение не в текущую модель,
        # а, например, в галерею текущей модели (другая модель),
        # тогда просто pass_fields = ('grab_img_by_url', ),
        # и обрабатываем отдельно, например, так
        # new_photo = Photos()
        # new_photo.upload_img(request.POST.get('grab_img_by_url'))
        gibu = 'grab_img_by_url' in pass_fields
        if self.request.POST.get('grab_img_by_url') and not gibu:
            row_vars['img'] = self.request.POST['grab_img_by_url']
        self.row_vars = row_vars

    def save_row(self, pass_fields:tuple = ()):
        """Сохранение записи - запись значений row_vars"""
        if not self.row or not self.row_vars:
            return None
        # --------------------
        # Находим ForeignKey's
        # --------------------
        foreign_keys = object_foreign_keys(self.row)
        types = object_fields_types(self.row)
        # --------------------------------------
        # Значения полей, указанные по умолчанию
        # --------------------------------------
        default_values = object_default_values(self.model)
        auto_now_fields = object_auto_now_fields(self.model)

        for key, value in self.row_vars.items():
            if key in pass_fields or key == 'img':
                continue

            if value is None:
                if key in types:
                    if types[key] in ('date', 'datetime'):
                        value = default_values.get(key)
            # ---------------------------------------------------
            # Обработка данных в соответствии с типом поля модели
            # ---------------------------------------------------
            elif key in types:
                if types[key] == 'int':
                    try:
                        value = int(value)
                    except ValueError:
                        value = None
                elif types[key] == 'boolean':
                    try:
                        value = int(value)
                    except ValueError:
                        value = False
                    if value:
                        value = True
                elif types[key] == 'float':
                    if value == "nan":
                        value = None
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            value = None
                elif types[key] in ('date', 'datetime'):
                    if not type(value) in (datetime.date, datetime.datetime):
                        value = str_to_date(value)
                    if not value and key in auto_now_fields:
                        value = default_values.get(key)
                elif types[key] == 'foreign_key' and value:
                    if not key in foreign_keys:
                        value = None
                    elif not type(value) == type(foreign_keys[key]):
                        # ------------------
                        # Находим ForeignKey
                        # ------------------
                        try:
                            value = foreign_keys[key].objects.get(pk=int(value))
                        except ValueError:
                            continue
                        except foreign_keys[key].DoesNotExist:
                            continue
            # --------------------------------------------
            # Временное решение, надо прогонять, конечно,
            # полностью через новый model_helper - TODO!!!
            # --------------------------------------------
            #if '__' in key:
            #    foreign_key, foreign_field = key.split('__')
            #    foreign_obj = getattr(self.row, foreign_key)
            #    setattr(foreign_obj, foreign_field, value)
            #    logger.warning('Update related %s {%s: %s}' % (foreign_obj, foreign_field, value))
            #    continue
            setattr(self.row, key, value)
        self.row.save()
        # ---------------
        # Загружаем файлы
        # ---------------
        self.uploads()
        return self.row

    def uploads(self, row = None):
        """Загружаем файлы/изображения
           row позволяет грузить
           в экземпляр другой модели"""
        dest = self.row
        if row:
            dest = row
        if self.request.FILES and dest:
            for key, value in self.request.FILES.items():
                if key in self.files:
                    if hasattr(dest, key) and hasattr(dest, 'upload_img'):
                        dest.upload_file(value, key)
        if "img" in self.row_vars:
            # -----------------------------
            # Может быть файлом или ссылкой
            # -----------------------------
            if hasattr(dest, 'upload_img'):
                dest.upload_img(self.row_vars['img'])

    def standard_show(self, only_query:bool = False):
        """Стандартный вывод данных по модели
           filters = Q(name__isnull=True)|Q(name="")
           only_query просто вернуть запрос с фильтрами"""
        result = []

        # --------------------------
        # Если прав нету на просмотр
        # - ну тогда "пасется" пусть
        # --------------------------
        if not self.permissions['view']:
            if only_query:
                return self.model.objects.none()
            paginator, records = myPaginator(0, self.q_string['page'], self.q_string['by'])
            self.raw_paginator = paginator
            self.context['raw_paginator'] = self.raw_paginator
            self.paginator = navigator(paginator, self.q_string, self.paginator_template)
            self.context['paginator'] = self.paginator
            self.context['rows'] = result
            return result

        types = object_fields_types(self.model())
        query = self.model.objects.all()

        if self.select_related:
            query = query.select_related(*self.select_related)

        q = None

        if self.request:
            # ----------
            # GET / POST
            # ----------
            for q_var in ("q", "data[q]"):
                if self.request.method == "GET":
                    if self.request.GET.get(q_var) and self.search_fields:
                        q = self.request.GET[q_var]
                if self.request.method == "POST":
                    if self.request.POST.get(q_var) and self.search_fields:
                        q = self.request.POST[q_var]
        # -------------------------------------------
        # Если вдруг поисковая фраза не в q-параметре
        # -------------------------------------------
        if self.q:
            q = self.q

        cond = Q()
        if q:
            if not self.q:
                # -----------------------------------------
                # Мы не хотим, чтобы q писалось в
                # постраничную пагинацию параметром,
                # поэтому вообще не вносим его в q_string
                # это можно сделать после l.standard_show()
                # во view (l.q_string['q']['q'] = q
                # -----------------------------------------
                self.q_string['q']['q'] = q

            # -----------------
            # RAW / сырой поиск
            # -----------------
            raw_qqize = []
            q_array = q.split(" ")
            for item in q_array:
                tmp_cond = Q()
                for field in self.search_fields:
                    if field in types:
                        # ---------------------------
                        # По целому цислу, возможно,
                        # стоит сделать строгий поиск
                        # ("primary_key", "int")
                        # ---------------------------

                        # --------------------------------------
                        # По дате производим нестандартный поиск
                        # --------------------------------------
                        if types[field] in ("date", "datetime"):
                            d = str_to_date(q)
                            if d:
                                tmp_cond.add(Q(**{field:d}), Q.OR)
                            continue
                        else:
                            key = "%s__icontains" % field
                            tmp_cond.add(Q(**{key:item}), Q.OR)
                            raw_qqize.append(item)
                if tmp_cond:
                    cond.add(tmp_cond, Q.AND)

            # -----------------------------------------------------
            # Заполняем слова для подсветки (если они не заполнены,
            # что гарантировано, если мы не юзаем поиск по индексу)
            # -----------------------------------------------------
            if not self.words:
                self.words = raw_qqize

            # -------------------------------------------------------
            # Чтобы расширить поиск скажем своим списком айдишников,
            # нужно ввести это условие как Q.OR тогда сможем искать
            # стандартным поиском, однако добавлять свои результаты
            # скажем необходимо найти запись по переводу из Languages
            # -------------------------------------------------------
            if self.custom_filter:
                query = query.filter(Q(cond)|Q(self.custom_filter))
            else:
                query = query.filter(cond)

        if self.filters:
            for item in self.filters:
                # -----------------------------------
                # Принимаем в фильтры словарь или Q()
                # -----------------------------------
                if type(item) == dict:
                    key, value = item.popitem()
                    if key in types:
                        # ----------------------
                        # По числу строгий поиск
                        # ----------------------
                        if types[key] in ('int', 'float', 'primary_key', 'boolean'):
                            query = query.filter(**{key: value})
                        # --------------------------------------
                        # По дате производим нестандартный поиск
                        # --------------------------------------
                        elif types[key] in ('date', 'datetime'):
                            value = str_to_date(value)
                            if value:
                                if types[key] == 'datetime' and type(value) == datetime.date:
                                    start_date = datetime.datetime(value.year, value.month, value.day, 0, 0, 0)
                                    end_date = datetime.datetime(value.year, value.month, value.day, 23, 59, 59)
                                    query = query.filter(**{'%s__range' % (key, ): [start_date, end_date]})
                                else:
                                    query = query.filter(**{key: value})
                        else:
                            key = '%s__icontains' % key
                            query = query.filter(**{key: value})
                    elif '__' in key:
                        # ---------------------------
                        # Случай выбрки по ForeignKey
                        # ---------------------------
                        rel = key.split('__')[0]
                        if rel == 'pk':
                            rel = 'id'
                        query = query.filter(**{key: value})

                elif type(item) == type(Q()):
                    query = query.filter(item)

        if self.excludes:
            for item in self.excludes:
                query = query.exclude(item)
        # ----------------------------
        # Вернуть запрос для отдельных
        # предварительных манипуляций
        # ----------------------------
        if only_query:
            return query

        total_records = query.aggregate(Count("id"))['id__count']
        paginator, records = myPaginator(total_records, self.q_string['page'], self.q_string['by'])
        self.raw_paginator = paginator
        self.context['raw_paginator'] = self.raw_paginator
        self.paginator = navigator(paginator, self.q_string, self.paginator_template)
        self.context['paginator'] = self.paginator

        if not total_records:
            self.context['rows'] = []
            return []

        if self.custom_order:
            order_by = ["ordering", ]
            # ----------
            # Сортировки
            # ----------
            if self.order_by:
                for item in self.order_by:
                    order_by.append(item)
            query = query.extra(select={"ordering":self.custom_order}, order_by=order_by)
        # ----------
        # Сортировки
        # ----------
        if self.order_by and not self.custom_order:
            query = query.order_by(*self.order_by)

        result = query[records['start']:records['end']]
        self.context['rows'] = result
        return result

    def update_positions(self, custom_positions: list = None):
        """Изменение позиций моделей
           если нужно изменить позиции не из request,
           тогда передаем custom_positions id в нужном порядке"""
        result = {}
        if not self.request:
            return result

        positions = []
        if self.request.method == 'POST':
            positions = self.request.POST.getlist('positions[]')
        elif self.request.method == 'GET':
            positions = self.request.GET.getlist('positions[]')
        if custom_positions:
            positions = custom_positions

        self.filter_add({'pk__in': positions})
        query = self.standard_show(only_query=True)
        ids_items = {item.id: item for item in query.only('id', 'position')}

        bulk_update = []
        for i, item in enumerate(positions):
            pk = int(item)
            if not pk in ids_items:
                continue
            ids_items[pk].position = i + 1
            bulk_update.append(ids_items[pk])
        if bulk_update:
            self.model.objects.bulk_update(bulk_update, ['position'])
            result['success'] = 'Сортировка выполнена, обновите страничку'
        else:
            result['error'] = 'Ошибка при сортировке'
        return result

def create_model_helper(mh_vars, request, CUR_APP:str, action:str = None, reverse_params:dict = None):
    """Вспомогательная функция для создания ModelHelper"""
    model = mh_vars.pop('model')
    mh = ModelHelper(model, request)
    if not reverse_params:
        reverse_params = {}
    else:
        mh.context.update(reverse_params)

    mh_vars['root_url'] = reverse('%s:%s' % (CUR_APP, mh_vars['show_urla']), kwargs=reverse_params)
    # Опционально ссылка для создания объекта
    if 'create_urla' in mh_vars:
        reverse_params['action'] = 'create'
        mh_vars['url_create'] = reverse('%s:%s' % (CUR_APP, mh_vars['create_urla']), kwargs=reverse_params)

    mh_vars['action'] = action
    mh.context['permissions'] = mh.permissions
    for k, v in mh_vars.items():
        setattr(mh, k, v)
        mh.context[k] = v

    mh.breadcrumbs_add({
        'link': mh.root_url,
        'name': mh.plural_obj,
    })
    mh.context['breadcrumbs'] = mh.breadcrumbs
    return mh

