# -*- coding:utf-8 -*-
import os
import random
import time

from simple_logger import logger

def notify(title, subtitle: str = '', message: str = ''):
    """Push-уведомление
       сначала install terminal-notifier
       :param title заголовок
       :param subtitle: подзаголовок
       :param message: сообщение"""
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

if __name__ == '__main__':
    total = 0
    limit = 50
    while True:
        pullup_count = random.randrange(3,7)
        notify(title    = 'Го подтягиваться!',
               subtitle = 'ну давай %s' % pullup_count,
               message  = 'Жопу оторвал, на турникан пошел')
        total += pullup_count
        logger.info('заходим на %s, итого %s, осталось %s' % (pullup_count, total, limit - total))
        if total >= limit:
            logger.info('Молодца, на сегодня хва')
            break
        time.sleep(random.randrange(5*60, 10*60))