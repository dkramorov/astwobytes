# -*- coding: utf-8 -*-
import logging
import time
import json
import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from apps.main_functions.fortasks import search_process
from apps.main_functions.catcher import json_pretty_print
from apps.jabber.ejabberd_api import EjabberdApi
from apps.jabber.models import Registrations

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
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

    def handle(self, *args, **options):
        """Тестирование апи ejabberd
        """
        is_running = search_process(q = ('jabber_api_test', 'manage.py'))
        if is_running:
            logger.error('Already running %s' % (is_running, ))
            exit()

        conference_domain = 'conference.chat.masterme.ru'
        ejabberd_manager = EjabberdApi()

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
