# -*- coding:utf-8 -*-
from django.db import transaction
from django.db.models import Value
from django.db.models.functions import Replace

def atomic_update(model, update_tasks: dict):
    """Обновление в транзакции только нужных полей
       update_tasks = [{
           'id': 1,
           'position': 10,
       }, {
           'id': 10,
           'position': 1,
       }]"""
    with transaction.atomic():
        for update_task in update_tasks:
            pk = update_task['id']
            del update_task['id']
            model.objects.filter(pk=pk).update(**update_task)

def bulk_replace(queryset, field, old_value, new_value):
    """Массовое обновление записей методом замены"""
    queryset.update(**{field:Replace(field, Value(old_value), Value(new_value))})


