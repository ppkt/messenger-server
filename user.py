__author__ = 'ppkt'
from enum import Enum

class State(Enum):
    not_connected = 0
    connected = 1
    authorized = 2
    not_responding = 3

class User(object):
    def __init__(self, handler=None):
        self._handler = handler
        self._state = State.not_connected

    @property
    def handler(self):
        return self._handler

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
