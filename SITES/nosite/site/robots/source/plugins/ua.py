# -*- coding:utf-8 -*-
import os
import json
import random

def luser_agents():
    """Последние версии браузеров (last user agent ну или просто лузерагент)
       https://www.whatismybrowser.com/guides/the-latest-user-agent/?utm_source=whatismybrowsercom
    """
    user_agents = {
        'chrome': {
            'windows': [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            ],
            'mac': [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            ],
            'linux': [
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            ],
            'ios': [
                'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4103.88 Mobile/15E148 Safari/604.1',
            ],
            'android': [
                'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
            ],
        },
        'firefox': {
            'windows': [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            ],
            'mac': [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            ],
            'linux': [
                'Mozilla/5.0 (Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
            ],
            'ios': [
                'Mozilla/5.0 (iPhone; CPU iPhone OS 10_15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/27.0 Mobile/15E148 Safari/605.1.15',
            ],
            'android': [
                'Mozilla/5.0 (Android 10; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0',
            ],
        },
        'safari': {
            'mac': [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            ],
            'ios': [
                'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/83.0.4103.88 Mobile/15E148 Safari/604.1',
            ],
        },
        'opera': {
            'windows': [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/68.0.3618.173',
            ],
            'mac': [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/68.0.3618.173',
            ],
            'linux': [
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/68.0.3618.173',
            ],
            'android': [
                'Mozilla/5.0 (Linux; Android 10; VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36 OPR/55.2.2719',
            ]
        },
        'yandex': {
            'windows': [
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 YaBrowser/20.4.0 Yowser/2.5 Safari/537.36',
            ],
            'mac': [
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 YaBrowser/20.4.0 Yowser/2.5 Safari/537.36',
            ],
            'ios': [
                'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 YaBrowser/20.4.4.227 Mobile/15E148 Safari/604.1',
            ],
            'android': [
                'Mozilla/5.0 (Linux; arm_64; Android 10; SM-G965F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 YaBrowser/20.4.2 Mobile Safari/537.36',
            ],
        }
    }
    return user_agents

def generate_ua():
    """Возвращаем user_agent по luser_agents последовательно
       DEMO USAGE:
       g = generate_ua()
       for i in range(600):
           print(next(g))
    """
    user_agents = luser_agents()
    i = 0 # family
    j = 0 # os
    while True:
        keys = list(user_agents.keys())
        subkeys = list(user_agents[keys[i]])
        if j >= len(subkeys):
            j = 0
            i += 1
            if i >= len(keys):
                i = 0
            subkeys = list(user_agents[keys[i]])
        yield user_agents[keys[i]][subkeys[j]]
        j += 1

def update_ua_in_all_profiles():
    """Обновление user_agent во всех профилях"""
    g = generate_ua()
    profiles_folder = '/home/jocker/selenium/profiles/chrome/'
    for item in os.listdir(profiles_folder):
        path = os.path.join(profiles_folder, item)
        if not os.path.isfile(path):
            ua_file = os.path.join(path, 'ua.json')
            with open(ua_file, 'w+', encoding='utf-8') as f:
                f.write(json.dumps({
                    'ua': next(g),
                    'starts_counter': 0,
                }))

def show_ua_from_all_profiles():
    """Показываем user_agent во всех профилях"""
    profiles_folder = '/home/jocker/selenium/profiles/chrome/'
    for item in os.listdir(profiles_folder):
        path = os.path.join(profiles_folder, item)
        if not os.path.isfile(path):
            ua_file = os.path.join(path, 'ua.json')
            with open(ua_file, 'r', encoding='utf-8') as f:
                ua = json.loads(f.read())
                print('%s: %s, %s' % (item, ua['ua'], ua['starts_counter']))
                print('-----------------')

def generate_user_agent():
    """Выбор случайного user_agent"""
    rand = random.randrange(100)
    g = generate_ua()
    for i in range(rand):
        ua = next(g)
    return ua

if __name__ == '__main__':
    #update_ua_in_all_profiles()
    #show_ua_from_all_profiles()
    print(generate_user_agent())

