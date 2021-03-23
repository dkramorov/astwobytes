# -*- coding:utf-8 -*-
import logging

from apps.personal.models import Shopper

logger = logging.getLogger('main')

def phone_confirmed(request):
    """Выставить флаг,
       что телефон пользователя подтвержден
    """
    shopper = request.session.get('shopper')
    if not shopper:
        return False
    elif isinstance(shopper, dict):
        sid = shopper.get('id')
    elif isinstance(shopper, Shopper):
        sid = shopper.id
    else:
        return False
    Shopper.objects.filter(pk=sid).update(phone_confirmed=True)
    try:
        del request.session['confirm_phone']
    except Exception as e:
        logger.info(e)
    user = Shopper.objects.get(pk=sid)
    request.session['shopper'] = user.to_dict()
    request.session.save()
    return True

def login_from_site(request):
    """Авторизация пользователя через форму на сайте
       :param request: HttpRequest
       :return: list(errors) or Shopper instance
    """
    result = None
    method = request.GET if request.method == 'GET' else request.POST
    login = method.get('login')
    passwd = method.get('passwd')
    if login and passwd:
        result = Shopper.objects.filter(
            is_active=1,
            login=login,
            passwd=passwd,
            oauth=1).first()
    if not result:
        result = ['Неправильная пара логин/пароль']
    return result

def register_from_site(request):
    """Регистрация пользователя через форму на сайте
       :param request: HttpRequest
       :return: list(errors) or Shopper instance
    """
    method = request.GET if request.method == 'GET' else request.POST
    result = register_from_site_helper({
        'name': method.get('name'),
        'first_name': method.get('first_name'),
        'last_name': method.get('last_name'),
        'middle_name': method.get('middle_name'),
        'email': method.get('email'),
        'phone': method.get('phone'),
        'address': method.get('address'),
        'login': method.get('login'),
        'passwd': method.get('passwd'),
        'passwd2': method.get('passwd2'),
    })
    return result

def register_from_site_helper(params: dict):
    """Вспомогательная функция для регистрации пользователя
       :param params: параметры для регистрации пользователя
       :return: list(errors) or Shopper instance
    """
    errors = []
    keys = (
        'name',
        'first_name',
        'last_name',
        'middle_name',
        'email',
        'phone',
        'address',
        'login',
        'passwd',
    )
    if not 'login' in params:
        errors.append('Введите логин')
    elif len(params['login']) < 3:
        errors.append('Логин должен быть длиннее трех символов')
    if not 'passwd' in params:
        errors.append('Введите пароль')
    if not params.get('passwd') == params.get('passwd2'):
        errors.append('Введенные пароли не совпадают')
    if errors:
        return errors
    analog = Shopper.objects.filter(login=params['login']).first()
    if analog:
        errors.append('Такой логин уже занят')
        return errors
    shopper = Shopper(oauth=1)
    for key in keys:
        setattr(shopper, key, params.get(key))
    shopper.save()
    return shopper

def update_profile_from_site(request):
    """Изменение информации о пользователе через форму на сайте
       :param request: HttpRequest
       :return: list(errors) or Shopper instance
    """
    method = request.GET if request.method == 'GET' else request.POST
    shopper = request.session.get('shopper')
    result = update_profile_from_site_helper(shopper, {
        'name': method.get('name'),
        'first_name': method.get('first_name'),
        'last_name': method.get('last_name'),
        'middle_name': method.get('middle_name'),
        'email': method.get('email'),
        'phone': method.get('phone'),
        'address': method.get('address'),
        'passwd': method.get('passwd'),
        'passwd1': method.get('passwd1'),
        'passwd2': method.get('passwd2'),
    })
    return result

def update_profile_from_site_helper(shopper, params: dict):
    """Вспомогательная функция для обновления профиля
       :param params: параметры для обновления профиля
       :param shopper: пользователь из сессии
       :return: list(errors) or Shopper instance
    """
    errors = []
    keys = (
        'name',
        'first_name',
        'last_name',
        'middle_name',
        'email',
        'phone',
        'address',
    )
    shopper_id = None
    if not shopper:
        errors.append('Пользователь не найден')
    elif isinstance(shopper, dict):
        shopper_id = shopper.get('id')
    elif isinstance(shopper, Shopper):
        shopper_id = shopper.id
    if not shopper_id:
        errors.append('Пользователь не найден')
        return errors
    user = Shopper.objects.filter(pk=shopper_id, is_active=True).first()
    if not user:
        errors.append('Пользователь не найден')
        return errors
    # Подтвержден телефон?
    if user.phone_confirmed:
        if user.phone != params.get('phone'):
            user.phone_confirmed = False

    passwd = params.get('passwd')
    passwd1 = params.get('passwd1')
    passwd2 = params.get('passwd2')
    if passwd or passwd1 or passwd2:
        if passwd == user.passwd and passwd1 == passwd2:
            user.passwd = passwd1
        else:
            errors.append('Вы неправильно ввели пароли')
    if errors:
        return errors
    for key in keys:
        setattr(user, key, params.get(key))
    user.save()
    return user