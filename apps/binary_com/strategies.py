#!/usr/bin/env python
# -*- coding: utf-8 -*-

def strategy_opposite_touches(ticks_data):
    """Касания линий Боллинджера
       Например,
       Должно быть касание - верх/центр/низ/центр/верх,
       либо наоборот ждем, - низ/центр/верх/центр/низ"""
    bmt = [] # bottom/middle/top
    tmb = [] # top/middle/bottom
    ticks_len = len(ticks_data) - 1

    # Касания выше/ниже линий боллинджера
    tick = ticks_data[-1]
    bb = tick[2]
    top = bb[0]
    bottom = bb[2]
    if tick[1] <= top: # тик выше чем верхняя линия Боллинджера
        bmt.append(ticks_len)
    elif tick[1] >= bottom: # тик ниже чем нижняя линия Боллинджера
        tmb.append(ticks_len)
    if not bmt and not tmb:
        return {'action': None, 'data': []}

    # По стратегии /верх/центр/низ/центр/верх
    if bmt:
        # Ищем касание ниже центра
        # Позиция: выше срендей линии Боллинджера
        # ждем пока упадем ниже средней линии Боллинджера
        for i in range(ticks_len, -1, -1):
            tick = ticks_data[i]
            bb = tick[2]
            middle = bb[1]
            if tick[1] >= middle: # тик ниже чем средняя линия Боллинджера
                bmt.append(i)
                break
        if len(bmt) > 1:
            # Ищем касание низа
            # Позиция: ниже средней линии Боллинджера
            # ждем пока упадем ниже нижней линии Боллинджера
            # мы не потерпим если окажемся выше верхней линии Боллинджера
            for i in range(ticks_len, -1, -1):
                if i > bmt[1]:
                    continue
                tick = ticks_data[i]
                bb = tick[2]
                top = bb[0]
                bottom = bb[2]
                if tick[1] >= bottom: # тик ниже чем нижняя линия Боллинджера
                    bmt.append(i)
                    break
                # Если происходит касание верха, тогда останавливаемся
                if tick[1] <= top: # тик выше чем верхняя линия Боллинджера
                    break
        if len(bmt) > 2:
            # Ищем касание выше центра
            # Позиция: ниже средней линии Боллинджера
            # ждем пока поднимемся выше срендей линии Боллинджера
            for i in range(ticks_len, -1, -1):
                if i > bmt[2]:
                    continue
                tick = ticks_data[i]
                bb = tick[2]
                middle = bb[1]
                bottom = bb[2]
                if tick[1] <= middle: # тик выше чем средняя линия Боллинджера
                    bmt.append(i)
                    break
        if len(bmt) > 3:
            # Ищем касание верха
            # Позиция: выше средней линии Боллинджера
            # ждем пока поднимемся выше верхней линии Боллинджера
            # мы не потерпим если окажемся ниже нижней линии Боллинджера
            for i in range(ticks_len, -1, -1):
                if i > bmt[3]:
                    continue
                tick = ticks_data[i]
                bb = tick[2]
                top = bb[0]
                bottom = bb[2]
                if tick[1] <= top: # тик выше чем верхняя линия Боллинджера
                    bmt.append(i)
                    break
                # Если происходит касание низа, тогда останавливаемся
                if tick[1] >= bottom: # тик ниже чем нижняя линия Боллинджера
                    break

    # По стратегии /низ/центр/верх/центр/низ
    if tmb:
        # Ищем касание выше центра
        # Позиция: ниже средней линии Боллинджера
        # ждем пока поднимеся выше средней линии Боллинджера
        for i in range(ticks_len, -1, -1):
            tick = ticks_data[i]
            bb = tick[2]
            middle = bb[1]
            if tick[1] <= middle: # тик выше чем средняя линия Боллинджера
                tmb.append(i)
                break
        if len(tmb) > 1:
            # Ищем касание верха
            # Позиция: выше средней линии Боллинджера
            # ждем пока поднимемся выше верхней линии Боллинджера
            # мы не потерпим если окажемся ниже нижней линии Боллинджера
            for i in range(ticks_len, -1, -1):
                if i > tmb[1]:
                    continue
                tick = ticks_data[i]
                bb = tick[2]
                top = bb[0]
                bottom = bb[2]
                if tick[1] <= top: # тик выше чем верхняя линия Боллинджера
                    tmb.append(i)
                    break
                # Если происходит касание низа, тогда останавливаемся
                if tick[1] >= bottom: # тик ниже чем нижняя линия Боллинджера
                    break
        if len(tmb) > 2:
            # Ищем касание ниже центра
            # Позиция: выше средней линии Боллинджера
            # ждем пока упадем ниже срендей линии Боллинджера
            for i in range(ticks_len, -1, -1):
                if i > tmb[2]:
                    continue
                tick = ticks_data[i]
                bb = tick[2]
                middle = bb[1]
                bottom = bb[2]
                if tick[1] >= middle: # тик ниже чем средняя линия Боллинджера
                    tmb.append(i)
                    break
        if len(tmb) > 3:
            # Ищем касание низа
            # Позиция: ниже средней линии Боллинджера
            # ждем пока упадем ниже нижней линии Боллинджера
            # мы не потерпим если окажемся выше верхней линии Боллинджера
            for i in range(ticks_len, -1, -1):
                if i > tmb[3]:
                    continue
                tick = ticks_data[i]
                bb = tick[2]
                top = bb[0]
                bottom = bb[2]
                if tick[1] >= bottom: # тик ниже чем нижняя линия Боллинджера
                    tmb.append(i)
                    break
                # Если происходит касание верха, тогда останавливаемся
                if tick[1] <= top: # тик выше чем верхняя линия Боллинджера
                    break

    if len(bmt) > 4:
        return {'action': 'PUT', 'data': bmt}
    if len(tmb) > 4:
        return {'action': 'CALL', 'data': tmb}
    return {'action': None, 'data': []}