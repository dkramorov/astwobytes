import inspect
from optparse import OptionParser


def get_debug_info():
    """Получить название файла и номер линии для отладки кода"""
    frameinfo = inspect.getframeinfo(inspect.currentframe())
    print(frameinfo.filename, frameinfo.lineno)
    return frameinfo.filename, frameinfo.lineno

def get_class_methods(instance):
    """Получить методы класса instance
       :param instance: класс, где ищем методы
    """
    return inspect.getmembers(OptionParser, predicate=inspect.isfunction)