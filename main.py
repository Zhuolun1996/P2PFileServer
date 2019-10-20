import socket
from PeerManager.Peer import Peer

if __name__ == "__main__":
    peer0 = Peer(0, 'peer0', '127.0.0.1', 8000, True)
    peer1 = Peer(1, 'peer1', '127.0.0.1', 8001)
    peer2 = Peer(2, 'peer2', '127.0.0.1', 8002)
    # peer3 = Peer(3, 'peer3', '127.0.0.1', 8003)

    peer0.startPeer()
    peer1.startPeer()
    peer2.startPeer()
    # peer3.startPeer()
    try:
        peer1.requestFileIndex('abc')
        peer2.downloadFile('abc')
    finally:
        peer0.shutdownPeer()
        peer1.shutdownPeer()
        peer2.shutdownPeer()
        # peer3.shutdownPeer()

