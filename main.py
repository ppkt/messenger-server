#!/usr/bin/env python

from twisted.internet import reactor
from twisted.application import internet

from twisted.internet.protocol import Protocol, Factory


class Echo(Protocol):
    def __init__(self, factory):
        # Assign Factory and create TimerService (for heartbeats)
        self.factory = factory
        self.timer = internet.TimerService(10, self.hearbeat)

    # Send heartbeat
    def hearbeat(self):
        self.transport.write("Ping\r\n")

    def connectionMade(self):
        # Run heartbeat service
        self.timer.startService()

        # Announce new presence
        for client in self.factory.clients:
            client.write("New user!\r\n")

        # Add user to roster
        self.factory.clients.append(self.transport)

        # Send greeting to user
        self.transport.write("Hi, currently there are %d clients\r\n" % (len(self.factory.clients)))

    def connectionLost(self, reason):
        # Remove user from roster and send announcement to other users
        self.factory.clients.remove(self.transport)
        for client in self.factory.clients:
            client.write("Client left server\r\n")

    # Send any received data to all clients
    def dataReceived(self, data):
        for client in self.factory.clients:
            if client != self.transport:
                client.write(data)
            else:
                self.transport.write("*" + data)

class EchoFactory(Factory):
    def __init__(self):
        # Define list of users
        self.clients = []

    def buildProtocol(self, addr):
        # Handle new connection
        return Echo(self)


reactor.listenTCP(8008, EchoFactory())
reactor.run()
