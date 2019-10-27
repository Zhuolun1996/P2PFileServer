import argparse
import time
from PeerManager.Peer import Peer
from DNSManager.DNSServer import DNSServer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', '--peers', help='Number of Peers', type=int, required=True)
    parser.add_argument('-M', '--files', help='Number of Files', type=int, required=True)
    parser.add_argument('-N', '--requests', help='Number of Requests', type=int, required=True)
    parser.add_argument('-F', '--frequency', help='Request Frequency', type=float, required=True)
    parser.add_argument('-C', '--centralized', help='Centralized Network: T or F', type=str, required=True)
    parser.add_argument('-L', '--length', help='File Length', type=int, required=True)
    parser.add_argument('-O', '--output', help='enable message output: clean || debug || false', type=str,
                        required=True)
    args = parser.parse_args()

    PEERS = args.peers
    FILES = args.files
    REQUESTS = args.requests
    FREQUENCY = args.frequency
    CENTRALIZED = args.centralized == 'T'
    LENGTH = args.length
    OUTPUT = args.output

    peerList = list()
    dnsServer = DNSServer()
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
    except OSError:
        print('wait until OS release ports')

    finally:
        if (CENTRALIZED):
            indexServer.printStatistic()
        for peer in peerList:
            peer.printStatistic()
        for peer in peerList:
            peer.shutdownPeer()
        if (CENTRALIZED):
            indexServer.shutdownPeer()
        testPeer.shutdownPeer()


if __name__ == "__main__":
    main()
