__author__ = 'ppkt'
import json
import abc

class Message(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._content = dict()

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


class ChatMessage(Message):
    def __init__(self, from_ = None, to = '', send_timestamp = '', receive_timestamp = ''):
        super(ChatMessage, self).__init__()
        self._content['type'] = 10 # chat message
        self._content['from'] = from_
        self._content['to'] = to
        self._content['send_timestamp'] = send_timestamp
        self._content['receive_timestamp'] = receive_timestamp

    def encode(self):
        return json.dumps(self.content)

    def decode(self, message):
        self.content = json.loads(message)
