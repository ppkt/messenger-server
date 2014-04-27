__author__ = 'ppkt'

from pymongo import MongoClient

class Database(object):
    def __init__(self):
        pass

    def connect(self):
        self._client = MongoClient('212.91.26.160', 27017)
        self._db = self._client.mo13594_msg_srv
        self._db.authenticate('mo13594_msg_srv', 'eYW4lultswXZTsc3IS4h')

        self._users = self._db.users
        self._messages = self._messages

    @property
    def users(self):
        return self._users