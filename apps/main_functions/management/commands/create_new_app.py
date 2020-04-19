# -*- coding: utf-8 -*-
import logging
import time
import os
import shutil
import re
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.fortasks import search_process

logger = logging.getLogger(__name__)

def capitalize(app_name, verbose: bool = False):
    """Делаем кэмел-кейс из строки
       первая - заглавная,
       после подчеркивания - заглавная,
       подчеркивания удаляем"""
    if not app_name:
        return app_name
    result = ''
    for i in range(len(app_name)):
        if app_name[i] == '_':
            continue
        if (i == 0) or (i - 1 >= 0 and app_name[i - 1] == '_'):
            result += app_name[i].upper()
        else:
            result += app_name[i]
    if verbose:
        logger.info('capitalize %s => %s' % (app_name, result))
    return result

def test_capitalize():
    """Тестирование преобразований кэмэл-кейса"""
    capitalize('', True)
    capitalize('_', True)
    capitalize('1_', True)
    capitalize('_1', True)
    capitalize('_ab', True)
    capitalize('ab_', True)
    capitalize('_abc_', True)
    capitalize('__abcd__', True)
    capitalize('__ab_cde__', True)
    capitalize('__abc__defg__', True)

def app2settings(app_name):
    """Добавляем новое приложение в settings.py
       :param app_name: новое приложение"""
    settings_path = os.path.join(settings.BASE_DIR, 'conf', 'settings.py')
    with open(settings_path, 'r') as f:
        content = f.read()
    rega_custom_apps = re.compile('# CUSTOM_APPS_START\nCUSTOM_APPS = (.+)\n# CUSTOM_APPS_END', re.I + re.U + re.DOTALL)
    custom_apps_match = rega_custom_apps.search(content)
    CUSTOM_APPS = json.loads(custom_apps_match.group(1))
    CUSTOM_APPS.append('apps.%s' % (app_name, ))
    CUSTOM_APPS = list(set(CUSTOM_APPS))
    new_custom_apps = """
# CUSTOM_APPS_START
CUSTOM_APPS = %s
# CUSTOM_APPS_END""" % (json_pretty_print(CUSTOM_APPS), )
    content = rega_custom_apps.sub(new_custom_apps, content)
    with open(settings_path, 'w') as f:
        f.write(content)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--fake',
            action = 'store_true',
            dest = 'fake',
            default = False,
            help = 'Do nothing')
        parser.add_argument('--fake_value',
            action = 'store',
            dest = 'fake_value',
            type = str,
            default = False,
            help = 'Set fake value')
        parser.add_argument('--app_name',
            action = 'store',
            dest = 'app_name',
            type = str,
            default = False,
            help = 'Set new app name')
        parser.add_argument('--model_name',
            action = 'store',
            dest = 'model_name',
            type = str,
            default = False,
            help = 'Set new model name')

    def handle(self, *args, **options):
        """Создание нового приложения,
           пример использования:
           python manage.py create_new_app --app_name=flattooltip --model_name=FlatToolTip
        """
        is_running = search_process(q = ('create_new_app', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()
        fake_value = 'just fake value'
        if options.get('fake'):
            logger.info('fake value is %s' % (fake_value, ))
            logger.info('sleeping 10 sec')
            time.sleep(10)
            return

        app_name = options.get('app_name')
        model_name = options.get('model_name')
        if not app_name:
            logger.info('you do not set app_name')
            return
        if not model_name:
            logger.info('you do not set model_name')
            return

        apps_path = os.path.join(settings.BASE_DIR, 'apps')
        demo_app_path = os.path.join(apps_path, '_demo_app')
        new_app_path = os.path.join(apps_path, app_name)
        if os.path.exists(new_app_path):
            logger.info('app %s already exists' % (app_name, ))
            return
        shutil.copytree(demo_app_path, new_app_path)

        RENAME_TASKS = {
            'apps.py': [{
                'from': 'demo_app',
                'to': app_name,
            }, {
                'from': 'DemoAppConfig',
                'to': '%sAppConfig' % (capitalize(app_name), ),
            }],
            'models.py': [{
                'from': 'DemoModel',
                'to': capitalize(model_name),
            }],
            'urls.py': [{
                'from': 'demo_app',
                'to': app_name,
            }, {
                'from': 'demo_model',
                'to': model_name,
            }],
            'views.py': [{
                'from': 'demo_model',
                'to': model_name,
            }, {
                'from': 'demo_app',
                'to': app_name,
            }, {
                'from': 'DemoModel',
                'to': capitalize(model_name),
            }],
            'templates/demo_app_admin_menu.html': [{
                'from': 'demo_model',
                'to': model_name,
            }, {
                'from': 'demo_app',
                'to': app_name,
            }],
            'templates/demo_app_edit.html': [{
                'from': 'demo_model',
                'to': model_name,
            }, {
                'from': 'demo_app',
                'to': app_name,
            }],
        }
        for fname, tasks in RENAME_TASKS.items():
            dest = os.path.join(apps_path, app_name, fname)
            with open(dest, 'r') as f:
                content = f.read()
            for task in tasks:
                content = content.replace(task['from'], task['to'])
            with open(dest, 'w') as f:
                f.write(content)

        REPLACE_TASKS = [{
            'from': 'templates/demo_app_admin_menu.html',
            'to': 'templates/%s_admin_menu.html' % (app_name, ),
        }, {
            'from': 'templates/demo_app_edit.html',
            'to': 'templates/%s_edit.html' % (app_name, ),
        }, {
            'from': 'templates/demo_app_table.html',
            'to': 'templates/%s_table.html' % (app_name, ),
        }]
        for task in REPLACE_TASKS:
            source = os.path.join(apps_path, app_name, task['from'])
            dest = os.path.join(apps_path, app_name, task['to'])
            shutil.copy2(source, dest)
            os.unlink(source)

