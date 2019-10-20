from PeerManager.Client import Client
from PeerManager.Server import Server


class Peer(Server, Client):
    def __init__(self, id, name, host, port, isFileIndexServer=False):
        self.id = id
        self.name = name
        self.address = (host, port)
        Server.__init__(self, id, name, host, port, isFileIndexServer)
        Client.__init__(self, id, name, host, port)

    def startPeer(self):
        self.startServer()
        self.initPeerAddress()
        self.initFileIndex()

    def shutdownPeer(self):
        self.shutdownServer()
