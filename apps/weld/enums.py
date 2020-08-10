# -*- coding: utf-8 -*-
import re
import logging

logger = logging.getLogger('main')

rega_rus2eng = re.compile('^[a-z0-9]+$', re.I+re.U+re.DOTALL)
rega_eng2rus = re.compile('^[а-я0-9]+$', re.I+re.U+re.DOTALL)

def replace_rus2eng(text):
    """Заменяем русские символы на английские,
       если остаются русские символы - выдаем ошибку
       :param text: текст, где производим замены
    """
    if not text:
        return
    # хэ на икс
    text = text.replace('Х', 'X')
    # нэ на эйч
    text = text.replace('Н', 'H')
    # тэ на ти
    text = text.replace('Т', 'T')
    search_rus = rega_rus2eng.match(text)
    if not search_rus:
        logger.info('%s still has rus text' % text)
        assert False
    return text

def replace_eng2rus(text):
    """Заменяем английские символы на русские,
       если остаются английские символы - выдаем ошибку
       :param text: текст, где производим замены
    """
    if not text:
        return
    # икс на хэ
    text = text.replace('X', 'Х')
    # эйч на нэ
    text = text.replace('H', 'Н')
    # ти на тэ
    text = text.replace('T', 'Т')
    search_eng = rega_eng2rus.match(text)
    if not search_eng:
        logger.info('%s still has eng text' % text)
        assert False
    return text

# Тип сварки
WELDING_TYPES = (
    (1, 'РАД'),
    (2, 'РД'),
    (3, 'РАД - РД'),
)

# Материал (сталь)
MATERIALS = (
    (1, '09Г2С'),
    (2, '12Х18Н10Т'),
    (3, '08Х18Н10Т'),
    (4, 'A-358 Gr.316/316L'),
)

JOIN_TYPES = (
    (1, 'труба'),
    (2, 'отвод'),
    (3, 'тройник'),
    (4, 'переходник'),
    (5, 'заглушка'),
    (6, 'фланец'),
    (7, 'штуцер'),
    (8, 'бобышка'),
)
WELDING_JOINT_STATES = (
    (1, 'Новый стык'),
    (2, 'В работе'),
    (3, 'Готовый стык'),
    (4, 'В ремонте'),
)

def get_welding_joint_state(state: str = None):
    """Получение статуса заявки стыка из ссылки
       :param state: значение статуса заявки стыка из ссылки
    """
    state_choices = {
        'new':         1, # 'Новый стык'
        'in_progress': 2, # 'В работе'
        'complete':    3, # 'Готовый стык'
        'in_repair':   4, # 'В ремонте'
    }
    if not state in state_choices:
        return None
    return state_choices[state]
