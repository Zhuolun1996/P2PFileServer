from PeerManager.Client import Client
from PeerManager.Server import Server


class Peer(Server, Client):
    def __init__(self, id, name, host, port, dnsServer, isFileIndexServer=False):
        self.id = id
        self.name = name
        self.address = (host, port)
        self.peerList = list()
        self.cachedIndexServer = None
        self.dnsServer = dnsServer
        Server.__init__(self, id, name, self.address, self.peerList, dnsServer, self.cachedIndexServer, isFileIndexServer)
        Client.__init__(self, id, name, self.address, self.peerList, dnsServer, self.cachedIndexServer, isFileIndexServer)

    def startPeer(self):
        self.startServer()
        self.requestJoinNetwork(self.dnsServer)
        self.requestFindIndexServer()
        self.initPeerAddress()
        self.initFileIndex()

    def shutdownPeer(self):
        self.shutdownServer()
