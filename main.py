from PeerManager.Peer import Peer

if __name__ == "__main__":
    peer0 = Peer(0, 'peer0', 'localhost', 8000, True)
    peer1 = Peer(1, 'peer1', 'localhost', 8001)
    peer2 = Peer(2, 'peer2', 'localhost', 8002)
    peer3 = Peer(3, 'peer3', 'localhost', 8003)

    peer0.startPeer()
    print('peer0 start')
    peer1.startPeer()
    print('peer1 start')
    peer2.startPeer()
    print('peer2 start')
    peer3.startPeer()
    print('peer3 start')
    peer0.client.requestFileIndex(peer0.address, 'abc')

    peer0.shutdownPeer()
    print('peer0 shutdown')
    peer1.shutdownPeer()
    print('peer1 shutdown')
    peer2.shutdownPeer()
    print('peer2 shutdown')
    peer3.shutdownPeer()
    print('peer3 shutdown')

