#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math

class MathOperations:
    """Различные математические операции"""
    @staticmethod
    def sma(points: list, cur_position: int, diff: int) -> float:
        """SMA: Простое скользящее среднее
           Это тоже самое, что и среднее арифметическое
           :param points: все точки (median prices)
           :param cur_position: текущая позиция (обычно последняя)
           :param diff: за сколько временных интервалов рассчитываем"""
        result = 0
        # diff вычитаем 1 т/к у него
        # нет нулевого индекса
        count = cur_position - (diff-1)
        if count < 0:
            return None
        # Нужно считать включительно
        # последний пункт

        i = cur_position
        while i >= count:
            result += points[i]
            i -= 1

        result = result/diff
        return result

    @staticmethod
    def std_dev(points: list, cur_position: int, diff: int) -> float:
        """Стандартное отклонение (standard deviation)
           :param points: все точки (median prices)
           :param cur_position: текущая позиция (обычно последняя)
           :param diff: за сколько временных интервалов рассчитываем

           Пример нахождения стандартного отклонения
           от 10 до 70 с шагом 10
           10   20,  30, 40, 50, 60, 70
           40   40,  40, 40, 40, 40, 40 - находим среднее
          -30, -20, -10, 0,  10, 20, 30 - находим разницу
           между значением и средним 10-40, 20-40...
           возводим разницу в квадрат -30*-30 = 900
           900, 400, 100, 0, 100, 400, 900
           суммируем квадраты 2800(900+900+400+400+100+100)
           делим на кол-во элементов выборки минус 1
           2800/(7-1) = 467
           Вычислаем квадратный корень sqrt(467) = 21,6

           diff вычитаем 1 т/к у него нет нулевого индекса"""
        count = cur_position - (diff-1)

        if count < 0:
            return None
        # Среднее
        middle = MathOperations.sma(points, cur_position, diff)
        # Находим разницы между позицией и средним
        # Сразу возводим их в квадрат
        diffs = []
        i = cur_position
        while i >= count:
            cur_diff = points[i] - middle
            diffs.append(pow(cur_diff, 2))
            i -= 1

        # Суммируем квадраты разниц
        squares_summ = 0
        for item in diffs:
            squares_summ += item

        # Делим на кол-во элементов выборки минус 1
        square = squares_summ / (diff-1)
        return math.sqrt(square)

    @staticmethod
    def bollinger_bands(points: list, cur_position: int, diff: int, D: int):
        """Bollinger Bands
           :param points: все точки (median prices)
           :param cur_position: текущая позиция (обычно последняя)
           :param diff: за сколько временных интервалов рассчитываем
           :param D: число стандартных отклонений

           ML = sma(points, cur_position, diff)
           TL(top_line) = ML(middle_line) + D * std_dev
           BL(bottom_line) = ML(middle_line) - D * std_dev

           D = число стандартных отклонений
           diff вычитаем 1 т/к у него нет нулевого индекса"""
        count = cur_position - (diff-1)

        if count < 0:
            return [None, None, None]

        ml = MathOperations.sma(points, cur_position, diff)
        standard_deviation = MathOperations.std_dev(points, cur_position, diff)
        bl = ml + D * standard_deviation
        tl = ml - D * standard_deviation
        return [round(tl, 4), round(ml, 4), round(bl, 4)]

    @staticmethod
    def martingail(digit: int, step: int, multiply: int = 2) -> float:
        """Стратегия Мартингейла
           У нас есть число digit,
           нам надо каждый шаг step удваивать это число
           :param digit: сумма ставки
           :param step: текущий шаг проигрышей подряд
           :param multiply: во сколько раз увеличиваем

           0.35 ставка, выплата 0.66
           35 = 66 (66-35=31 сколько это % от 35?)
           35   100%
           31   ?% 88% => 12% комиссия

           0.7 ставка, выплата 1.36
           70 = 136 (136-70=66 сколько это % от 70?)
           70   100%
           66   ?% 94% => 6% комиссия

           1.4 ставка, выплата 2.72
           140 = 272 (272-140=132 сколько это % от 140?)
           140 = 100%
           132 = ?% 94% => 6% комиссия

           2.8 ставка, выплата 5.44
           280 = 544 (544-280=264 сколько это % от 280?)
           280 = 100%
           264 = ?% 94% => 6% комиссия

           multiply => множитель, по умолчанию 2,
           с множителем в 1,5 можно 6 повторов сделать"""
        summa = 0
        percent = 6
        for i in range(step):
            if i == 0:
                summa += digit
            else:
                # От удваемого числа нужно плюсануть 6%
                # на первом шаге 12%, согласно расчетам
                if i == 1:
                    percent = 12
                six_percents = summa / 100 * percent
                summa = summa * multiply + six_percents
        return summa