# -*- coding:utf-8 -*-
import json
import jwt
import datetime

from django.contrib.auth.models import User
from django.db.models import Q, Count, Max, F
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, resolve
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.main_functions.date_time import date_plus_days, str_to_date, date_to_timestamp, timestamp_to_date
from apps.ws.models import Messages, BcastMessages, Conversations, ConversationGroup

SHORT_MSG_LEN = 20
CUR_APP = 'ws'
chat_vars = {
    'singular_obj': 'Чат',
    'plural_obj': 'Чаты',
    'rp_singular_obj': 'чата',
    'rp_plural_obj': 'чатов',
    'template_prefix': 'ws_',
    'action_create': 'Создание',
    'action_edit': 'Редактирование',
    'action_drop': 'Удаление',
    'menu': 'ws',
    'submenu': 'chat',
    'show_urla': 'show_chat',
    'create_urla': 'create_chat',
    'edit_urla': 'edit_chat',
    'model': None,
}

@login_required
def show_chat(request, *args, **kwargs):
    """Вывод чата"""
    context = chat_vars.copy()
    token = jwt.encode({'token': request.user.username}, settings.WS_SECRET, algorithm='HS256')
    context['token'] = token.decode('utf-8')
    context['ws_server'] = settings.WS_SERVER
    template = '%schat.html' % (context['template_prefix'], )
    return render(request, template, context)

def get_user_messages(user1: int = 0, user2: int = 0, last_pk: int = 0, by: int = 50) -> dict:
    """Вспомогательная функция для получения беседы 2х пользователей"""
    result = {'messages': [], 'by': by, 'user_id': user1, 'last_pk': -1, 'with_user': user2}
    if last_pk == -1:
        return result
    ids_users = {}
    users = User.objects.filter(pk__in=[user1, user2]).values_list('id', 'username')
    if len(users) < 2:
        result['error'] = 'user not found'
        return result
    ids_users = {user[0]: user[1] for user in users}

    """
    query = BcastMessages.objects.filter(created__gt=start_date, created__lt=end_date)
    messages = query.order_by("-created")[page*by:page*by+by]
    for msg in messages:
        if not msg.created in result:
            result[msg.created] = []
        result[msg.created].append({
            'date': msg.created.strftime('%H:%M %d/%m'),
            'from_user': msg.from_user,
            'text': msg.text,
            'bcast_message': True,
        })
        ids_users[msg.from_user] = None
    """
    query = Messages.objects.filter(Q(to_user=user1, from_user=user2)|Q(from_user=user1, to_user=user2))
    if last_pk not in(0, -1):
        query = query.filter(pk__lt=last_pk)
    messages = query.order_by("-created")[:by]
    if messages:
        result['last_pk'] = min([msg.id for msg in messages])
        for msg in messages:
            msg_obj = {
                'sort': date_to_timestamp(msg.created),
                'date': msg.created.strftime('%d-%m-%Y'),
                'time': msg.created.strftime('%H:%M'),
                'from_user': ids_users[msg.from_user],
                'to_user': ids_users[msg.to_user],
                'text': msg.text,
            }
            msg_obj['updated'] = msg_obj['sort']
            result['messages'].append(msg_obj)
        result['messages'] = result['messages'][::-1]
    return result

