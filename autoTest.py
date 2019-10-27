import numpy as np
import matplotlib.pyplot as plt
import time
import statistics
from PeerManager.Peer import Peer
from DNSManager.DNSServer import DNSServer
from Util.testData import testData


def autoTest(P, M, N, F, C, L, O):
    PEERS = P
    FILES = M
    REQUESTS = N
    FREQUENCY = F
    CENTRALIZED = C
    LENGTH = L
    OUTPUT = O

    peerList = list()
    dnsServer = DNSServer()

    messageSentData = list()
    messageReceivedData = list()
    bytesSentData = list()
    bytesReceivedData = list()
    avgResponseTimeData = list()

    try:
        # init centralized server if is centralized mode
        if (CENTRALIZED):
            indexServer = Peer(10000, 'indexServer', '127.0.0.1', 60000, dnsServer, True, CENTRALIZED, False, OUTPUT)
            indexServer.startPeer(FILES, LENGTH)

        # init peers
        for i in range(0, PEERS):
            peerList.append(
                Peer(i, 'peer' + str(i), '127.0.0.1', 50000 + i, dnsServer, False, CENTRALIZED, False, OUTPUT))

        for peer in peerList:
            peer.startPeer(FILES, LENGTH)

        # init test peer for download test
        testPeer = Peer(1000, 'testPeer', '127.0.0.1', 51000, dnsServer, False, CENTRALIZED, True, OUTPUT)
        testPeer.startPeer(FILES, LENGTH)

        # test download file
        for i in range(REQUESTS):
            testPeer.downloadFile(str(i % FILES))
            time.sleep(1 / FREQUENCY)

        if (CENTRALIZED):
            indexServer.recordStatistic(messageSentData, messageReceivedData, bytesSentData, bytesReceivedData,
                                        avgResponseTimeData)
        for peer in peerList:
            peer.recordStatistic(messageSentData, messageReceivedData, bytesSentData, bytesReceivedData,
                                 avgResponseTimeData)
        testPeer.recordStatistic(messageSentData, messageReceivedData, bytesSentData, bytesReceivedData,
                                 avgResponseTimeData)
        data = testData(messageSentData, messageReceivedData, bytesSentData, bytesReceivedData, avgResponseTimeData)
        return data

    except OSError:
        print('wait until OS release ports')

    finally:
        for peer in peerList:
            peer.shutdownPeer()
        if (CENTRALIZED):
            indexServer.shutdownPeer()
        testPeer.shutdownPeer()


def makePlot():
    O = 'false'
    C1 = 'T'
    C2 = 'F'
    P1 = 1
    M1 = 1
    N1 = 1
    F1 = 1
    L1 = 1

    # Ptest = 10
    data = autoTest(P1, M1, N1, F1, C1, L1, O)
    l1 = plt.plot(np.arange(1,11), data.messageSentData, 'r--', label='inner test')
    plt.legend()
