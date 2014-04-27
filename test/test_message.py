import unittest
import message
import datetime

__author__ = 'ppkt'

class TestChatMessage(unittest.TestCase):
    def setUp(self):
        self.send_timestamp = datetime.datetime.utcnow() - datetime.timedelta(seconds=5)
        self.recv_timestamp = datetime.datetime.utcnow()


    def test_encoding_decoding_normal_message(self):
        oldMessage = message.ChatMessage(to='sender',
                                         from_='receiver',
                                         send_timestamp=self.send_timestamp.strftime("%s"),
                                         receive_timestamp=self.recv_timestamp.strftime("%s"))
        text = oldMessage.encode()
        newMessage = message.ChatMessage()
        newMessage.decode(text)

        self.assertEqual(newMessage.getContent(), oldMessage.getContent())

    def test_encoding_decoding_empty_message(self):
        oldMessage = message.ChatMessage()
        text = oldMessage.encode()
        newMessage = message.ChatMessage()
        newMessage.decode(text)

        self.assertEqual(newMessage.getContent(), oldMessage.getContent())


class TestPingMessage(unittest.TestCase):
    def test_encoding_decoding_normal_ping(self):
        oldPing = message.Ping()
        text = oldPing.encode()
        newPing = message.Ping()
        newPing.decode(text)

        self.assertEqual(newPing.getContent(), oldPing.getContent())