#!/usr/bin/env python

from twisted.internet import reactor
from twisted.application import internet

from twisted.internet.protocol import Protocol, Factory


class Echo(Protocol):
    # Wrapper for encoding
    @classmethod
    def _clientSend(cls, handler, content):
        if not content.endswith("\r\n"):
            content +=  "\r\n"
        handler.write(content)


    def __init__(self, factory):
        # Assign Factory and create TimerService (for heartbeats)
        self.factory = factory
        self.timer = internet.TimerService(10, self.heartbeat)

    # Send heartbeat
    def heartbeat(self):
        self._clientSend(self.transport, "Ping")

    def connectionMade(self):
        # Run heartbeat service
        self.timer.startService()

        # Announce new presence
        for client in self.factory.clients:
            self._clientSend(client, "New user")

        # Add user to roster
        self.factory.clients.append(self.transport)

        # Send greeting to user
        self._clientSend(self.transport, "Hi, currently there are %d clients" % (len(self.factory.clients)))

    def connectionLost(self, reason):
        # Remove user from roster and send announcement to other users
        self.factory.clients.remove(self.transport)
        for client in self.factory.clients:
            self._clientSend(client, "Client left server")

    # Send any received data to all clients
    def dataReceived(self, data):
        for client in self.factory.clients:
            if client != self.transport:
                self._clientSend(client, data)
            else:
                self._clientSend(self.transport, "*" + data)

class EchoFactory(Factory):
    def __init__(self):
        # Define list of users
        self.clients = []

    def buildProtocol(self, addr):
        # Handle new connection
        return Echo(self)


reactor.listenTCP(8008, EchoFactory())
reactor.run()
