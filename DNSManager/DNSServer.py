class DNSServer:
    '''
    DNS server
    '''
    def __init__(self):
        self.peerList = list()
        self.indexServerAddress = tuple()
        self.indexServer = None

    def getFileIndexServerAddress(self):
        return self.indexServerAddress

    def updateIndexServerAddress(self, address):
        self.indexServerAddress = address

    def simulateARPAndPortScan(self):
        '''
        Simulate ARP and port scan
        :return: peers in the network
        '''
        return self.peerList

    def addPeerList(self, peerId, address):
        self.peerList.append((peerId, address))

    def getPeerList(self):
        return self.peerList