import time
import uuid
import xmpp
import logging

from django.conf import settings

logger = logging.getLogger()

class EjabberdBot:
    """Бот для ejabberd"""
    name: str = None
    passwd: str = None
    domain: str = None
    client = None

    def __init__(self, name: str, passwd: str):
        """Инициализация, необходимы логин и пароль
           name - логин, передавать без префикса, например, bot_dbupdates,
           принимаем просто dbupdates
        """
        conf = settings.FULL_SETTINGS_SET
        self.domain = conf.get('JABBER_DOMAIN')

        self.name = name or ''
        if self.name.startswith('bot_'):
            self.name = self.name.split('bot_')[-1]
        if self.name.startswith('channel_'):
            self.name = self.name.split('channel_')[-1]
        self.passwd = passwd

    def to_jid(self, login: str):
        """Дописать домен к логину, если нет собаки
           :param login: логин
        """
        return '%s@%s' % (login, self.domain) if '@' not in login else login

    def get_channel_name(self):
        """Название канала"""
        return 'channel_%s' % self.name

    def get_channel_jid(self):
        """JID канала"""
        return '%s@conference.%s' % (self.get_channel_name(), self.domain)

    def get_bot_name(self):
        """Имя бота"""
        return 'bot_%s' % self.name

    def auth(self):
        """Авторизация бота
        """
        bot_name = self.get_bot_name()
        channel_name = self.get_channel_name()
        bot_jid = self.to_jid(channel_name)
        channel_jid = self.get_channel_jid()

        #jid = xmpp.protocol.JID(bot_jid)
        #self.client = xmpp.Client(jid.getDomain(), debug=[])
        self.client = xmpp.Client(self.domain, debug=[])
        connect = self.client.connect()
        if not connect:
            logger.error('can not connect to server %s' % self.domain)
            return 400 # bad request
        result = self.client.auth(bot_name, self.passwd)
        if not result:
            logger.error('authorization error %s / %s' % (bot_name, self.passwd))
            return 401 # not authorized
        # Подписываемся на канал
        self.client.send(xmpp.Presence(to='%s/%s' % (channel_jid, bot_name)))
        return self.client.connected # tls+sasl (connect+result)

    def new_uuid(self):
        """Возвращает новый uuid"""
        return str(uuid.uuid1())

    def new_ts(self):
        """Возвращает время в миллисекундах от текущего
           в формате совместимого с ejabberd сообщением
        """
        return str(time.time_ns() / 1000000).split('.')[0]

    def send_channel_message(self, text: str):
        """Отправка сообщения в канал (группу)
           :param text: текст сообщения
        """
        if not self.client or not self.client.connected:
            assert False
        channel_jid = self.get_channel_jid()
        msg = xmpp.protocol.Message(channel_jid, text)
        msg.setType('groupchat')
        msg.kids.append("<TIME xmlns='urn:xmpp:time'><ts>%s</ts></TIME>" % self.new_ts())
        msg.setID(self.new_uuid())
        self.client.send(msg)
        time.sleep(1)

    def disconnect(self):
        """Отключение"""
        if not self.client or not self.client.connected:
            return
        self.client.disconnect()


def bot_muc_message(text: str):
    """Отправка сообщения от бота в muc
       :param text: текст, который надо отправить в канал
    """
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
