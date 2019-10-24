import socket
from PeerManager.Peer import Peer
from DNSManager.DNSServer import DNSServer

if __name__ == "__main__":
    dnsServer = DNSServer()
    peer0 = Peer(0, 'peer0', '127.0.0.1', 8000, dnsServer)
    peer1 = Peer(1, 'peer1', '127.0.0.1', 8001, dnsServer)
    peer2 = Peer(2, 'peer2', '127.0.0.1', 8002, dnsServer)
    # peer3 = Peer(3, 'peer3', '127.0.0.1', 8003)

    peer0.startPeer()
    peer1.startPeer()
    peer2.startPeer()
    # peer3.startPeer()
    try:
        print(peer0.cachedIndexServer, peer1.cachedIndexServer, peer2.cachedIndexServer)
        peer1.requestFileIndex('abc')
        peer2.downloadFile('abc')
    finally:
        peer0.shutdownPeer()
        peer1.shutdownPeer()
        peer2.shutdownPeer()
        # peer3.shutdownPeer()