def get_group_messages(user: int = 0, group_id: int = 0, last_pk: int = 0, by: int = 50) -> dict:
    """Вспомогательная функция для получения сообщений группы"""
    result = {'messages': [], 'by': by, 'group_id': group_id, 'last_pk': -1}
    if last_pk == -1:
        return result
    ids_users = {}
    group = ConversationGroup.objects.filter(pk=group_id).values_list('id', 'name').first()
    if not group:
        result['error'] = 'group not found'
        return result

    group_users = Conversations.objects.filter(group=group).values_list('user_id', flat=True)
    if not user in group_users:
        result['error'] = 'you are not member this group'
        return result
    group_users = list(group_users)

    query = Messages.objects.filter(group=group)
    # Помимо все пользователей группы,
    # надо еще и достать всех пользователей
    # от которых были сообщения в группе,
    # например, какой то пользователь писал,
    # а потом его похерили из группы -
    # сообщения должны быть всеравно выведены,
    # поэтому пользователей вытаскиваем поздже
    users_by_messages = query.exclude(from_user__in=group_users)
    users_by_messages = users_by_messages.values_list('from_user', flat=True)
    for user_id in users_by_messages:
        group_users.append(user_id)

    users = User.objects.filter(pk__in=group_users).values_list('id', 'username')
    ids_users = {user[0]: user[1] for user in users}

    if last_pk not in(0, -1):
        query = query.filter(pk__lt=last_pk)
    messages = query.order_by("-created")[:by]
    if messages:
        result['last_pk'] = min([msg.id for msg in messages])
        for msg in messages:
            msg_obj = {
                'is_group': True,
                'sort': date_to_timestamp(msg.created),
                'date': msg.created.strftime('%d-%m-%Y'),
                'time': msg.created.strftime('%H:%M'),
                'from_user': ids_users[msg.from_user],
                'to_user': msg.group_id,
                'group_id': msg.group_id,
                'text': msg.text,
            }
            msg_obj['updated'] = msg_obj['sort']
            result['messages'].append(msg_obj)
        result['is_group'] = True
        result['messages'] = result['messages'][::-1]
    return result

