__author__ = 'ppkt'

class User(object):
    def __init__(self, handler=None):
        self._handler = handler
        self._authorized = False

    @property
    def handler(self):
        return self._handler

    @property
    def authorized(self):
        return self._authorized

    @authorized.setter
    def authorized(self, value):
        self._authorized = value
