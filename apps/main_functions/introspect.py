from inspect import currentframe, getframeinfo

def get_debug_info():
    """Получить название файла и номер линии для отладки кода"""
    frameinfo = getframeinfo(currentframe())
    print(frameinfo.filename, frameinfo.lineno)