def get_user_conversations(user_id: int = 0) -> dict:
    """Вспомогательная функция для получения бесед пользователя
       Могут быть
       1) беседы тет-а-тет
       2) беседы группы
    """
    result = []
    # ----------------
    # Беседы тет-а-тет
    # ----------------
    conversations = Conversations.objects.filter(user_id=user_id, contact__isnull=False).values_list('contact', flat=True)
    # -------------------------------------------
    # Получение последних непрочитанных сообщений
    # по беседам тет-а-тет
    # -------------------------------------------
    messages = Messages.objects.filter(to_user=user_id, from_user__in=conversations, state__isnull=True).values('from_user', ).annotate(mcount=Count('from_user'), created=Max('created'))
    for item in conversations:
        conversation = {
            'to_user': user_id,
            'from_user': item,
            'new_messages': 0,
            'updated': 0,
        }
        for message in messages:
            if message['from_user'] == item:
                conversation['new_messages'] = message['mcount']
                t = date_to_timestamp(message['created'])
                conversation['updated'] = t
                conversation['date'] = message['created'].strftime('%d-%m-%Y')
                conversation['time'] = message['created'].strftime('%H:%M')
                conversation['created'] = message['created']

        result.append(conversation)
    # -------------------------------------------
    # Новые сообщения мы взяли, теперь надо взять
    # оставшиеся беседы и посмотреть есть что-то
    # что мы отправляли или нам отправляли и
    # записать последниее из них
    # -------------------------------------------
    not_new = [conversation for conversation in result if conversation['new_messages'] == 0]
    cond = Q()
    for item in not_new:
        cond.add(Q(from_user=item['from_user'], to_user=item['to_user'])|Q(to_user=item['from_user'], from_user=item['to_user']), Q.OR)
    # state не важен, т/к наши сообщения могли быть непрочитаны
    messages = Messages.objects.filter(cond).filter(group__isnull=True).values('from_user', 'to_user').annotate(Max('created'))

    for conversation in result:
        for message in messages:
            if (message['to_user'] == conversation['to_user'] and message['from_user'] == conversation['from_user']) or (message['to_user'] == conversation['from_user'] and message['from_user'] == conversation['to_user']):
                t = date_to_timestamp(message['created__max'])
                if t > conversation['updated']:
                    conversation['updated'] = t
                    conversation['date'] = message['created__max'].strftime('%d-%m-%Y')
                    conversation['time'] = message['created__max'].strftime('%H:%M')
                    conversation['created'] = message['created__max']
    # ---------------------------
    # Довыбрать тексты под беседы
    # ---------------------------
    cond = Q()
    for conversation in result:
        cond.add(Q(from_user=conversation['from_user'], to_user=conversation['to_user'], created=conversation['created']), Q.OR)
        cond.add(Q(to_user=conversation['from_user'], from_user=conversation['to_user'], created=conversation['created']), Q.OR)
    messages = Messages.objects.filter(cond).values('from_user', 'to_user', 'created', 'text')
    for conversation in result:
        for message in messages:
            if conversation['created'] == message['created']:
                if (conversation['from_user'] == message['from_user'] \
                and conversation['to_user'] == message['to_user']) \
                or (conversation['to_user'] == message['from_user'] \
                and conversation['from_user'] == message['to_user']):
                    t = date_to_timestamp(message['created'])
                    if t >= conversation['updated']:
                        conversation['updated'] = t
                        conversation['date'] = message['created'].strftime('%d-%m-%Y')
                        conversation['time'] = message['created'].strftime('%H:%M')
                        conversation['text'] = message['text']
                        if len(conversation['text']) > SHORT_MSG_LEN:
                            conversation['text'] = conversation['text'][:SHORT_MSG_LEN] + '...'
    # ----------------
    # Групповые беседы
    # ----------------
    conversations = Conversations.objects.select_related('group').filter(user_id=user_id, contact__isnull=True).values('group__name', 'created', 'group')
    ids_contacts = [conversation['group'] for conversation in conversations]
    contacts = Conversations.objects.filter(group__in=ids_contacts).values('user_id', 'group')
    # ------------------------------------
    # Группы надо выводить и без сообщений
    # ------------------------------------
    for item in conversations:
        conversation = {
            'is_group': True,
            'group_name': item['group__name'],
            'to_user': user_id,
            'from_user': item['group'],
            'new_messages': 0,
            'updated': date_to_timestamp(item['created']),
            'date': item['created'].strftime('%d-%m-%Y'),
            'time': item['created'].strftime('%H:%M'),
            'text': '...',
            'sender': 0,
            'contacts': [contact['user_id'] for contact in contacts
                if (contact['group'] == item['group'] and contact['user_id'] != user_id)],
        }
        result.append(conversation)
    # -------------------------------------------
    # Получение последних непрочитанных сообщений
    # по групповым беседам
    # -------------------------------------------
    messages = Messages.objects.filter(group__in=ids_contacts, state__isnull=True, group__isnull=False).values('from_user', 'created', 'group', 'text').annotate(mcount=Count('group'))
    for conversation in result:
        if not 'is_group' in conversation:
            continue
        for message in messages:
            if message['group'] == conversation['from_user']:
                conversation['new_messages'] = message['mcount']
                t = date_to_timestamp(message['created'])
                if t > conversation['updated']:
                    conversation['updated'] = t
                    conversation['date'] = message['created'].strftime('%d-%m-%Y')
                    conversation['time'] = message['created'].strftime('%H:%M')
                    conversation['text'] = message['text']
                    conversation['sender'] = message['from_user']
                    if len(conversation['text']) > SHORT_MSG_LEN:
                        conversation['text'] = conversation['text'][:SHORT_MSG_LEN] + '...'
        # Если этот пользователь отправлял последним,
        # то не надо помечать, что есть новые сообщения
        if conversation['sender'] == user_id:
            conversation['new_messages'] = 0


    # -----------------------------------------
    # Получение последних прочитанных сообщений
    # -----------------------------------------
    """
    messages = []
    old_conversations = [conversation['from_user'] for conversation in result if not 'text' in conversation]
    if old_conversations:
        messages_to = Messages.objects.filter(to_user=user_id, from_user__in=old_conversations).values('to_user', 'from_user').annotate(Max('created'))
        messages_from = Messages.objects.filter(from_user=user_id, to_user__in=old_conversations).values('from_user', 'to_user').annotate(Max('created'))
        old_messages = list(messages_to) + list(messages_from)
        if old_messages:
            cond = Q()
            for item in old_messages:
                cond.add(Q(to_user=item['to_user'], from_user=item['from_user'], created=item['created__max']), Q.OR)
            messages = Messages.objects.filter(cond)
    for item in result:
        for message in messages:
            if message.from_user == item['from_user'] and message.to_user == item['to_user']:
                t = date_to_timestamp(message.created)
                if t > conversation['updated']:
                    conversation['updated'] = t
                    conversation['date'] = message.created.strftime('%d-%m-%Y')
                    conversation['time'] = message.created.strftime('%H:%M')
                    conversation['text'] = message.text
                    if len(conversation['text']) > SHORT_MSG_LEN:
                        conversation['text'] = conversation['text'][:SHORT_MSG_LEN] + '...'
    """
    return sorted(result, key=lambda x:x['updated'], reverse=True)

