import datetime

from django.test import TestCase
from django.urls import reverse

from apps.main_functions.fortasks import search_process_created_time
from apps.main_functions.files import create_captcha, check_path
from apps.main_functions.models import Captcha

"""
$ python manage.py test apps.main_functions
"""

class ForTasksTests(TestCase):
    """Тестирование функций для задач
    """
    def test_search_prcess_created_time(self):
        """Тестирование получения времени создания процесса
        """
        test_str = """{'cmdline': ['/bin/bash', '-c', 'source /home/jocker/sites/astwobytes/env/bin/activate && python /home/jocker/sites/astwobytes/manage.py spam_task --spam_delay=15 --images_with_watermarks'], 'create_time': 1617292860.78, 'pid': 44563}"""
        created = search_process_created_time(test_str)
        self.assertTrue(created is not None)
        self.assertTrue(created != '')

class CaptchaTests(TestCase):
    """Тестирование капчи
    """
    def test_create_captcha(self):
        """Тестирование создание капчи
        """
        alphabet = 'abc'
        captcha_size = 11
        text, img = create_captcha(alphabet, captcha_size)
        assert len(text) == 11

        alphabet = '.'
        captcha_size = 3
        text, img = create_captcha(alphabet, captcha_size)
        assert len(text) == 3
        assert text == '...'

    def test_save_captcha(self):
        """Тестирование сохранения капчи
           Внимание: перетрет в папке картинку
        """
        new_captcha = Captcha().gen_captcha(
            alphabet = 'a,b,c,d,e,f'.split(','),
            captcha_size = 7,
        )
        assert len(new_captcha.value) == 7
        assert new_captcha.get_folder() == 'captcha'
        assert not check_path(new_captcha.get_captcha())
        assert new_captcha.get_captcha() == 'captcha/1.png'

