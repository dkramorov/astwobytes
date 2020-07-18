# -*- coding: utf-8 -*-
import re

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
    (3, 'РАД/РД'),
)