def get_group_conversation(user_id: int = 0, group_id: int = 0) -> dict:
    """Вспомогательная функция для получения групповой беседы пользователя
    """
    result = {}

    group = ConversationGroup.objects.filter(pk=group_id).first()
    if not group:
        result['error'] = 'Группа не найдена'
        return result

    conversations = Conversations.objects.filter(group=group)
    # Проверяем, что пользователь в группе
    user_conversation = list(filter(lambda x: x.user_id == user_id, conversations))
    if not user_conversation:
        result['error'] = 'Вы не являетесь членом этой группы'
        return result

    user_conversation = user_conversation[0]
    contacts = [conversation.user_id for conversation in conversations if conversation.id != user_conversation.id]

    result = {
        'is_group': True,
        'group_name': group.name,
        'to_user': user_id,
        'from_user': group.id,
        'new_messages': 0,
        'updated': date_to_timestamp(user_conversation.created),
        'date': user_conversation.created.strftime('%d-%m-%Y'),
        'time': user_conversation.created.strftime('%H:%M'),
        'text': '...',
        'sender': 0,
        'contacts': contacts,
    }
    # -------------------------------------------
    # Получение последних непрочитанных сообщений
    # -------------------------------------------
    messages = Messages.objects.filter(group=group, state__isnull=True).values('from_user', 'created', 'group', 'text').annotate(mcount=Count('group'))
    for message in messages:
        result['new_messages'] = message['mcount']
        t = date_to_timestamp(message['created'])
        if t > result['updated']:
            result['updated'] = t
            result['date'] = message['created'].strftime('%d-%m-%Y')
            result['time'] = message['created'].strftime('%H:%M')
            result['text'] = message['text']
            result['sender'] = message['from_user']
            if len(result['text']) > SHORT_MSG_LEN:
                result['text'] = result['text'][:SHORT_MSG_LEN] + '...'
    # Если этот пользователь отправлял последним,
    # то не надо помечать, что есть новые сообщения
    if result['sender'] == user_id:
        result['new_messages'] = 0

    return result


