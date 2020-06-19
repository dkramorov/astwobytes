from django.db import models

from apps.main_functions.models import Standard
from apps.demonology.models import Daemon

class Robots(Standard):
    name = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    daemon = models.OneToOneField(Daemon, blank=True, null=True, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    class Meta:
        verbose_name = 'Бинари - Робот'
        verbose_name_plural = 'Бинари - Роботы'

def build_symbols_dict(obj: dict):
    """Построить словарь контрактов
       :param obj: полученные контракты (get_active_symbols)
    """
    from apps.main_functions.catcher import json_pretty_print
    active_symbols = obj['active_symbols']
    markets = {}
    for item in active_symbols:
        market = markets.get(item['market'])
        if not market:
            market = {
                'market': item['market'],
                'name': item['market_display_name'],
                'submarkets': {},
            }
            markets[item['market']] = market
        submarket = market['submarkets'].get(item['submarket'])
        if not submarket:
            submarket = {
                'submarket': item['submarket'],
                'name': item['submarket_display_name'],
                'symbols': [],
            }
            market['submarkets'][item['submarket']] = submarket
        submarket['symbols'].append(item['symbol'])
    print(json_pretty_print(markets))
    return markets

class Schedule(Standard):
    """Расписание с использованием календаря"""
    event_choices = (
        (1, 'Стратегия Bollinger'),
        (2, 'Стратегия Random'),
    )
    event = models.IntegerField(choices=event_choices, blank=True, null=True, db_index=True)
    start = models.DateTimeField(blank=True, null=True, verbose_name='Начало события', db_index=True)
    end = models.DateTimeField(blank=True, null=True, verbose_name='Завершение события', db_index=True)
    robot = models.ForeignKey(Robots, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Робот')
    class Meta:
        verbose_name = 'Бинари - Расписание для робота'
        verbose_name_plural = 'Бинари - Расписания для робота'
