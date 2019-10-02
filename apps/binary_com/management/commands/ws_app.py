# -*- coding: utf-8 -*-
import math

from lomond import WebSocket, events
from lomond.persist import persist

from apps.main_functions.date_time import timestamp_to_date

class WS:
    def __init__(self, websocket):
        self.websocket = websocket

        self.MAX_TICKS = 1000
        self.BOLLINGER_BANDS_STEPS = 20
        self.STANDARD_DEVIATIONS = 2
        self.BUY_FROM_LOOSE_COUNT = 6

        #self.ws_token = 'S2CdZcfFPZ6Q0A2'
        #self.ws_token_real = 'vwG5V6Vo66jUpqq'
        self.ws_token = 'HuHXzecHbYEr66i' # info-223-4
        self.symbol = 'R_50'
        self.ticks_array = []
        self.deals_array = []

    def check_event(self, event):
        """Определить что за событие пришло к нам,
           в зависимости от этого выполнить действия"""
        ws_events = {
            events.Ready:          'ready',
            events.Text:           'text',
            events.Binary:         'binary',
            events.BackOff:        'backoff',
            events.Closed:         'closed',
            events.Closing:        'closing',
            events.ConnectFail:    'connectfail',
            events.Connected:      'connected',
            events.Connecting:     'connecting',
            events.Disconnected:   'disconnected',
            events.Ping:           'ping',
            events.Poll:           'poll',
            events.Pong:           'pong',
            events.ProtocolError:  'protocolerror',
            events.Rejected:       'rejected',
            events.Unresponsive:   'unresponsive',
            events.UnknownMessage: 'unknownmessage',
        }
        etype = type(event)

        if ws_events[etype] == 'text':
            # Получено текстовое сообщение
            msg_type = event.json.get('msg_type')

            if msg_type in ('ping', 'pong', 'poll'):
                pass
            elif msg_type == 'history':
                # Если пришла история тиков, подписываемся на поток тиков
                self.save_ticks(event.json.get('history'))
                self.subscribe_ticks_stream()
            elif msg_type == 'tick':
                # Получаем поток тиков
                self.save_tick(event.json.get('tick'))
            elif msg_type == 'authorize':
                # Авторизация
                print(event.json)
                self.buy('CALL')

            elif msg_type == 'buy':
                # Покупка контракта
                print(event.json)
            elif msg_type == 'proposal_open_contract':
                # Мы подписаны на сделку по контракту
                print(event.json)
            else:
                print(event.text)
        # -------------
        # Событие READY
        # -------------
        elif ws_events[etype] == 'ready':
            # Websocket готов ибошить
            self.get_ticks_history()
            self.authorize()
        else:
            print('---> event %s, text %s' % (etype, event))

    def save_ticks(self, history: list = None):
        """Сохраняем полученную историю по тикам"""
        self.ticks_array = []
        for i, item in enumerate(history['prices']):
            tick = {
                'quote': history['prices'][i],
                'epoch': history['times'][i],
            }
            self.save_tick(tick)

    def save_tick(self, tick):
        """Запоминаем полученные тики в потоке"""
        new_tick = [tick['epoch'], float(tick['quote'])]
        self.ticks_array.append(new_tick)
        if len(self.ticks_array) > self.MAX_TICKS:
            self.ticks_array.pop(0)
        # Докидываем боллинджера в тик
        # третий элемент массива в
        # каждом тике со словарем
        prices = [item[1] for item in self.ticks_array]

        for i in range(len(self.ticks_array)):
            cur_item = self.ticks_array[i]
            # Линии болленджера
            # top, middle, bottom
            if len(cur_item) >= 3:
                continue
            bb = bollinger_bands(prices,
                                 i,
                                 self.BOLLINGER_BANDS_STEPS,
                                 self.STANDARD_DEVIATIONS)
            cur_item.append(bb)

    def authorize(self):
        """Авторизация"""
        self.websocket.send_json({
            'authorize': self.ws_token,
        });

    def get_ticks_history(self):
        """Запрашиваем историю по тикам"""
        self.websocket.send_json({
            'ticks_history': self.symbol,
            'end': 'latest',
            'start': 1,
            'style': 'ticks',
            'adjust_start_time': 1,
            'count': self.MAX_TICKS,
        })

    def subscribe_ticks_stream(self):
        """Подписаться на поток тиков по контракту"""
        self.websocket.send_json({
            'ticks': self.symbol,
            'subscribe': 1,
        });

    def unsubscribe_ticks_stream(self):
        """Отписаться от потока тиков по контракту"""
        self.websocket.send_json({
            'forget': self.symbol,
        });

    def buy(self, contract_type):
        """Делаем ставку, т/к условия удовлетворены"""
        deal_params = {
            'contract_type': contract_type,
            'amount': self.calc_rates(),
            'symbol': self.symbol,
            'duration_unit': 't',
            'duration': 5,
            'basis': 'stake',
            'currency': 'USD',
            'amount': '0.35',
        }

        deal = {"parameters": deal_params}
        deal['price'] = deal_params['amount']
        deal['buy'] = 1
        deal['subscribe'] = 1

        self.websocket.send_json(deal);

    def playboy(self):
        """Играем, нах"""
        epoch = 0
        last_deal = None
        # -----------------------------------
        # Ищем по контракту последнюю сделку,
        # от нее считать будем
        # -----------------------------------
        if self.deals_array:
            # --------------------------------
            # Если последняя сделка еще
            # не завершена, тогда пока ожидаем
            # --------------------------------
            last_deal = self.deals_array[-1]
            if last_deal['status'] == 'open':
                # ----------------------------------------------------
                # Бывают ситуации, когда больше уведомление не придет,
                # т/к сделка закрыта, но событие еще не сработало,
                # это попытка обработать такую ситуацию
                # ----------------------------------------------------
                is_server_bug = False
                if last_deal.get('audit_details'):
                    is_server_bug = True
                if not is_server_bug:
                    return
            epoch = self.deals_array[-1]['date_expiry']
        # ---------------------------------
        # Проверяем последний тик,
        # должно быть касание верхней линии
        # ---------------------------------
        ticks_len = self.ticks_array.length
        if ticks_len < 10:
            return

        last_tick = self.ticks_array[1]

        bb = last_tick[2]
        if last_tick[1] > bb[0]:
            # ---------------------------------------------------
            # Если после предыдущей сделки не был касание центра,
            # то защищаемся от тренда и не делаем ставку
            # ---------------------------------------------------
            if last_deal:
                # ---------------------------
                # Идем в обратном направлении
                # Ищем пересечение центра
                # ---------------------------
                for i, tick in enumerate(self.ticks_array):
                    bb = tick[2];
                    # -------------------
                    # Пересечения не было
                    # -------------------
                    if epoch > tick[0]:
                        break
                    # ----------------
                    # Пересечение было
                    # ----------------
                    if tick[1] <= bb[1]:
                        self.buy('PUT')
                        break
            else:
                self.buy('PUT')
        elif last_tick[1] < bb[2]:
            # ----------------------------------------------------
            # Если после предыдущей сделки не было касание центра,
            # то защищаемся от тренда и не делаем ставку
            # ----------------------------------------------------
            if last_deal:
                # ---------------------------
                # Идем в обратном направлении
                # Ищем пересечение центра
                # ---------------------------
                for i, tick in enumerate(self.ticks_array):
                    bb = tick[2]
                    # -------------------
                    # Пересечения не было
                    # -------------------
                    if epoch > tick[0]:
                        break
                    # ----------------
                    # Пересечение было
                    # ----------------
                    if tick[1] >= bb[1]:
                        self.buy('CALL')
                        break
            else:
                self.buy('CALL')

    def get_loose_count(self):
        """Рассчитываем сколько раз мы уже серанули"""
        loose_count = 1
        for deal in self.deals_array[::-1]:
          if deal['status'] == 'lost':
              loose_count += 1
          else:
            # ------------------------------------
            # Если какая то сделка без информации,
            # пропускаем ее
            # ------------------------------------
            if deal['status'] == 'open':
                continue
            break
        return loose_count

    def calc_rates(self):
        """Высчитываем с помощью мартингейла
           сколько мы должны сейчас поставить"""
        digit = 0.35
        max_loose_count = 5
        multiply = 2
        loose_count = self.get_loose_count()

        while loose_count > max_loose_count:
            loose_count = loose_count - max_loose_count
        return martingail(digit, loose_count, multiply)

