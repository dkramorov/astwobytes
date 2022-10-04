import logging
import requests

from django.conf import settings

logger = logging.getLogger()

class EjabberdApi:
    def __init__(self):
        conf = settings.FULL_SETTINGS_SET
        self.domain = conf['JABBER_DOMAIN']
        self.port = '5443'
        self.schema = 'https'
        self.host = '%s://%s:%s' % (self.schema, self.domain, self.port)
        self.session = requests.Session()
        self.session.auth = ('%s@%s' % (
            conf['JABBER_ADMIN_LOGIN'],
            self.domain), conf['JABBER_ADMIN_PASSWD'])

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