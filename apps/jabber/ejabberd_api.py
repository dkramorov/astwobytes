import logging
import requests

from django.conf import settings

logger = logging.getLogger()

class EjabberdApi:
    """Работа с апи ejabberd
       /jabber/vcard/?action=set_vcard&phone=89148959223&credentials=...&field=URL&value=8800.help
       /jabber/vcard/?action=get_vcard&phone=89148959223&credentials=...&field=URL
    """
    def __init__(self):
        conf = settings.FULL_SETTINGS_SET
        self.domain = conf.get('JABBER_DOMAIN')
        self.port = '5443'
        self.schema = 'https'
        self.host = '%s://%s:%s' % (self.schema, self.domain, self.port)
        self.session = requests.Session()
        self.session.auth = ('%s@%s' % (
            conf.get('JABBER_ADMIN_LOGIN'),
            self.domain), conf.get('JABBER_ADMIN_PASSWD'))

    def create_user(self, login: str, passwd: str):
        """https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#register
           Register a user
           Arguments:
               user :: string : Username
               host :: string : Local vhost served by ejabberd
               password :: string : Password
           Result:
               res :: string : Raw result string
           Tags: accounts
           Examples:
               POST /api/register
               {
                   "user": "bob",
                   "host": "example.com",
                   "password": "SomEPass44"
               }
               HTTP/1.1 200 OK
               "Success"
        """
        endpoint = '%s/api/register' % self.host
        params = {
            'user': login,
            'host': self.domain,
            'password': passwd,
        }
        logger.info('create_user, params %s' % params)
        return self.session.post(url=endpoint, json=params)

    def drop_user(self, login):
        """https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#unregister
           Unregister a user
           This deletes the authentication and all the data associated to the account (roster, vcard...).
           Arguments:
               user :: string : Username
               host :: string : Local vhost served by ejabberd
           Result:
               res :: string : Raw result string
           Tags: accounts
           Examples:
               POST /api/unregister
               {
                   "user": "bob",
                   "host": "example.com"
               }    
               HTTP/1.1 200 OK
               "Success"
        """
        endpoint = '%s/api/unregister' % self.host
        params = {
            'user': login,
            'host': self.domain,
        }
        logger.info('drop_user, params %s' % params)
        return self.session.post(url=endpoint, json=params)

    def get_vcard(self, login, vcard_field: str = None):
        """https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#get-vcard
           Get content from a vCard field
           Some vcard field names in get/set_vcard are:
               FN - Full Name
               NICKNAME - Nickname
               BDAY - Birthday
               TITLE - Work: Position
               ROLE - Work: Role
               For a full list of vCard fields check XEP-0054: vcard-temp at https://xmpp.org/extensions/xep-0054.html
           Arguments:
               user :: string : User name
               host :: string : Server name
               name :: string : Field name
           Result:
               content :: string : Field content
           Tags: vcard
           Module: mod_admin_extra
           Examples:
               POST /api/get_vcard
               {
                   "user": "user1",
                   "host": "myserver.com",
                   "name": "NICKNAME"
               }
               HTTP/1.1 200 OK
               {"content": "User 1"}
        """
        if not vcard_field:
            vcard_field = 'NICKNAME'
        endpoint = '%s/api/get_vcard' % self.host
        params = {
            'user': login,
            # Проверял по conference. домену: vcard - не работает
            'host': self.domain,
            'name': vcard_field,
        }
        logger.info('get_vcard, params %s' % params)
        return self.session.post(url=endpoint, json=params)


    def set_vcard(self, login, vcard_field: str, vcard_value: str):
        """https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#set-vcard
           Set content in a vCard field
           Some vcard field names in get/set_vcard are:
               FN - Full Name
               NICKNAME - Nickname
               BDAY - Birthday
               TITLE - Work: Position
               ROLE - Work: Role
           For a full list of vCard fields check XEP-0054: vcard-temp at https://xmpp.org/extensions/xep-0054.html
           Arguments:
               user :: string : User name
               host :: string : Server name
               name :: string : Field name
               content :: string : Value
           Result:
               res :: integer : Status code (0 on success, 1 otherwise)
           Tags: vcard
           Module: mod_admin_extra
           Examples:
               POST /api/set_vcard
               {
                   "user": "user1",
                   "host": "myserver.com",
                   "name": "URL",
                   "content": "www.example.com"
               }
               HTTP/1.1 200 OK
        """
        if not vcard_field or not vcard_value:
            return
        endpoint = '%s/api/set_vcard' % self.host
        params = {
            'user': login,
            'host': self.domain,
            'name': vcard_field,
            'content': vcard_value,
        }
        logger.info('set_vcard, params %s' % params)
        return self.session.post(url=endpoint, json=params)

    def get_private_storage(self, login, element: str, ns: str):
        """https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#private-get
           Get some information from a user private storage
           Arguments:
               user :: string : User name
               host :: string : Server name
               element :: string : Element name
               ns :: string : Namespace
           Result:
             res :: string
           Tags: private
           Module: mod_admin_extra
           Examples:
               POST /api/private_get
               {
                   "user": "user1",
                   "host": "myserver.com",
                   "element": "storage",
                   "ns": "storage:rosternotes"
               }
           HTTP/1.1 200 OK {"res": "aaaaa"}
        """
        endpoint = '%s/api/private_get' % self.host
        params = {
            'user': login,
            'host': self.domain,
            'element': element,
            'ns': ns,
        }
        logger.info('get_private_storage, params %s' % params)
        return self.session.post(url=endpoint, json=params)

    def set_private_storage(self, login, element: str, ns: str):
        """https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#private-set
           Set to the user private storage
           Arguments:
               user :: string : User name
               host :: string : Server name
               element :: string : XML storage element
           Result:
               res :: integer : Status code (0 on success, 1 otherwise)
           Tags: private
           Module: mod_admin_extra
           Examples:
               POST /api/private_set
               {
                  "user": "user1",
                  "host": "myserver.com",
                  "element": "<storage xmlns='storage:rosternotes'/>"
               }
           HTTP/1.1 200 OK
        """
        endpoint = '%s/api/private_set' % self.host
        params = {
            'user': login,
            'host': self.domain,
            'element': element,
        }
        logger.info('set_private_storage, params %s' % params)
        return self.session.post(url=endpoint, json=params)

    def get_room_affiliations(self, name: str, service: str):
        """https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#get-room-affiliation
           Get the list of affiliations of a MUC room
           Arguments:
               name :: string : Room name
               service :: string : MUC service
           Result:
               affiliations :: [{username::string, domain::string, affiliation::string, reason::string}] : The list of affiliations with username, domain, affiliation and reason
           Tags: muc_room
           Module: mod_muc_admin
           Examples:
               POST /api/get_room_affiliations
               {
                   "name": "room1",
                   "service": "muc.example.com"
               }
           HTTP/1.1 200 OK
           [{
               "username": "user1",
               "domain": "example.com",
               "affiliation": "member",
               "reason": "member"
           }]
        """
        endpoint = '%s/api/get_room_affiliations' % self.host
        params = {
            'name': name,
            'service': service,
        }
        logger.info('get_room_affiliations, params %s' % params)
        return self.session.post(url=endpoint, json=params)

    def get_room_occupants(self, name: str, service: str):
        """https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#get-room-occupants
           Get the list of occupants of a MUC room
           Arguments:
               name :: string : Room name
               service :: string : MUC service
           Result:
               occupants :: [{jid::string, nick::string, role::string}] : The list of occupants with JID, nick and affiliation
           Tags: muc_room
               Module: mod_muc_admin
           Examples:
           POST /api/get_room_occupants
           {
               "name": "room1",
               "service": "muc.example.com"
           }
           HTTP/1.1 200 OK
           [{
               "jid": "user1@example.com/psi",
               "nick": "User 1",
               "role": "owner"
           }]
        """
        endpoint = '%s/api/get_room_occupants' % self.host
        params = {
            'name': name,
            'service': service,
        }
        logger.info('get_room_occupants, params %s' % params)
        return self.session.post(url=endpoint, json=params)

    def set_room_affiliation(self, name: str, service: str, jid: str, affiliation: str = 'member'):
        """https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#set-room-affiliation
           Change an affiliation in a MUC room
           Arguments:
               name :: string : Room name
               service :: string : MUC service
               jid :: string : User JID
               affiliation :: string : Affiliation to set
           Result:
               res :: integer : Status code (0 on success, 1 otherwise)
           Tags: muc_room
           Module: mod_muc_admin
           Examples:
           POST /api/set_room_affiliation
           {
               "name": "room1",
               "service": "muc.example.com",
               "jid": "user2@example.com",
               "affiliation": "member"
           }
           HTTP/1.1 200 OK
        """
        endpoint = '%s/api/set_room_affiliation' % self.host
        params = {
            'name': name,
            'service': service,
            'jid': jid,
            'affiliation': affiliation,
        }
        logger.info('set_room_affiliation, params %s' % params)
        return self.session.post(url=endpoint, json=params)

    def get_room_options(self, name: str, service: str):
        """https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#get-room-options
           Get options from a MUC room
           Arguments:
               name :: string : Room name
               service :: string : MUC service
           Result:
               options :: [{name::string, value::string}] : List of room options tuples with name and value
           Tags: muc_room
           Module: mod_muc_admin
           Examples:
           POST /api/get_room_options
           {
               "name": "room1",
               "service": "muc.example.com"
           }
           HTTP/1.1 200 OK
           [{
               "name": "members_only",
               "value": "true"
           }]
        """
        endpoint = '%s/api/get_room_options' % self.host
        params = {
            'name': name,
            'service': service,
        }
        logger.info('get_room_options, params %s' % params)
        return self.session.post(url=endpoint, json=params)

    def drop_muc(self, name: str, service: str):
        """https://docs.ejabberd.im/developer/ejabberd-api/admin-api/#destroy-room
           Destroy a MUC room
           Arguments:
               name :: string : Room name
               service :: string : MUC service
           Result:
               res :: integer : Status code (0 on success, 1 otherwise)
           Tags: muc_room
           Module: mod_muc_admin
           Examples:
           POST /api/destroy_room
           {
               "name": "room1",
               "service": "muc.example.com"
           }
           HTTP/1.1 200 OK
        """
        endpoint = '%s/api/destroy_room' % self.host
        params = {
            'name': name,
            'service': service,
        }
        logger.info('drop_muc, params %s' % params)
        return self.session.post(url=endpoint, json=params)


ejabberd_manager = EjabberdApi()

