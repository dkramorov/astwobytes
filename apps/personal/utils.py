# -*- coding:utf-8 -*-
from apps.main_functions.functions import object_fields

def get_user_name(user):
    """Вывести имя пользователя
       :param user: словарь с полями пользователя
       :return: имя пользователя
    """
    if not isinstance(user, dict):
        user = user.to_dict()
    if user['first_name'] and user['middle_name']:
        return '%s %s' % (user['first_name'], user['middle_name'])
    if user['first_name'] and user['last_name']:
        return '%s %s' % (user['last_name'], user['first_name'])
    if user['first_name']:
        return user['first_name']
    if user['last_name']:
        return user['last_name']
    if user['name']:
        return user['name']
    if user['email']:
        return user['email']
    return 'Ваше Вашество'

def save_user_to_request(request, user):
    """Пишем пользователя в сессию
       :param request: HttpRequest
       :param user: Shopper
    """
    #remove_user_from_request(request)
    shopper = user.to_dict()
    shopper['name'] = get_user_name(shopper)
    request.session['shopper'] = shopper.copy()
    #request.session.modified = True

def remove_user_from_request(request):
    """Удаляем пользователя из сессии
       :param request: HttpRequest
    """
    if request.session.get('shopper'):
        del request.session['shopper']
