#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys

# --------------------------------------------
# print sys.maxint # 9 223 372 036 854 775 807
# maxint НЕТ в python3 теперь sys.maxsize
# Хотим хранить 19 разрядное число
# какая нужна вложенность для этого?
# --------------------------------------------
# x/x/x/file - 3 вложенность по 1000
# 1000 * 1000 * 1000 * 1000 = 12
# --------------------------------------------
def get_smart_folder(pk):
    """Папка для хранения изображений/других файлов"""
    MFC = 1000 # максимальное количество файлов в папке
    # -----------------------------------------
    # Нужно разбросать 20 разрядов по папкам,
    # как это будем делать?
    # Исходим из максимального кол-ва файлов
    # в папке = 1000, тогда
    # -----------------------------------------
    # 1000 папок на верхнем уровне и в каждой
    # по 1000 файлов дает нам 1млн (6 разрядов)
    # -----------------------------------------
    # 1000 папок => 1000 => 1000 = 9 разрядов
    # 4 уровень вложенности = 12 разрядов
    # 5 уровень вложенности = 15 разрядов
    # 6 уровень вложенности = 18 разрядов
    # 7 уровень вложенности = 21 разряд
    # -----------------------------------------

    # -----------------------------------------
    # Нужно кодировать айдишник так, чтобы
    # чем выше было число, тем больше была
    # вложенность - до 6 знаков (1млн) ложим
    # просто в подпапки 1 уровня 409/file
    # -----------------------------------------
    # затем, ложим во второй уровень
    # 1/999/file это 12 разрядов
    # -----------------------------------------
    # затем, ложим в третий уровень
    # 24/53/180/file
    # -----------------------------------------
    # Каждые три разряда повышаем вложенность
    # -----------------------------------------
    # Поэтому просто раскладываем по 3 разряда
    # -----------------------------------------
    pk_str = str(pk)

    pk_array = []
    pk_str = str(pk)[::-1]
    for i, y in enumerate(pk_str):
        if not i % 3:
            pk_array.append(pk_str[i:i+3][::-1])

    result = []
    for item in pk_array[::-1]:
        try:
            item = int(item)
        except ValueError:
            assert False
        result.append(item)

    folder = ""
    for item in result:
        folder += "%s/" % (item, )
    return folder

# -----------------------
# Test case/demo in place
# -----------------------
if __name__ == "__main__":
    tests = (
        123, 123321, 1234567890,
        0, 99, 100, 101, 999, 1000, 1001, 2000,
        50000, 100000, 1000000, 10000000, 25000000, 26000000, 34567891,
        123456789012, 987654321012345678, sys.maxsize,
    )
    for item in tests:
        print(item, "=>", get_smart_folder(item))
