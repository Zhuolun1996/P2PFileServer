import socket
from PeerManager.Peer import Peer
from DNSManager.DNSServer import DNSServer

if __name__ == "__main__":
    dnsServer = DNSServer()
    isCentralized = False
    peer0 = Peer(0, 'peer0', '127.0.0.1', 8000, dnsServer, False, isCentralized)
    peer1 = Peer(1, 'peer1', '127.0.0.1', 8001, dnsServer, False, isCentralized)
    peer2 = Peer(2, 'peer2', '127.0.0.1', 8002, dnsServer, False, isCentralized)
    peer3 = Peer(3, 'peer3', '127.0.0.1', 8003, dnsServer, False, isCentralized)

    peer0.startPeer()
    peer1.startPeer()
    peer2.startPeer()
    peer3.startPeer()
    try:
        # peer1.requestFileIndex('abc')
        print(peer0.fileMd5Table)
        peer3.downloadFile('abc')
    finally:
        peer0.printStatistic()
        peer1.printStatistic()
        peer2.printStatistic()
        peer3.printStatistic()
        peer0.shutdownPeer()
        peer1.shutdownPeer()
        peer2.shutdownPeer()
        peer3.shutdownPeer()

