# -*- coding: utf-8 -*-
import logging
import time
import uuid
import json
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.fortasks import search_process
from apps.main_functions.catcher import json_pretty_print
from apps.main_functions.string_parser import GenPasswd
from apps.jabber.ejabberd_api import EjabberdApi
from apps.jabber.models import Registrations

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--api_methods',
            action = 'store_true',
            dest = 'api_methods',
            default = False,
            help = 'Show api methods')
        parser.add_argument('--just_test',
            action = 'store_true',
            dest = 'just_test',
            default = False,
            help = 'Test create/drop user')
        parser.add_argument('--fill_all_vcards',
            action = 'store_true',
            dest = 'fill_all_vcards',
            default = False,
            help = 'Fill all vcards with name from registration')
        parser.add_argument('--get_vcard',
            action = 'store',
            type = str,
            dest = 'get_vcard',
            default = False,
            help = 'Get vcard for login')
        parser.add_argument('--set_vcard',
            action = 'store',
            type = str,
            dest = 'set_vcard',
            default = False,
            help = 'Set vcard for login with custom field and value')
        parser.add_argument('--get_private_storage',
            action = 'store',
            type = str,
            dest = 'get_private_storage',
            default = False,
            help = 'Get private storage for login')
        parser.add_argument('--get_room_affiliations',
            action = 'store',
            type = str,
            dest = 'get_room_affiliations',
            default = False,
            help = 'Get room affiliations and occupants')
        parser.add_argument('--set_room_affiliation',
            action = 'store',
            type = str,
            dest = 'set_room_affiliation',
            default = False,
            help = 'Set room affiliation for user')
        parser.add_argument('--get_room_options',
            action = 'store',
            type = str,
            dest = 'get_room_options',
            default = False,
            help = 'Get room options')
        parser.add_argument('--create_muc',
            action = 'store',
            type = str,
            dest = 'create_muc',
            default = False,
            help = 'Create MUC room with name')
        parser.add_argument('--drop_muc',
            action = 'store',
            type = str,
            dest = 'drop_muc',
            default = False,
            help = 'Drop MUC room by name')
        parser.add_argument('--create_user',
            action = 'store',
            type = str,
            dest = 'create_user',
            default = False,
            help = 'Create user with login and passwd')
        parser.add_argument('--drop_user',
            action = 'store',
            type = str,
            dest = 'drop_user',
            default = False,
            help = 'Drop user')
        parser.add_argument('--create_channel',
            action = 'store',
            type = str,
            dest = 'create_channel',
            default = False,
            help = 'Create channel with bot')
        parser.add_argument('--drop_channel',
            action = 'store',
            type = str,
            dest = 'drop_channel',
            default = False,
            help = 'Drop channel with bot')
        parser.add_argument('--send_message',
            action = 'store',
            type = str,
            dest = 'send_message',
            default = False,
            help = 'Send message')
        parser.add_argument('--send_group_message',
            action = 'store',
            type = str,
            dest = 'send_group_message',
            default = False,
            help = 'Send MUC message')

    def handle(self, *args, **options):
        """Тестирование апи ejabberd
        """
        is_running = search_process(q = ('jabber_api_test', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()

        conference_domain = 'conference.chat.masterme.ru'
        ejabberd_manager = EjabberdApi()

        if options.get('api_methods'):
            #from apps.main_functions.introspect import get_class_methods
            #api_methods = get_class_methods(ejabberd_manager)
            #for method in api_methods:
            #    if method[0].startswith('_'):
            #        continue
            #    print(method[0])
            for item in dir(ejabberd_manager):
                if item.startswith('_'):
                    continue
                #print(item, help(item))
                print('\n---\n', item, '\n', getattr(ejabberd_manager, item).__doc__)

        if options.get('get_vcard'):
            # Проверял по conference. домену: vcard - не работает
            login = options['get_vcard']
            field = 'DESC'
            check = ejabberd_manager.get_vcard(login, field).json()
            print(check)

        if options.get('set_vcard'):
            login = options['set_vcard']
            field = 'DESC'
            value = json.dumps({'test': 1})
            resp = ejabberd_manager.set_vcard(login, field, value)
            print('resp=>', resp.status_code, resp.text)

        if options.get('fill_all_vcards'):
            field = 'FN'
            all_regs = Registrations.objects.filter(is_active=True)
            for reg in all_regs:
                ejabberd_manager.set_vcard(reg.phone, field, reg.name)
                check = ejabberd_manager.get_vcard(reg.phone, field).json()
                print(reg.phone, reg.name, check)
                assert check['content'] == reg.name

        if options.get('just_test'):
            resp = ejabberd_manager.create_user(login='potestua', passwd='123')
            print('resp=>', resp.status_code, resp.text)
            print('---')
            resp = ejabberd_manager.drop_user(login='potestua')
            print('resp=>', resp.status_code, resp.text)

            jaba_domain = 'https://%s' % settings.JABBER_DOMAIN.rstrip('/')
            endpoint = '/jabber/get_jabber_users'
            url = '%s%s' % (jaba_domain, endpoint)
            headers = {
                'token': settings.FS_TOKEN,
            }
            r = requests.get(url, headers=headers)
            print(r.status_code, r.text)

        if options.get('get_private_storage'):
            resp = ejabberd_manager.get_private_storage(login=options['get_private_storage'], element='phonebook', ns='phonebook:hashed')
            print('resp=>', resp.status_code, resp.text)
            import base64
            import xml.etree.ElementTree as ET
            tree = ET.fromstring(resp.json()['res'])
            phonebook = tree[0]
            hashed = phonebook[0]
            #print(hashed.tag, hashed.text)
            contacts = json.loads(base64.b64decode(hashed.text))
            print(json_pretty_print(contacts))

        if options.get('get_room_affiliations'):
            room_name = options.get('get_room_affiliations')
            resp = ejabberd_manager.get_room_affiliations(name=room_name, service=conference_domain)
            print('resp=>', resp.status_code, resp.text)
            resp = ejabberd_manager.get_room_occupants(name=room_name, service=conference_domain)
            print('resp=>', resp.status_code, resp.text)

        if options.get('set_room_affiliation'):
            room_name = options.get('set_room_affiliation')
            jid = '89148959223@chat.masterme.ru'
            affiliation = 'member'

            resp = ejabberd_manager.set_room_affiliation(
                name=room_name,
                service=conference_domain,
                jid=jid,
                affiliation=affiliation,
            )
            print('resp=>', resp.status_code, resp.text)

        if options.get('get_room_options'):
            room_name = options.get('get_room_options')
            resp = ejabberd_manager.get_room_options(name=room_name, service=conference_domain)

        if options.get('drop_muc'):
            # company10808901659-86-23, vcard GROUP_company_1080_89016598623@chat.masterme.ru
            room_name = options.get('drop_muc')
            resp = ejabberd_manager.drop_muc(name=room_name, service=conference_domain)
            print(resp.text)

        if options.get('create_muc'):
            room_name = options.get('create_muc')
            resp = ejabberd_manager.create_muc(name=room_name, service=conference_domain)
            print(resp.text)

        if options.get('create_user'):
            login = options.get('create_user')
            passwd = GenPasswd(length=5)
            resp = ejabberd_manager.create_user(login=login, passwd=passwd)
            print(resp.text, 'passwd:', passwd)

        if options.get('drop_user'):
            login = options.get('drop_user')
            resp = ejabberd_manager.drop_user(login=login)
            print(resp.text)

        if options.get('drop_channel'):
            # 1) Удаляем группу (канал)
            room_name = options.get('drop_channel')
            resp = ejabberd_manager.drop_muc(name='channel_%s' % room_name, service=conference_domain)
            print(resp.text)
            # 2) Удаляем пользователя - бота для канала
            resp = ejabberd_manager.drop_user(login='bot_%s' % room_name)
            print(resp.text)

        if options.get('create_channel'):
            # 1) Создаем группу, это будет канал
            room_name = options.get('create_channel')
            channel_name = 'channel_%s' % room_name
            resp = ejabberd_manager.create_muc(name=channel_name, service=conference_domain)
            print(resp.text)
            # 2) Создаем пользователя - бота для канала
            bot_jid = 'bot_%s' % room_name
            passwd = GenPasswd(length=10)
            resp = ejabberd_manager.create_user(login=bot_jid, passwd=passwd)
            print(resp.text, 'passwd:', passwd)
            # 3) Делаем пользователя в группе главным
            resp = ejabberd_manager.set_room_affiliation(name=channel_name, service=conference_domain, jid=bot_jid, affiliation='owner')
            print(resp.text)

        if options.get('send_message'):
            """Отправка сообщений
            """
            msg = options['send_message']
            uid = str(uuid.uuid1())
            ts = str(time.time_ns() / 1000).split('.')[0]

            channel_name = 'channel_potestua'
            bot_jid = ejabberd_manager.to_jid(channel_name.replace('channel_', 'bot_'))
            channel_jid = '%s@%s' % (channel_name, conference_domain)

            resp = ejabberd_manager.get_room_occupants(name=channel_name, service=conference_domain)
            print(resp.text)

            resp = ejabberd_manager.get_room_affiliations(name=channel_name, service=conference_domain)
            print(resp.text)

            #resp = ejabberd_manager.send_message(
            #    from_login='89016598623',
            #    to_login='89148959223',
            #    subject='test',
            #    body=msg,
            #    mtype='chat',
            #)
            #resp = ejabberd_manager.send_message(
            #    from_login=bot_jid,
            #    to_login=channel_jid,
            #    subject='test',
            #    body=msg,
            #    mtype='groupchat',
            #)
            #print(resp.text)

            stanza = '''<message xmlns='jabber:client' to='89016598623@chat.masterme.ru' id='%s' type='chat'><body>%s</body><TIME xmlns='urn:xmpp:time'><ts>%s</ts></TIME><request xmlns='urn:xmpp:receipts'/></message>''' % (uid, msg, ts)
            #resp = ejabberd_manager.send_stanza(
            #    from_login='89148959223',
            #    to_login='89016598623',
            #    stanza=stanza,
            #)
            #print(resp.text)

            stanza = '''<message xmlns='jabber:client' to='%s@%s' id='%s' type='groupchat'><body>%s</body><TIME xmlns='urn:xmpp:time'><ts>%s</ts></TIME><request xmlns='urn:xmpp:receipts'/></message>''' % (channel_name, conference_domain, uid, msg, ts)
            #resp = ejabberd_manager.send_stanza(
            #    from_login=bot_jid,
            #    to_login=channel_jid,
            #    stanza=stanza,
            #)
            #print(resp.text)

        if options.get('send_group_message'):
            """Отправка в групповой чат сообщений
               pip install xmpppy==0.7.1
               Только occupants могут слать сообщения в MUC
            """
            import xmpp
            msg = options['send_group_message']
            uid = str(uuid.uuid1())
            ts = str(time.time_ns() / 1000).split('.')[0]

            channel_name = 'channel_dbupdates'
            bot_jid = ejabberd_manager.to_jid(channel_name.replace('channel_', 'bot_'))
            channel_jid = '%s@%s' % (channel_name, conference_domain)
            passwd = ''

            jid = xmpp.protocol.JID(bot_jid)
            cl = xmpp.Client(jid.getDomain(), debug=[])
            cl.connect()
            cl.auth(jid.getNode(), '75ij5tvx49')
            #cl.send(xmpp.protocol.Message('89148959223@chat.masterme.ru','test'))
            cl.send(xmpp.Presence(to="%s/%s" % (channel_jid, jid.getNode())))
            msgObj = xmpp.protocol.Message(channel_jid, msg)
            msgObj.setType('groupchat')
            msgObj.kids.append("<TIME xmlns='urn:xmpp:time'><ts>%s</ts></TIME>" % str(time.time_ns() / 1000000).split('.')[0])
            msgObj.setID(uid)
            cl.send(msgObj)
            time.sleep(1)
            cl.disconnect()


