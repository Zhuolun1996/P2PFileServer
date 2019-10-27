import argparse
import time
from PeerManager.Peer import Peer
from DNSManager.DNSServer import DNSServer


# if __name__ == "__main__":
#     dnsServer = DNSServer()
#     isCentralized = False
#     peer0 = Peer(0, 'peer0', '127.0.0.1', 8000, dnsServer, False, isCentralized)
#     peer1 = Peer(1, 'peer1', '127.0.0.1', 8001, dnsServer, False, isCentralized)
#     peer2 = Peer(2, 'peer2', '127.0.0.1', 8002, dnsServer, False, isCentralized)
#     peer3 = Peer(3, 'peer3', '127.0.0.1', 8003, dnsServer, False, isCentralized)
#
#     peer0.startPeer()
#     peer1.startPeer()
#     peer2.startPeer()
#     peer3.startPeer()
#     try:
#         # peer1.requestFileIndex('abc')
#         print(peer0.fileMd5Table)
#         peer3.downloadFile('abc')
#     finally:
#         peer0.printStatistic()
#         peer1.printStatistic()
#         peer2.printStatistic()
#         peer3.printStatistic()
#         peer0.shutdownPeer()
#         peer1.shutdownPeer()
#         peer2.shutdownPeer()
#         peer3.shutdownPeer()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', '--peers', help='Number of Peers', type=int, required=True)
    parser.add_argument('-M', '--files', help='Number of Files', type=int, required=True)
    parser.add_argument('-N', '--requests', help='Number of Requests', type=int, required=True)
    parser.add_argument('-F', '--frequency', help='Request Frequency', type=float, required=True)
    parser.add_argument('-C', '--centralized', help='Centralized Network: T or F', type=str, required=True)

    args = parser.parse_args()
    print(args)
    PEERS = args.peers
    FILES = args.files
    REQUESTS = args.requests
    FREQUENCY = args.frequency
    CENTRALIZED = args.centralized == 'T'

    peerList = list()
    dnsServer = DNSServer()

    if (CENTRALIZED):
        indexServer = Peer(10000, 'indexServer', '127.0.0.1', 10000, dnsServer, True, CENTRALIZED)
        indexServer.startPeer(FILES)

    for i in range(0, PEERS):
        peerList.append(Peer(i, 'peer' + str(i), '127.0.0.1', 8000 + i, dnsServer, False, CENTRALIZED))

    for peer in peerList:
        peer.startPeer(FILES)

    testPeer = Peer(1000, 'testPeer', '127.0.0.1', 9000, dnsServer, False, CENTRALIZED)

    try:
        for i in range(REQUESTS):
            testPeer.downloadFile(i % FILES)
            time.sleep(FREQUENCY)
    finally:
        if (CENTRALIZED):
            dnsServer.indexServer.printStatistic()
        for peer in peerList:
            peer.printStatistic()
        for peer in peerList:
            peer.shutdownPeer()


if __name__ == "__main__":
    main()
