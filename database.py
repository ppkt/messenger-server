__author__ = 'ppkt'

from pymongo import MongoClient
from twisted.python import log

import ConfigParser

class Database(object):
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        log.msg(config.sections())

    def connect(self):
        log.msg('Connecting to database')
        self._client = MongoClient('212.91.26.160', 27017)
        self._db = self._client.mo13594_msg_srv
        self._db.authenticate('mo13594_msg_srv', 'eYW4lultswXZTsc3IS4h')

        self._users = self._db.users
        self._messages = self._db.messages
        log.msg('Successful')

    @property
    def users(self):
        return self._users

    @property
    def messages(self):
        return self._messages