@csrf_exempt
def messages_api(request):
    """Апи-методы для получения/сохранения сообщений от ws
       Апи-методы для получения/сохранения бесед от ws"""
    result = {}

    @csrf_protect
    def get_messages(request, user1: int = 0, user2: int = 0, last_pk: int = 0):
        """Получение сообщений пользователя"""
        return get_user_messages(user1=user1, user2=user2, last_pk=int(last_pk))

    @csrf_protect
    def get_gmessages(request, user: int = 0, group_id: int = 0, last_pk: int = 0):
        """Получение сообщений группы"""
        return get_group_messages(user=user, group_id=group_id, last_pk=int(last_pk))

    @csrf_protect
    def get_conversations(request, user_id: int = 0):
        """Получение бесед пользователя"""
        return get_user_conversations(user_id=user_id)

    @csrf_protect
    def get_group(request, user_id: int = 0, group_id: int = 0):
        """Получение группы"""
        return get_group_conversation(user_id=user_id, group_id=group_id)

    if request.method == "POST":
        body = json.loads(request.body)
        msg = body.get('msg', {})
        token = body.get('token', '')
        # --------------------------------------------
        # Отправка с клиента (не от сервера вебсокета)
        # В этом случае from получаем по токену
        # --------------------------------------------
        is_encoded = body.get('is_encoded', False)
        if is_encoded:
            try:
                token = jwt.decode(token, settings.WS_SECRET, algorithms=['HS256'])
                msg['from'] = token['token']
            except Exception as e:
                logger.info('[ERROR]: %s' % (e, ))
                token = None
        else:
            token = token == settings.WS_SECRET

        if msg and token:
            result['success'] = 1
        else:
            result['error'] = 'Error occured. Message and token are required'
        result['msg'] = msg

        action = msg.get('action')
        username = msg.get('from')
        from_user = User.objects.filter(username=username).first()
        # ---------------------------
        # Токен проверяем обязательно
        # ---------------------------
        if action and from_user:

            if action in ('bcast_msg', 'to_user', 'to_group'):
                updated = msg.get('updated')
                if updated:
                    updated = timestamp_to_date(updated)

            if action == 'bcast_msg':
                BcastMessages.objects.create(text=msg.get(action),
                                             from_user=from_user.id,
                                             created=updated)
            elif action == 'to_user':
                username = msg.get('to')
                to_user = User.objects.filter(username=username).first()
                if to_user:
                    Messages.objects.create(text=msg.get('msg'),
                                            from_user=from_user.id,
                                            to_user=to_user.id,
                                            created=updated)
                    # Если пользователя нет в Conversations,
                    # надо добавить
                    conversations = Conversations.objects.filter(Q(user_id=to_user.id, contact=from_user.id)|Q(user_id=from_user.id, contact=to_user.id)).values_list('user_id', 'contact')
                    if len(conversations) < 2:
                        conversations = list(conversations)
                        if not (to_user.id, from_user.id) in conversations:
                            Conversations.objects.create(user_id=to_user.id, contact=from_user.id)
                        if not (from_user.id, to_user.id) in conversations:
                            Conversations.objects.create(user_id=from_user.id, contact=to_user.id)
            elif action == 'to_group':
                group_id = msg.get('group_id')
                group = ConversationGroup.objects.filter(pk=group_id).first()
                if group:
                    Messages.objects.create(text=msg.get('msg'),
                                            from_user=from_user.id,
                                            group=group,
                                            created=updated)
            elif action == 'get_messages':
                to_user = User.objects.filter(username=msg.get('with_user')).values_list('id', flat=True).first()
                result = get_messages(request,
                                      user1=from_user.id,
                                      user2=to_user,
                                      last_pk=msg.get('last_pk'))
            elif action == 'get_group_messages':
                result = get_gmessages(request,
                                       user=from_user.id,
                                       group_id=msg.get('group', 0),
                                       last_pk=msg.get('last_pk'))
            elif action == 'get_conversations':
                result = get_conversations(request, user_id=from_user.id)
            # Отметить сообщения прочитанными
            elif action == 'mark_messages_read':
                is_group = msg.get('is_group')
                with_user = msg.get('with_user')
                updated = msg.get('updated')
                updated = int(updated) + 1
                updated = timestamp_to_date(updated)
                if is_group:
                    in_group = Conversations.objects.filter(user_id=from_user.id, group=with_user).first()
                    if in_group:
                        Messages.objects.filter(group=with_user, created__lt=updated).update(state=1)
                else:
                    with_user = User.objects.filter(username=with_user).values_list('id', flat=True).first()
                    if with_user:
                        Messages.objects.filter(from_user=with_user, to_user=from_user.id, created__lt=updated).update(state=1)
            # Создание новой беседы
            elif action == 'new_conversation':
                name = msg.get('name', '').strip()
                usernames = msg.get('users')
                users = User.objects.filter(username__in=usernames)
                if users and name:
                    new_conversation = ConversationGroup.objects.create(name=name, user_id=from_user.id)
                    # инициатор должен быть в группе
                    if not from_user.username in usernames:
                        users = list(users)
                        users.append(from_user)
                    for user in users:
                        Conversations.objects.create(user_id=user.id, group=new_conversation)
                    result = {
                        'first': True,
                        'is_group': True,
                        'group_name': new_conversation.name,
                        'to_user': from_user.id,
                        'from_user': new_conversation.id,
                        'new_messages': 0,
                        'updated': date_to_timestamp(new_conversation.created),
                        'date': new_conversation.created.strftime('%d-%m-%Y'),
                        'time': new_conversation.created.strftime('%H:%M'),
                        'text': '...',
                        'sender': 0,
                        'contacts': [user.id for user in users
                            if user.id != from_user.id],
                    }
            elif action == 'edit_conversation':
                name = msg.get('name', '').strip()
                usernames = msg.get('users')
                users = User.objects.filter(username__in=usernames)
                conversation_id = int(msg.get('conversation_id'))
                if users and name and conversation_id:
                    group = ConversationGroup.objects.filter(pk=conversation_id).first()
                    # инициатор должен быть админом
                    if from_user.id == group.user_id:
                        group.name = name
                        group.save()
                        users = list(users)
                        for user in users:
                            analog = Conversations.objects.filter(user_id=user.id, group=group).first()
                            if not analog:
                                Conversations.objects.create(user_id=user.id, group=group)
                        ids_users = [user.id for user in users]
                        ids_users.append(from_user.id)
                        Conversations.objects.filter(group=group).exclude(user_id__in=ids_users).delete()
                    result = {
                        'group_name': group.name,
                        'contacts': [user.id for user in users
                            if user.id != from_user.id],
                    }
            # Удаление чата пока только для бесед
            elif action == 'drop_chat':
                with_user = msg.get('with_user')
                group = ConversationGroup.objects.filter(id=with_user, user_id=from_user.id).first()
                if not group:
                    result['error'] = 'Вы не администратор этого чата'
                    return JsonResponse(result, safe=False)
                result['success'] = 'Чат удален'
                messages = Messages.objects.filter(group=group)
                messages.delete()
                conversations = Conversations.objects.filter(group=group)
                conversations.delete()
                group.delete()
            elif action == 'get_group':
                result = get_group(request, user_id=from_user.id, group_id=msg.get('group_id'))
    return JsonResponse(result, safe=False)


