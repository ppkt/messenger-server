__author__ = 'ppkt'
import json

class Message(object):
    def __init__(self):
        self.content = dict()

    def getCode(self):
        pass

    def getType(self):
        pass

    def getContent(self):
        pass

    def decode(self, message):
        pass

    def encode(self):
        pass

class Ping(Message):
    def __init__(self):
        super(Ping, self).__init__()
        pass

    def getCode(self):
        return 1

    def getType(self):
        return 'SERVICE'

    def getContent(self):
        return ''

    # Message does not have any content, skip decoding / encoding
    def encode(self):
        return json.dumps(self.getContent())

    def decode(self, message):
        pass


class ChatMessage(Message):
    def __init__(self, from_, to, send_timestamp, receive_timestamp):
        super(ChatMessage, self).__init__()
        self.content = {}
        self.content['from'] = from_
        self.content['to'] = to
        self.content['send_timestamp'] = send_timestamp
        self.content['receive_timestamp'] = receive_timestamp


    def getCode(self):
        return 10

    def getType(self):
        return 'CHAT'

    def getContent(self):
        return self.content

    def encode(self):
        return json.dumps(self.content)

    def decode(self, message):
        self.content = json.loads(message)