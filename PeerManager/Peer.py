from PeerManager.Client import Client
from PeerManager.Server import Server


class Peer:
    def __init__(self, id, name, host, port, isFileIndexServer=False):
        self.id = id
        self.name = name
        self.address = (host, port)
        self.server = Server(id, name, host, port, isFileIndexServer)
        self.client = Client(id, name)

    def startPeer(self):
        self.server.startServer()

    def shutdownPeer(self):
        self.server.shutdownServer()