# -----------------------------------------------
# У нас есть число digit,
# нам надо каждый шаг step удваивать это число
# -----------------------------------------------
# 0.35 ставка, выплата 0.66
# 35 = 66 (66-35=31 сколько это % от 35?)
# 35   100%
# 31   ?% 88% => 12% комиссия
# -----------------------------------------------
# 0.7 ставка, выплата 1.36
# 70 = 136 (136-70=66 сколько это % от 70?)
# 70   100%
# 66   ?% 94% => 6% комиссия
# -----------------------------------------------
# 1.4 ставка, выплата 2.72
# 140 = 272 (272-140=132 сколько это % от 140?)
# 140 = 100%
# 132 = ?% 94% => 6% комиссия
# -----------------------------------------------
# 2.8 ставка, выплата 5.44
# 280 = 544 (544-280=264 сколько это % от 280?)
# 280 = 100%
# 264 = ?% 94% => 6% комиссия
# -----------------------------------------------
# multiply => множитель, по умолчанию 2,
# с множителем в 1,5 можно 6 повторов сделать
# -----------------------------------------------
def martingail(digit, step, multiply):
    summa = 0
    percent = 6

    for i in range(step):
        if i == 0:
            summa += digit
        else:
            # -------------------------------------
            # От удваемого числа нужно плюсануть 6%
            # на первом шаге 12%, согласно расчетам
            # -------------------------------------
            if i == 1:
                percent = 12

            six_percents = summa / 100 * percent
            summa = summa * multiply + six_percents
    return float(summa)