def fast_chat_new_messages(user_id: int, exclude_list: list) -> list:
    """Находим все непрочитанные сообщения пользователя и возвращаем их
       :param user_id: ИД пользователя
       :exclude_list: список сообщений, которые надо исключить"""
    excluded = [item for item in exclude_list.split(',') if item.isdigit()]
    # Сообщение может прилететь в группу
    user_groups = Conversations.objects.filter(user_id=user_id).values_list('group', flat=True)
    new_messages = Messages.objects.filter(Q(to_user=user_id)|Q(group__in=user_groups)).filter(state__isnull=True).exclude(pk__in=excluded).exclude(group__in=user_groups, from_user=user_id)
    users = User.objects.filter(pk__in=[msg.from_user for msg in new_messages]).values('id', 'username', 'first_name', 'last_name', 'email')
    ids_users = {
        user['id']: {
            'user': user,
            'messages': [],
        } for user in users
    }
    for msg in new_messages:
        new_msg = {
            'id': msg.id,
            'sort': date_to_timestamp(msg.created),
            'date': msg.created.strftime('%d-%m-%Y'),
            'time': msg.created.strftime('%H:%M'),
            'text': msg.text,
        }
        ids_users[msg.from_user]['messages'].append(new_msg)
    result = [{
        'user': user['user'],
        'messages': sorted(user['messages'], key=lambda x: x['sort']),
    } for user in ids_users.values() if user['messages']]
    return result

@login_required
@csrf_exempt
def fast_chat(request):
    """Аякс запросы по чату вне странички чата"""
    result = {}
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'get_new_messages':
            exclude_list = request.POST.get('exclude', '')
            result = fast_chat_new_messages(request.user.id, exclude_list)
        elif action == 'mark_messages_read':
            user_id = request.user.id
            ids_list = request.POST.get('ids', '')
            ids = [item for item in ids_list.split(',') if item.isdigit()]
            if ids:
                # Сообщение может прилететь в группу
                user_groups = Conversations.objects.filter(user_id=user_id).values_list('group', flat=True)
                Messages.objects.filter(pk__in=ids).filter(Q(to_user=user_id)|Q(group__in=user_groups)).update(state=1)
    return JsonResponse(result, safe=False)

