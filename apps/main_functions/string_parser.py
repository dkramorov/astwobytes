# -*- coding:utf-8 -*-
import sys
import re
import string
import random
import string

from django.conf import settings

rega_space = re.compile('[\s]+', re.I+re.U+re.DOTALL)
rega_int = re.compile('[^0-9]', re.U+re.I+re.DOTALL)
rega_quotes = re.compile('[\'"`]', re.U+re.I+re.DOTALL)
rega_strict_text = re.compile('[^0-9a-zA-Zа-яА-ЯёЁ/-]', re.U+re.I+re.DOTALL)
rega_html = re.compile('(<[^>]+>)?', re.U+re.I+re.DOTALL)
rega_ip = re.compile("([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})")

def q_string_fill(request, q_string):
    """Заполняем параметры для запроса q_string page, by"""
    page = 1
    by = 20
    q_vars = {'page':1, 'by':20, 'size': None}
    for var in q_vars:
        value = None
        # -----------------------------------------
        # Значения уже могут содержаться в q_string
        # -----------------------------------------
        if var in q_string:
            q_vars[var] = q_string[var]
        # ---
        # GET
        # ---
        if request.method == "GET":
            if request.GET.get(var):
              try:
                  value = int(request.GET[var])
              except ValueError:
                  value = None
        # ----
        # POST
        # ----
        if request.method == "POST":
            if request.POST.get(var):
                try:
                    value = int(request.POST[var])
                except ValueError:
                    value = None
        if value:
            q_vars[var] = value
        # ----------------------------------
        # Вместо by можно передаваться size,
        # вписываем его как by
        # ----------------------------------
        if var == 'size' and value:
            q_vars['by'] = value

    q_string['page'] = q_vars['page']
    if q_string['page'] < 1:
        q_string['page'] = 1
    q_string['by'] = q_vars['by']
    if q_string['by'] < 1:
        q_string['by'] = 20
    q_string['link'] = request.META['PATH_INFO']

def prepare_simple_text(text:str):
    """Убрать из текста хтмл-пробелы типа &nbsp;
       которые хуй увидишь - даже в mysql они
       печатаются обычным пробелом"""
    rega_search = rega_space.search(text)
    if rega_search > -1:
        text = rega_space.sub(' ', text)
    return text.strip()

def string_size(text:str):
    """Размер строки в байтах"""
    size = 0
    if type(text) == str or type(text) == unicode:
        size = sys.getsizeof(text)
    return size

def kill_quotes(item, rega=None, replace=''):
    """Замена в строке на replace символы
       (обычно на "", но можно на пробел
       Своя регулярка, например,
       заменить несколько пробелов на один
       kill_quotes(" Радужный  42", "rega[\s]+", " ")"""
    if not rega:
        rega = rega_space
    elif rega.startswith('rega[') and rega.enswith(']'):
        rega = rega.replace('rega', '')
        rega = re.compile(rega, re.U+re.I+re.DOTALL)
    elif rega == 'int':
        rega = rega_int
    elif rega == 'quotes':
        rega = rega_quotes
    elif rega == 'strict_text':
        rega = rega_strict_text
    else:
        return item
    return rega.sub(replace, item)

