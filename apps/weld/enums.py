# -*- coding: utf-8 -*-
import re
import logging

logger = logging.getLogger('main')

rega_rus2eng = re.compile('^[a-z0-9\s/-]+$', re.I+re.U+re.DOTALL)
rega_eng2rus = re.compile('^[а-я0-9\s/-]+$', re.I+re.U+re.DOTALL)

def replace_rus2eng(text:str, force_return: bool = False):
    """Заменяем русские символы на английские,
       если остаются русские символы - выдаем ошибку
       :param text: текст, где производим замены
       :param force_return: возвратить то, что удалось преобразовать
    """
    if not text:
        return
    # хэ на икс
    text = text.replace('Х', 'X')
    # нэ на эйч
    text = text.replace('Н', 'H')
    # тэ на ти
    text = text.replace('Т', 'T')
    # а на эй
    text = text.replace('А', 'A')
    # вэ на б
    text = text.replace('В', 'B')
    # сэ на си
    text = text.replace('С', 'C')
    # мэ на эм
    text = text.replace('М', 'M')
    # рэ на пи
    text = text.replace('Р', 'P')
    # о на оу
    text = text.replace('О', 'O')
    # е(бана) на е
    text = text.replace('Е', 'E')
    search_rus = rega_rus2eng.match(text)
    if not search_rus:
        if not force_return:
            logger.info('%s still has rus text' % text)
            assert False
    return text

def replace_eng2rus(text: str, force_return: bool = False):
    """Заменяем английские символы на русские,
       если остаются английские символы - выдаем ошибку
       :param text: текст, где производим замены
       :param force_return: возвратить то, что удалось преобразовать
    """
    if not text:
        return
    # икс на хэ
    text = text.replace('X', 'Х')
    # эйч на нэ
    text = text.replace('H', 'Н')
    # ти на тэ
    text = text.replace('T', 'Т')
    # эй на а
    text = text.replace('A', 'А')
    # б на вэ
    text = text.replace('B', 'В')
    # си на сэ
    text = text.replace('C', 'С')
    # эм на мэ
    text = text.replace('M', 'М')
    # пи на рэ
    text = text.replace('P', 'Р')
    # оу на о
    text = text.replace('O', 'О')
    # е на е(бана)
    text = text.replace('E', 'Е')
    search_eng = rega_eng2rus.match(text)
    if not search_eng:
        logger.info('%s still has eng text' % text)
        if not force_return:
            assert False
    return text

# Тип сварки
WELDING_TYPES = (
    (1, 'РАД'),
    (2, 'РД'),
    (3, 'РАД - РД'),
)
WELDING_TYPE_DESCRIPTIONS = (
    (1, 'ручной аргонодуговой сваркой'), # РАД
    (2, 'ручной дуговой сваркой'), # РД
    (3, 'комбинированной сваркой'), # РАД - РД
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
    (4, 'переход'),
    (5, 'заглушка'),
    (6, 'фланец'),
    (7, 'штуцер'),
    (8, 'бобышка'),
    (9, 'пробка'),
    (10, 'клапан'),
    (11, 'задвижка'),
    (12, 'кран'),
    (13, 'затвор'),
)
WELDING_JOINT_STATES = (
    (1, 'Новый'),
    (2, 'На контроле ЗНК'), # В работе
    (3, 'Годен'), # Готов
    (4, 'В ремонте'),
    (5, 'Заявка отклонена'),
)
# Оценка качества в заключениях
CONCLUSION_STATES = (
    (1, 'Годен'),
    (2, 'Ремонт'),
    (3, 'Вырез'),
    (4, 'УЗК'),
    (5, 'Пересвет'),
    (6, 'Брак'),
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
        'rejected':    5, # 'Заявка отклонена'
    }
    if not state in state_choices:
        return None
    return state_choices[state]

DIAMETERS = (
  10, 11, 13, 14, 15, 20, 21, 22, 25, 27, 28, 32,
  33, 35, 45, 50, 57, 60, 80, 89, 100, 108, 109,
  110, 114, 159, 168, 219, 273, 284, 325, 377,
  426, 477, 530, 820, 1200,
)