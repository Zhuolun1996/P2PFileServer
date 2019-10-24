from PeerManager.Client import Client
from PeerManager.Server import Server


class Peer(Server, Client):
    def __init__(self, id, name, host, port, dnsServer, isFileIndexServer=False, isCentralized=False):
        self.id = id
        self.name = name
        self.address = (host, port)
        self.peerList = list()
        self.cachedIndexServer = None
        self.dnsServer = dnsServer
        self.messageSent = [0]
        self.messageReceived = [0]
        self.bytesSent = [0]
        self.bytesReceived = [0]
        self.avgResponseTime = [0]
        self.isCentralized = isCentralized
        Server.__init__(self, id, name, self.address, self.peerList, dnsServer, self.cachedIndexServer,
                        self.messageSent, self.messageReceived, self.bytesSent, self.bytesReceived,
                        self.avgResponseTime, isFileIndexServer, isCentralized)
        Client.__init__(self, id, name, self.address, self.peerList, dnsServer, self.cachedIndexServer,
                        self.messageSent, self.messageReceived, self.bytesSent, self.bytesReceived,
                        self.avgResponseTime, isFileIndexServer, isCentralized)

    def startPeer(self):
        self.startServer()
        self.requestJoinNetwork(self.dnsServer)
        self.requestFindIndexServer()
        self.initPeerAddress()
        self.initFileIndex()

    def shutdownPeer(self):
        self.shutdownServer()

    def printStatistic(self):
        print('Peer {} Message Sent: {}'.format(self.id, self.messageSent[0]))
        print('Peer {} Message Received: {}'.format(self.id, self.messageSent[0]))
        print('Peer {} Bytes Sent: {}'.format(self.id, self.messageSent[0]))
        print('Peer {} Bytes Received: {}'.format(self.id, self.messageSent[0]))
        print('Peer {} Average Response Time: {}'.format(self.id, self.messageSent[0]))
