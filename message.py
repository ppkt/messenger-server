__author__ = 'ppkt'
import json
import abc
from twisted.python import log
from utils import switch

def decodeMessage(data):
    log.msg(repr(data))

    message = json.loads(data.strip())
    log.msg(message)
    received = None
    for case in switch(message['type']):
        if case(1):
            log.msg('Ping')
            received = Ping()
            break
        if case(2):
            log.msg('Pong')
            received = Pong()
            break
        if case(20):
            log.msg('Login')
            received = LoginMessage()
            break
    received.decode(data)
    return received



class Message(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._content = dict()

    def __getitem__(self, key):
        return self._content[key]

    def __setitem__(self, key, item):
        self._content[key] = item

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @abc.abstractmethod
    def decode(self, message):
        return

    @abc.abstractmethod
    def encode(self):
        return

class Ping(Message):
    def __init__(self):
        super(Ping, self).__init__()
        self._content['type'] = 1 # ping message

    def encode(self):
        return json.dumps(self.content)

    # Message does not have any content, skip decoding
    def decode(self, message):
        pass

    def __str__(self):
        return "Ping message: " + str(self._content)

class Pong(Message):
    def __init__(self):
        super(Pong, self).__init__()
        self._content['type'] = 2 # login message

    def encode(self):
        return json.dumps(self.content)

    def decode(self, message):
        self.content = json.loads(message)

class ChatMessage(Message):
    def __init__(self, from_=None, to='', text='', send_timestamp='', receive_timestamp=''):
        super(ChatMessage, self).__init__()
        self._content['type'] = 10 # chat message
        self._content['from'] = from_
        self._content['to'] = to
        self._content['text'] = text
        self._content['send_timestamp'] = send_timestamp
        self._content['receive_timestamp'] = receive_timestamp

    def encode(self):
        return json.dumps(self.content)

    def decode(self, message):
        self.content = json.loads(message)

class LoginMessage(Message):
    def __init__(self):
        super(LoginMessage, self).__init__()
        self._content['type'] = 20 # login message

    def encode(self):
        return json.dumps(self.content)

    def decode(self, message):
        self.content = json.loads(message)

