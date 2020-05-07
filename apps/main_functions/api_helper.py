# -*- coding:utf-8 -*-
from openpyxl import load_workbook
from io import BytesIO

from django.http import JsonResponse
from django.db.models import Q

from apps.main_functions.functions import object_fields
from apps.main_functions.model_helper import create_model_helper

def ApiHelper(request, model_vars: dict, CUR_APP: str):
    """Апи-метод для получения всех данных
       :param request: HttpRequest
       :param model_vars: по какой модели отдаем данные
       :param CUR_APP: текущее приложение
    """
    mh_vars = model_vars.copy()
    mh = create_model_helper(mh_vars, request, CUR_APP)
    # Принудительные права на просмотр
    mh.permissions['view'] = True

    # Независимо от метода
    params = request.GET if request.method == 'GET' else request.POST

    only_fields = []
    get_only_fields = params.get('only_fields')
    if get_only_fields:
        get_only_fields = get_only_fields.split(',')
        only_fields = [field.strip() for field in get_only_fields]
    # Параметры фильтрации через filter__field = ''
    # filter__ означает, что мы хотим отфильтровать по какому то полю,
    # например, ?filter__id=1&filter__is_active=1
    filters = {k.replace('filter__', ''): v for k, v in params.items() if 'filter__' in k}
    if filters:
        mh.filter_add(Q(**filters))

    context = mh.context
    rows = mh.standard_show(only_fields=only_fields)

    result = []
    for row in rows:
        item = object_fields(row, only_fields=only_fields)
        if not only_fields or 'folder' in only_fields:
            item['folder'] = row.get_folder()
        result.append(item)
    result = {'data': result,
              'last_page': mh.raw_paginator['total_pages'],
              'total_records': mh.raw_paginator['total_records'],
              'cur_page': mh.raw_paginator['cur_page'],
              'by': mh.raw_paginator['by'], }
    return JsonResponse(result, safe=False)

def XlsxHelper(request, model_vars: dict, CUR_APP: str,
               cond_fields: list = ['id']):
    """Апи-метод для сохранения данных из excel-файла
       :param request: HttpRequest
       :param model_vars: по какой модели отдаем данные
       :param CUR_APP: текущее приложение
       :param cond_fields: поля, по которым определяем аналог для обновления
    """
    result = {}
    mh_vars = model_vars.copy()

    mh = create_model_helper(mh_vars, request, CUR_APP)
    result['perms'] = mh.permissions

    action = request.POST.get('action')
    job = {'errors': ['Операция не поддерживается']}
    if action == 'import_xlsx':
        job = import_from_excel(mh.model, request.FILES.get('file'))
        if not job['errors']:
            result['success'] = 'Файл обработан, подтвердите загрузку'
    elif action == 'save':
        count = request.POST.get('count')
        data = request.POST.get('data')
        rows = []
        if count.isdigit():
            count = int(count)
            template = object_fields(mh.model(),
                                     pass_fields=('created', 'updated', 'img'))
            if count > 0:
                names = [k for k in template.keys() if request.POST.get('data[0][%s]' % k)]
                # по шаблону модели обходим количество отправленных объектов
                rows = [{k: request.POST.get('data[%s][%s]' % (i, k)) for k in names} for i in range(count)]
        job = save_from_excel(mh.model, rows, cond_fields)
        if not job['errors']:
            result['success'] = 'Добавлено %s, обновлено %s' % (job['created'], job['updated'])
    result['resp'] = job
    if job['errors']:
        result['error'] = '<br>'.join(job['errors'])
    return JsonResponse(result, safe=False)

def import_from_excel(model, excel_file, required_names: list = None):
    """Импорт данных из excel
       :param model: модель, в которую импортируем данные
       :param excel_file: экселька, например, request.FILES.get("excel_file")
       :param required_names: список обязательных полей в шапке
    """
    if not required_names:
        required_names = []
    result = {'errors': []}
    if not excel_file:
        result['errors'].append('Не передан файл')
        return result
    wb = load_workbook(BytesIO(excel_file.read()))
    sheet = wb.active

    rows = list(sheet.rows)
    if not len(rows) > 0:
        result['errors'].append('Файл пустой')
        return result

    # ----------------
    # Обработка ошибок
    # ----------------
    errors = []
    names = [cell.value for cell in rows[0]]
    for name in required_names:
        if not name in names:
            result['errors'].append('обязательное поле %s' % name)

    if result['errors']:
        return result

    template = object_fields(model(), only_fields=names)
    indexes = {name: names.index(name) for name in names if name in template}
    data = []

    for row in sheet.rows:
        item = {}
        # В первой записи будут названия полей
        for name, ind in indexes.items():
            item[name] = row[ind].value
        data.append(item)
    result['data'] = data[1:]
    return result

def save_from_excel(model, data, cond_fields: list = None):
    """Сохранение массива в базу
       :param model: модель, в которую импортируем данные
       :param data: массив с данными для импорта
       :param cond_fields: поля по которым ищем аналоги (обновляем)
    """
    result = {'errors': []}
    if not data:
        result['errors'].append('Не переданы данные для сохранения')
        return result
    if not cond_fields:
        result['errors'].append('Не переданы условия для обновления')
        return result
    created = 0
    updated = 0
    for item in data:
        cond = Q()
        # id обновлять - плохая затея
        if 'id' in item:
            del item['id']
        for k, v in item.items():
            if v:
                item[k] = v.strip()
        for cond_field in cond_fields:
            cond.add(Q(**{cond_field: item.get(cond_field)}), Q.AND)
        analog = model.objects.filter(cond).first()
        if analog:
            updated += 1
            model.objects.filter(pk=analog.id).update(**item)
        else:
            created += 1
            model.objects.create(**item)
    result['created'] = created
    result['updated'] = updated
    return result