# ---------------------------------------------------
# SMA: Простое скользящее среднее
# Это тоже самое, что и среднее арифметическое
# points = все точки (median prices)
# cur_position - текущая позиция (последняя?)
# diff - за сколько временных интервалов рассчитываем
# ---------------------------------------------------
def sma(points, cur_position, diff):
  result = 0
  # --------------------------
  # diff вычитаем 1 т/к у него
  # нет нулевого индекса
  # --------------------------
  count = cur_position - (diff-1)
  if count < 0:
    return

  # --------------------------
  # Нужно считать включительно
  # последний пункт
  # --------------------------
  i = cur_position
  while i >= count:
    result += float(points[i])
    i -= 1

  result = result/diff
  return result

# ---------------------------------------------------
# Стандартное отклонение (standard deviation)
# points = все точки (median prices)
# cur_position - текущая позиция (последняя?)
# diff - за сколько временных интервалов рассчитываем
# Пример нахождения стандартного отклонения
# от 10 до 70 с шагом 10
#  10   20,  30, 40, 50, 60, 70
#  40   40,  40, 40, 40, 40, 40 - находим среднее
# -30, -20, -10, 0,  10, 20, 30 - находим разницу
# между значением и средним 10-40, 20-40...
# возводим разницу в квадрат -30*-30 = 900
# 900, 400, 100, 0, 100, 400, 900
# суммируем квадраты 2800(900+900+400+400+100+100)
# делим на кол-во элементов выборки минус 1
# 2800/(7-1) = 467
# Вычислаем квадратный корень sqrt(467) = 21,6
# diff вычитаем 1 т/к у него нет нулевого индекса
# ---------------------------------------------------
def std_dev(points, cur_position, diff):
    result = 0
    count = cur_position - (diff-1)

    if count < 0:
      return
    # -------
    # Среднее
    # -------
    middle = sma(points, cur_position, diff)
    # ----------------------------------------
    # Находим разницы между позицией и средним
    # Сразу возводим их в квадрат
    # ----------------------------------------
    diffs = []
    i = cur_position
    while i >= count:
      cur_diff = points[i] - middle
      diffs.append(pow(cur_diff, 2))
      i -= 1

    # -------------------------
    # Суммируем квадраты разниц
    # -------------------------
    squares_summ = 0
    for j in range(len(diffs)):
      squares_summ += diffs[j]

    # -----------------------------------------
    # Делим на кол-во элементов выборки минус 1
    # -----------------------------------------
    square = squares_summ / (diff-1)
    # ---------------------------
    # Вычисляем квадратный корень
    # ---------------------------
    result = math.sqrt(square)
    return result

# -----------------------------------------------
# Bollinger Bands
# ML = sma(points, cur_position, diff)
# TL(top_line) = ML(middle_line) + D * std_dev
# BL(bottom_line) = ML(middle_line) - D * std_dev
# D = число стандартных отклонений
# diff вычитаем 1 т/к у него нет нулевого индекса
# -----------------------------------------------
def bollinger_bands(points, cur_position, diff, D):
    result = []
    count = cur_position - (diff-1)

    if count < 0:
      return [None, None, None]

    ml = sma(points, cur_position, diff)
    standard_deviation = std_dev(points, cur_position, diff)
    tl = ml + D * standard_deviation
    bl = ml - D * standard_deviation
    result = [tl, ml, bl]
    return result

websocket = WebSocket('wss://ws.binaryws.com/websockets/v3?app_id=1089&l=RU')
ws = WS(websocket)
for event in persist(websocket):
    ws.check_event(event)
