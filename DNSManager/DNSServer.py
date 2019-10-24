class DNSServer:
    def __init__(self):
        self.peerList = list()
        self.indexServer = tuple()

    def getFileIndexServerAddress(self):
        return self.indexServer

    def updateIndexServer(self, address):
        self.indexServer = address

    def simulateARPAndPortScan(self):
        return self.peerList

    def addPeerList(self, peerId, address):
        self.peerList.append((peerId, address))

    def getPeerList(self):
        return self.peerList