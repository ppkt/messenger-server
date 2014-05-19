#!/usr/bin/env python

from twisted.internet import reactor
from twisted.application import internet

from twisted.internet.protocol import Protocol, Factory
from twisted.python import log
import sys
from message import Message, decodeMessage, LoginMessage
from user import User
from database import Database
import message
from utils import switch

class Echo(Protocol):
    # Wrapper for encoding
    @classmethod
    def _clientSend(cls, handler, message):
        content = message.encode()
        log.msg("< %s\t%s" % (handler.getPeer(), message))
        if not content.endswith("\r\n"):
            content +=  "\r\n"
        handler.write(content)


    def __init__(self, factory):
        # Assign Factory and create TimerService (for heartbeats)
        self.factory = factory
        self.timer = internet.TimerService(10, self.heartbeat)

    # Send heartbeat
    def heartbeat(self):
        self._clientSend(self.transport, message.Ping())

    def connectionMade(self):
        self.user = User(self.transport)

        log.msg("New connection")
        log.msg(self.user.handler.getPeer())

        # Run heartbeat service
        self.timer.startService()

        # Announce new presence
        for client in self.factory.clients:
            self._clientSend(client.handler, "New user")

        # Add user to roster
        self.factory.clients.append(self.user)

        # Send greeting to user
        #self._clientSend(self.user.handler, "Hi, currently there are %d clients" % (len(self.factory.clients)))

    def connectionLost(self, reason):
        log.msg("Connection lost")
        self.timer.stopService()
        log.msg(self.user.handler.getPeer())

        # Remove user from roster and send announcement to other users
        self.factory.clients.remove(self.user)
        for client in self.factory.clients:
            self._clientSend(client.handler, "Client left server")

    # Send any received data to all clients
    def dataReceived(self, data):
        log.msg("> %s\t%s" % (self.user.handler.getPeer(), data.strip()))
        message = decodeMessage(data)

        self.dispatchMessage(message)

    def dispatchMessage(self, message):

        for case in switch(message['type']):
            if case(20):
                # Check user credentials
                authorized = False
                if message['username'] == 'test1' and message['password'] == 'pass123':
                    authorized = True

                reply = LoginMessage()
                reply['username'] = message['username']
                reply['authorization'] = authorized
                self._clientSend(self.user.handler, reply)

                if not authorized:
                    # Bye Bye
                    self.transport.loseConnection()


class EchoFactory(Factory):
    def __init__(self):
        # Establish connection with DB
        self.db = Database()
        self.db.connect()

        # Define list of users
        self.clients = []

    def buildProtocol(self, addr):
        # Handle new connection
        return Echo(self)

log.startLogging(sys.stdout)
reactor.listenTCP(8008, EchoFactory())
reactor.run()
