import json
import datetime
import redis

from django.conf import settings
from django.db.models import Count, F, Q

from apps.main_functions.string_parser import kill_quotes
from apps.spamcha.models import SMSPhone

def get_phones_from_cache():
    """Получить телефоны из кэша, которые на связи с вебсокетом"""
    rediska = redis.Redis()
    phones = rediska.get('%s_PHONES' % settings.SMS_HUB_TOKEN)
    if not phones:
        return []
    return json.loads(phones)

def get_phones(cond_list: list = None, respect_limit: bool = True):
    """Получить телефоны по условиям
       :param cond_list: условия для выборки, которые добавим в filter
       :param respect_limit: выбрать телефоны, которые не прошибли лимит
    """
    query = SMSPhone.objects.all()
    if respect_limit:
        query = query.filter(Q(sent__lt=F('limit'))|Q(sent__isnull=True))

    if not cond_list:
        cond_list = []
    for cond in cond_list:
        if isinstance(cond, dict):
            query = query.filter(**cond)
        else:
            query = query.filter(**cond)
    phones = query.values('id', 'name', 'phone', 'code', 'sent', 'limit')
    return list(phones)

def get_sms_volume(text):
    """1 SMS на латинице вмещает до 160 символов,
       1 SMS на кириллице — 70 символов
       Берем с запасом - 150 vs 65
    """
    sms_parts = 0
    sms_part_len = 65
    if not text:
        return 0
    text_len = len(text)
    while text_len > 0:
        text_len -= sms_part_len
        sms_parts += 1
    return sms_parts

def send_sms_helper(request):
    """Вспомогательная функция,
       чтобы отправить sms
       1) достаем из spamcha телефоны для рассылки,
          смотрим по лимитам кто может отправить смс,
          следим за балансировкой - кто сколько отправил
       2) у нас должен работать sms_hub.py на порту (5009)
          подключаемся в него и отправляем смс на телефон
    """
    result = {}
    method = request.GET if request.method == 'GET' else request.POST
    text = method.get('text')
    phone = method.get('phone')
    token = method.get('token')
    if not token == settings.SMS_HUB_TOKEN:
        result['error'] = 'Неправильный токен'
        return result
    if not phone or not text:
        result['error'] = 'Телефон или сообщение отсутствует'
        return result
    phone = kill_quotes(phone, 'int')
    if len(phone) != 11:
        result['error'] = 'Телефон должен быть из 11 цифр'
        return result
    receiver_number = '8%s' % phone[1:]
    if not receiver_number.startswith('89'):
        result['error'] = 'Телефон не должен быть городским (начинаться с 89)'
        return result

    # Вариант узнать какие телефоны на связи, только через
    phones_from_cache = get_phones_from_cache()

    # --------------------------------------------
    # Телефоны на связи, если дата меньше сегодня,
    # нужно просто пересохранять,
    # чтобы обновился счетчик отправленных смсин
    # --------------------------------------------
    now = datetime.datetime.today()
    today = datetime.datetime(now.year, now.month, now.day, 0, 30, 0)
    refresh_query = SMSPhone.objects.filter(updated__lt=today)
    for_refresh = refresh_query.aggregate(Count('id'))['id__count']
    if for_refresh:
        for item in refresh_query:
            item.sent = 0
            item.save()

    # Находим телефоны через которые можно отправить смс
    cond_list = [{'code__in': phones_from_cache}]
    phones = get_phones(cond_list=cond_list)
    if not phones:
        result['error'] = 'Нет телефонов для отправки смс'
        return result

    candidate = phones[0]
    if not candidate['sent']:
        candidate['sent'] = 0
    for phone in phones:
        if not phone['sent']:
            phone['sent'] = 0
        if phone['sent'] < candidate['sent']:
            candidate = phone

    # Отправка в кэш-очередь смсины
    rediska = redis.Redis()
    cache_key = '%s_%s' % (settings.SMS_HUB_TOKEN, candidate['code'])
    queue = rediska.get(cache_key)
    if queue:
        queue = json.loads(queue)
    else:
        queue = []
    queue.append({'phone': receiver_number, 'text': text})
    rediska.set(cache_key, json.dumps(queue))

    # Накидываем кол-во отправленных смсин
    candidate['sent'] += get_sms_volume(text)
    SMSPhone.objects.filter(pk=candidate['id']).update(sent=candidate['sent'])

    result['success'] = 1
    return result
