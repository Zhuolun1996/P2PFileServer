from PeerManager.Client import Client
from PeerManager.Server import Server


class Peer(Server, Client):
    '''
    Peer class
    Inherit Server and Client
    '''

    def __init__(self, id, name, host, port, dnsServer, isFileIndexServer=False, isCentralized=False, isTest=False,
                 output='clean'):
        self.id = id
        self.name = name
        self.address = (host, port)
        self.peerList = list()
        self.cachedIndexServer = [0]
        self.dnsServer = dnsServer
        self.messageSent = [0]
        self.messageReceived = [0]
        self.bytesSent = [0]
        self.bytesReceived = [0]
        self.avgResponseTime = [0]
        self.isFileIndexServer = isFileIndexServer
        self.isCentralized = isCentralized
        self.isTest = isTest
        self.output = output
        Server.__init__(self, self.id, self.name, self.address, self.peerList, self.dnsServer, self.cachedIndexServer,
                        self.messageSent, self.messageReceived, self.bytesSent, self.bytesReceived,
                        self.avgResponseTime, self.isFileIndexServer, self.isCentralized, self.isTest, self.output)
        Client.__init__(self, self.id, self.name, self.address, self.peerList, self.dnsServer, self.cachedIndexServer,
                        self.messageSent, self.messageReceived, self.bytesSent, self.bytesReceived,
                        self.avgResponseTime, self.isFileIndexServer, self.isCentralized, self.isTest, self.output)
        # Update index server in DNSServer if is centralized mode and self is index server
        if (self.isFileIndexServer and self.isCentralized):
            self.dnsServer.updateIndexServerAddress(self.address)
            self.dnsServer.indexServer = self

    def startPeer(self, M, L):
        '''
        Start Peer
        Start server, listening on the port
        Tell index server self's id address
        Clean file directory
        If is not index server or test peer, init files
        Tell index server self's files
        :param M: number of files
        :param L: file length
        :return:
        '''
        self.startServer()
        if (not self.isCentralized):
            self.requestJoinNetwork(self.dnsServer)
            self.requestFindIndexServer()
        self.initPeerAddress()
        self.cleanFileDirectory()
        if not (self.isCentralized and self.isFileIndexServer) and not self.isTest:
            self.initFiles(M, L)
        self.initFileIndex()

    def shutdownPeer(self):
        '''
        Shutdown peer
        Stop listening on the port
        :return:
        '''
        self.shutdownServer()

    def recordStatistic(self, messageSentData, messageReceivedData, bytesSentData, bytesReceivedData,
                        avgResponseTimeData):
        messageSentData.append(self.messageSent[0])
        messageReceivedData.append(self.messageReceived[0])
        bytesSentData.append(self.bytesSent[0])
        bytesReceivedData.append(self.bytesReceived[0])
        avgResponseTimeData.append(self.avgResponseTime[0])

    def printStatistic(self):
        print('Peer {} Message Sent: {}'.format(self.id, self.messageSent[0]))
        print('Peer {} Message Received: {}'.format(self.id, self.messageReceived[0]))
        print('Peer {} Bytes Sent: {}'.format(self.id, self.bytesSent[0]))
        print('Peer {} Bytes Received: {}'.format(self.id, self.bytesReceived[0]))
        print('Peer {} Average Response Time: {} milliseconds'.format(self.id, self.avgResponseTime[0]))
