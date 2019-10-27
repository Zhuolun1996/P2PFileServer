import numpy as np
import matplotlib.pyplot as plt
import time
import statistics
from PeerManager.Peer import Peer
from DNSManager.DNSServer import DNSServer
from Util.testData import testData


def autoTest(parameters):
    try:
        PEERS = parameters[0]
        FILES = parameters[1]
        REQUESTS = parameters[2]
        FREQUENCY = parameters[3]
        CENTRALIZED = parameters[4]
        LENGTH = parameters[5]
        OUTPUT = parameters[6]

        peerList = list()
        dnsServer = DNSServer()

        messageSentData = list()
        messageReceivedData = list()
        bytesSentData = list()
        bytesReceivedData = list()
        avgResponseTimeData = list()

        # init centralized server if is centralized mode
        if (CENTRALIZED):
            indexServer = Peer(10000, 'indexServer', '127.0.0.1', 60000, dnsServer, True, CENTRALIZED, False,
                               OUTPUT)
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


        for peer in peerList:
            peer.recordStatistic(messageSentData, messageReceivedData, bytesSentData, bytesReceivedData,
                                 avgResponseTimeData)
        if (CENTRALIZED):
            indexServer.recordStatistic(messageSentData, messageReceivedData, bytesSentData, bytesReceivedData,
                                        avgResponseTimeData)
        testPeer.recordStatistic(messageSentData, messageReceivedData, bytesSentData, bytesReceivedData,
                                 avgResponseTimeData)

        data = testData(messageSentData, messageReceivedData, bytesSentData, bytesReceivedData, avgResponseTimeData)

        makePlot(data.messageSentData, 'message sent' + str(parameters), CENTRALIZED)
        makePlot(data.messageReceivedData, 'message received' + str(parameters), CENTRALIZED)
        makePlot(data.bytesSentData, 'bytes sent' + str(parameters), CENTRALIZED)
        makePlot(data.bytesReceivedData, 'bytes received' + str(parameters), CENTRALIZED)
        makePlot(data.avgResponseTimeData, 'average time' + str(parameters), CENTRALIZED)

        print('avg message sent: ', data.getAvgMessageSentData())
        print('avg message recv: ', data.getAvgMessageReceivedData())
        print('avg bytes sent: ', data.getAvgBytesSentData())
        print('avg bytes recv: ', data.getAvgBytesReceivedData())
        print('avg response time: ', data.getAvgAvgResponseTimeData())


    except OSError:
        print('wait until OS release ports')

    finally:
        for peer in peerList:
            peer.shutdownPeer()
        if (CENTRALIZED):
            indexServer.shutdownPeer()
        testPeer.shutdownPeer()


def makePlot(plotData, name, isCentralized):
    plt.figure()
    plt.plot(np.arange(1, len(plotData)+1), plotData, label=name)
    plt.legend()
    plt.savefig(name + '.png')



parameters = [4, 2, 1, 10, 'T', 5, 'false']
autoTest(parameters)
