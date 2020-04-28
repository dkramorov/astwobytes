# -*- coding:utf-8 -*-
import os
import requests

# requirements
# pyperclip==1.8.0
import pyperclip
# DEMO USAGE buffer-clip
# pyperclip.copy('123')
# pyperclip.paste() # 123

# pynput==1.6.8
from pynput.keyboard import Key, Listener
#def on_press(key):
#    print('{0} pressed'.format(key))
#def on_release(key):
#    print('{0} release'.format(key))
#    if key == Key.esc:
#        return False
# Collect events until released
#with Listener(on_press=on_press, on_release=on_release) as listener:
#    listener.join()

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

def translate(sl: str = 'en', tl: str = 'ru', q: str = 'hello', max_len: int = 50):
    """Перевод через google translate
       :param sl: с какого языка переводим
       :param tl: на какой язык переводим
       :param q: текст, который переводим, если пусто - берем из буфера
       :param max_len: максимальная длина текста
    """
    if not q:
        q = pyperclip.paste()
    if not q:
        return ''
    if len(q) > max_len:
        return ''
    r = requests.get('https://translate.google.com/translate_a/single?client=at&dt=t&dt=ld&dt=qca&dt=rm&dt=bd&dj=1&hl=uk-RU&ie=UTF-8&oe=UTF-8&inputm=2&otf=2&iid=1dd3b944-fa62-4b55-b330-74909a99969e&sl=%s&tl=%s&q=%s' % (sl, tl, q))
    if r.status_code == 429:
        print(r.status_code, 'Too many requests')
        notify(title    = 'Перевод',
               subtitle = '%s =>' % q,
               message  = 'Слишком много запросов, выходим...')
        exit()
    try:
        resp = r.json()
        sentences = resp.get('sentences', [])
        if sentences:
            result = sentences[0].get('trans')
            print('%s => %s' % (q, result))
            notify(title    = 'Перевод',
                   subtitle = '%s =>' % q,
                   message  = result)
            return result
    except Exception as e:
        print('status_code', r.status_code)
        print('error', e)
        notify(title    = 'Перевод',
               subtitle = '%s =>' % q,
               message  = e)
    return ''

def on_press(key):
    pass
def on_release(key):
    if key == Key.cmd:
        translate(q='')

if __name__ == '__main__':
    #print(translate(q='the weather is fine'))
    #print(translate(q=''))
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