def get_request_ip(request):
    """Получаем ip пользователя из request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for #.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def GenPasswd(length:int = 7, alphabet:str = None):
    """Генератор пароля"""
    passwd = []
    if not alphabet:
        alphabet = '%s%s' % (string.ascii_lowercase, string.digits)
    for i in range(length):
        letter = random.randrange(0, len(alphabet))
        passwd.append(alphabet[letter])
    return ''.join(passwd)

def random_boolean():
    """Случайное bool значение"""
    variants = (True, False)
    return variants[random.randrange(0, 2)]

def kill_html(text):
  """Убирает все теги из текста"""
  if text:
      text = rega_html.sub('', text)
  return text

def translit(text):
    """Транслит текста с русского в латиницу"""
    if not text:
        return ''
    alphabet = string.ascii_lowercase
    rus = ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя №')
    eng = ('a', 'b', 'v', 'g', 'd', 'e', 'yo', 'j', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'h', 'c', 'ch', 'sh', 'shh', '', 'y', '', 'e', 'yu', 'ya', '-', '-')
    chars = ('-0123456789_%s' % (alphabet, ))
    result = ''
    for item in text:
        letter = ''
        item = item.lower()
        if item in rus:
            ind = rus.index(item)
            letter = eng[ind]
        else:
            if item in chars:
                letter = item
        result += letter
    return result

def digit_to_str(digit):
    """Число записываем прописью"""
    digits = []
    result = ''
    measure = ('', '', 'миллион', 'миллиард', 'триллион',
               'квадриллион', 'квинтиллион', 'секстиллион',
               'септиллион', 'октиллион', 'нониллион', 'дециллион')
    measure_len = len(measure)
    if not type(digit) == int:
        try:
            digit = float(digit)
        except ValueError:
            digit = 0
    try:
        digit = int(digit)
    except ValueError:
        digit = 0
    digit_str = str(digit)
    digit_len = len(digit_str)

    z = 0

    summa = summa_format(digit)
    if " " in summa:
        digits = summa.split(' ')
    else:
        digits = [summa, ]
    digits.reverse()
    # Каждый триптих обрабатываем, добавляя пояснение (тысячи, милионы)
    z = 0
    for item in digits:
        woman = False
        voca = None
        triptix = item
        if z == 1: # тысячу передаем в женском роде
            woman = True
            voca = ('тысяча', 'тысяч', 'тысячи')
        else:
            if z > 1 and z < (measure_len -1):
                inf = measure[z]
                voca = (inf, inf + 'ов', inf + 'а')
        cur_digit =  analyze_triptix(triptix, woman)
        cur_name =  analyze_digit(triptix, voca)
        if result:
            result = ' ' + result
        cur_result = cur_digit
        if cur_name:
            cur_result += ' ' + cur_name
        result = cur_result + result
        z += 1
    return result

def analyze_triptix(digit, woman=False):
    """Передаем число (максимум трехзначное), пишем его прописью
       woman = False по умолчанию - мужской род, например, "один" (м.б одна)"""
    result = ''
    hundred = dozen = unit = None
    hundred_str = dozen_str = unit_str = ''

    units = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    units_str = ('', 'один', 'два', 'три', 'четыре', 'пять',
                 'шесть', 'семь', 'восемь', 'девять')
    units_str_woman = ('', 'одна', 'две', 'три', 'четыре', 'пять',
                       'шесть', 'семь', 'восемь', 'девять')

    dozens_ten = (10, 11, 12, 13, 14, 15, 16, 17, 18, 19)
    dozens_ten_str =  ('десять', 'одиннадцать', 'двенадцать', 'тринадцать',
                       'четырнадцать', 'пятнадцать', 'шестнадцать',
                       'семнадцать', 'восемнадцать', 'девятнадцать')
    dozens_str = ('', '', 'двадцать', 'тридцать', 'сорок', 'пятьдесят',
                  'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто')

    hundreds_str = ('', 'сто', 'двести', 'триста', 'четыреста', 'пятьсот',
                    'шестьсот', 'семьсот', 'восемьсот', 'девятьсот')

    digit_str = str(digit)
    digit_len = len(digit_str)
    # Записываем unit
    unit = int(digit_str[-1])

    # Записываем dozen & hundred
    if digit_len == 2: # Два разряда
        dozen = int(digit_str[0])
    if digit_len == 3: # Три разряда
        hundred = int(digit_str[0])
        dozen = int(digit_str[1])
    # Если это 10-19
    if dozen == 1:
        # Создаем новый dozen - dozen_ten
        dozen_ten = int("%s%s" % (dozen, unit))
        if dozen_ten in dozens_ten:
            dozen_str = dozens_ten_str[dozens_ten.index(dozen_ten)]
    # Если это 20-99
    else:
        if dozen in units:
            dozen_str = dozens_str[units.index(dozen)]

    if unit in units and not dozen == 1:
        if woman:
            unit_str = units_str_woman[units.index(unit)]
        else:
            unit_str = units_str[units.index(unit)]

    if hundred:
        if hundred in units:
            hundred_str = hundreds_str[units.index(hundred)]

    # Пишем результат
    for item in (hundred_str, dozen_str, unit_str):
        if result:
            result += ' '
        result += item
    return result

def analyze_digit(digit, end:tuple = ('тысяча', 'тысяч', 'тысячи')):
    """Пишет прописью  с нужным окончанием слово (день, год, месяц)
       digit = цифра, от которой зависит окончание
       end = варианты окончаний:
       1 миллион, 10 миллионов, 2 миллиона
       (u"год", u"лет", u"года")
       (u"месяц", u"месяцев", u"месяца")
       (u"день", u"дней", u"дня")"""
    result = ''
    try:
        digit = int(digit)
    except ValueError:
        return result
    if not end:
        return result
    digit_str = str(digit)
    digit_str = int(digit_str[-1])
    # ---------------------------------------
    # На окончания влияет 2 последних символа
    # ---------------------------------------
    if digit_str == 0 or digit_str >=5:
        result = end[1] # тысяч
    if digit_str == 1:
        result = end[0] # тысяча
    if digit_str > 1 and digit_str < 5:
        result = end[2] # тысячи
    if digit > 9:
        digit_str2 = int(str(digit)[-2])
        if digit_str2 == 1:
            result = end[1] # тысяч
    return result

def summa_format(summa):
  """Деньга с пробелами через 3 знака с конца"""
  summa_str = str(summa)
  rub, kop = summa_str, 0
  if '.' in summa_str:
    rub, kop = summa_str.split('.')
  if ',' in summa_str:
    rub, kop = summa_str.split(',')
  summa_tmp = ''
  summa_len = len(rub)
  zero_kop = kop
  try:
      kop = int(kop)
  except ValueError:
      kop = 0

  if summa_len <= 3:
      if kop > 0:
          return summa_str
      return rub
  else:
      for i in range(summa_len):
          if i > 0 and i % 3 == 0:
              summa_tmp = ' ' + summa_tmp
          summa_tmp = rub[summa_len-i-1] + summa_tmp
      summa = summa_tmp

  if kop > 0:
      summa = '%s.%s' % (summa, zero_kop)
  return summa

def ip2long(ip):
    """Преобразуем ip-адрес в число"""
    #>>> o = map(int, "146.0.238.42".split("."))
    #[146, 0, 238, 42]
    #>>> res = (16777216 * o[0]) + (65536 * o[1]) + (256 * o[2]) + o[3];
    #2449534506
    result = None
    search_ip = rega_ip.match(ip)
    if search_ip > -1:
        a, b, c, d = search_ip.group(1), search_ip.group(2), search_ip.group(3), search_ip.group(4)
        ### << Binary Left Shift
        ### The left operands value is moved left by the number of bits specified by the right operand. 	a << = 240 (means 1111 0000)
        ### >> Binary Right Shift
        ### The left operands value is moved right by the number of bits specified by the right operand. 	a >> = 15 (means 0000 1111)
        result = (int(a) << 24) + (int(b) << 16) + (int(c) << 8) + int(d)
    return result

def date_translater(date):
    """Пишет прописью  в нужном падеже дату (день, год, месяц)
       date = {"years":years, "months":months, "days":days}"""
    period_digit = None
    result = ''
    if not date:
        return result
    if "years" in date:
        period_digit = date['years']
        period_padej = ('год', 'лет', 'года')
    if "months" in date:
        period_digit = date['months']
        period_padej = (u"месяц", u"месяцев", u"месяца")
    if "days" in date:
        period_digit = date['days']
        period_padej = (u"день", u"дней", u"дня")
    if not period_digit:
        return result

    result = '%s ' % (period_digit, )
    result += analyze_digit(period_digit, period_padej)
    return result