import datetime

from django.test import TestCase
from django.urls import reverse

from apps.main_functions.fortasks import search_process_created_time

class ForTasksTests(TestCase):
    """Тестирование функций для задач"""
    def test_search_prcess_created_time(self):
        """Тестирование получения времени создания процесса
        """
        test_str = """{'cmdline': ['/bin/bash', '-c', 'source /home/jocker/sites/astwobytes/env/bin/activate && python /home/jocker/sites/astwobytes/manage.py spam_task --spam_delay=15 --images_with_watermarks'], 'create_time': 1617292860.78, 'pid': 44563}"""
        created = search_process_created_time(test_str)
        self.assertTrue(created is not None)
        self.assertTrue(created != '')




