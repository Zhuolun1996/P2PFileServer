class DNSServer:
    def __init__(self):
        self.peerList = list()

    @staticmethod
    def getFileIndexServerAddress():
        ip = '127.0.0.1'
        port = 8000
        return ip, port

    def simulateARPAndPortScan(self):
        return self.peerList

    def addPeerList(self, peerId, address):
        self.peerList.append((peerId, address))

    def getPeerList(self):
        return self.peerList