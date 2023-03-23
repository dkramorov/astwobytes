# -*- coding: utf-8 -*-
from django.db import models

from apps.main_functions.models import Standard

class IPRange(Standard):
    """Диапазоны IP адресов"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='Имя хоста')
    start_ip = models.CharField(max_length=64, blank=True, null=True, db_index=True,
        verbose_name='Начальный ip адрес')
    end_ip = models.CharField(max_length=64, blank=True, null=True, db_index=True,
        verbose_name='Конечный ip адрес')

    class Meta:
        verbose_name = 'NetTools - IPRange'
        verbose_name_plural = 'NetTools - IPRange'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(IPRange, self).save(*args, **kwargs)

    def __str__(self):
        return 'id=%s, name=%s, %s-%s' % (self.id, self.name, self.start_ip, self.end_ip)

class IPAddress(Standard):
    """IP адрес"""
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True,
        verbose_name='Имя хоста')
    ip = models.CharField(max_length=64, blank=True, null=True, db_index=True,
        verbose_name='IP адрес')
    mac = models.CharField(max_length=64, blank=True, null=True, db_index=True,
        verbose_name='MAC адрес')

    class Meta:
        verbose_name = 'NetTools - IPAddress'
        verbose_name_plural = 'NetTools - IPAddresses'
        #permissions = (
        #    ('view_obj', 'Просмотр объектов'),
        #    ('create_obj', 'Создание объектов'),
        #    ('edit_obj', 'Редактирование объектов'),
        #    ('drop_obj', 'Удаление объектов'),
        #)
        #default_permissions = []

    def save(self, *args, **kwargs):
        super(IPAddress, self).save(*args, **kwargs)

    def __str__(self):
        return 'id=%s ip=%s, mac=%s, name=%s' % (self.id, self.ip, self.mac, self.name)

def make_list_from_range(ip_range: str = '127.0.0.1-127.0.0.2'):
    """Создаем список ip-адресов из строки с диапазоном
       :param ip_range: диапазон строкой ip адресов
    """
    error = ''
    if not ip_range:
        return {
            'error': 'Диапазон не найден',
        }
    if not ip_range.count('-') == 1:
        return {
            'error': 'Неправильно указано тире в диапазоне',
        }
    start_ip, end_ip = ip_range.split('-')
    start_ip_parts = start_ip.split('.')
    end_ip_parts = end_ip.split('.')
    if not len(start_ip_parts) == 4 or not len(end_ip_parts) == 4:
        return {
            'error': 'Диапазоны не соответствуют нужной длине',
        }
    out_of_range = False
    for i in range(len(start_ip_parts)):
        start_ip_parts[i] = int(start_ip_parts[i])
        end_ip_parts[i] = int(end_ip_parts[i])
        if start_ip_parts[i] > 255 or start_ip_parts[i] < 0:
            out_of_range = True
        if end_ip_parts[i] > 255 or end_ip_parts[i] < 0:
            out_of_range = True
    if out_of_range:
        return {
            'error': 'Указаны ip адреса вне диапазона'
        }

    def check_ip_parts(i: int = 0):
        """Проверяем не больше ли начальный ip чем конечный]
           :param i: уровень на котором проверяем
        """
        if start_ip_parts[i] > end_ip_parts[i]:
            return True
        return False
    is_range_error = check_ip_parts(0)
    if start_ip_parts[0] == end_ip_parts[0] and not is_range_error:
        is_range_error = check_ip_parts(1)
        if start_ip_parts[1] == end_ip_parts[1] and not is_range_error:
            is_range_error = check_ip_parts(2)
            if start_ip_parts[2] == end_ip_parts[2] and not is_range_error:
                is_range_error = check_ip_parts(3)

    if is_range_error:
        return {
            'error': 'Начальный диапазон больше конечного',
        }
    result = []

    start = start_ip_parts
    end = end_ip_parts
    while True:
        print(start, end)
        if start == end:
            if end[3] != 0 and end[0] != 0:
                result.append('.'.join([str(item) for item in start]))
            break
        if end[3] != 0 and end[0] != 0:
            result.append('%s.%s.%s.%s' % (end[0], end[1], end[2], end[3]))
        end[3] = end[3] - 1
        if end[3] < 0:
            end[3] = 255
            end[2] = end[2] - 1
        if end[2] < 0:
            end[2] = 255
            end[1] = end[1] - 1
        if end[1] < 0:
            end[1] = 255
            end[0] = end[0] - 1
        if end[0] < 0:
            #print(result)
            assert False
    return result

