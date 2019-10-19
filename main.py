from PeerManager.Peer import Peer

if __name__ == "__main__":
    peer0 = Peer(0, 'peer0', 'localhost', 8000, True)
    peer1 = Peer(1, 'peer1', 'localhost', 8001)
    # peer2 = Peer(2, 'peer2', 'localhost', 8002)
    # peer3 = Peer(3, 'peer3', 'localhost', 8003)

    peer0.startPeer()
    peer1.startPeer()
    # peer2.startPeer()
    # peer3.startPeer()
    peer1.client.requestFileIndex('abc')

    peer0.shutdownPeer()
    peer1.shutdownPeer()
    # peer2.shutdownPeer()
    # peer3.shutdownPeer()

