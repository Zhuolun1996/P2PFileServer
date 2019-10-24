import os
import socket
import hashlib
import json
from collections import Counter
from ast import literal_eval
from Util.SocketMessageManager import SocketMessageManager
from MessageAssembler.RequestAssembler import RequestAssembler
from DNSManager.DNSServer import DNSServer
from pathlib import Path


class Client:
    def __init__(self, id, name, address, peerList, dnsServer, cachedIndexServer, isFileIndexServer):
        self.id = id
        self.name = name
        self.address = address
        self.peerList = peerList
        self.dnsServer = dnsServer
        self.cachedIndexServer = cachedIndexServer
        self.isFileIndexServer = isFileIndexServer

    def sendMessage(self, address, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(address)
            SocketMessageManager.sendMessage(sock, bytes(message, 'utf-8'))
            print("Client {} send: {} to {}".format(self.id, message, str(address)))
            sock.settimeout(0.5)
            try:
                response = str(SocketMessageManager.recvMessage(sock), 'utf-8')
            except socket.timeout:
                print("Peer {} timeout".format(address))
            print("Client {} Received: {}".format(self.id, response))
            return response

    def getDirectoryPath(self):
        return Path('./Files/' + str(self.id))

    def initFileIndex(self):
        directory = self.getDirectoryPath()
        if not directory.exists():
            os.mkdir(directory)
        for file in directory.iterdir():
            self.requestUpdateFileIndex(file.name, hashlib.md5(file.read_bytes()).hexdigest())

    def initPeerAddress(self):
        return self.requestUpdatePeerAddress()

    def requestFileIndex(self, fileName):
        return self.sendMessage(DNSServer.getFileIndexServerAddress(),
                                RequestAssembler.assembleFileIndexRequest(fileName))

    def requestDownloadFile(self, fileName, index, chunks, targetPeerAddress):
        return self.sendMessage(targetPeerAddress, RequestAssembler.assembleDownloadRequest(fileName, index, chunks))

    def requestUpdateFileIndex(self, fileName, fileMd5):
        return self.sendMessage(DNSServer.getFileIndexServerAddress(),
                                RequestAssembler.assembleUpdateFileIndexRequest(fileName, fileMd5, self.id))

    def requestUpdatePeerAddress(self):
        return self.sendMessage(DNSServer.getFileIndexServerAddress(),
                                RequestAssembler.assembleUpdatePeerAddressRequest(self.id, self.address))

    def requestJoinNetwork(self, dnsServer):
        peerList = dnsServer.getPeerList()
        dnsServer.getPeerList().append((self.id, self.address))
        for peerInfo in peerList:
            if peerInfo[0] != self.id:
                self.requestJoinPeer(peerInfo)
                self.peerList.append(peerInfo)

    def requestJoinPeer(self, peerInfo):
        return self.sendMessage(peerInfo[1], RequestAssembler.assembleJoinPeerNetworkRequest(self.id, self.address))

    def requestFindIndexServer(self):
        responseList = list()
        for peerInfo in self.peerList:
            responseList.append(json.loads(self.requestIndexServerFromPeer(peerInfo[1])))
        indexServerCounter = Counter()
        for response in responseList:
            if response['head'] == 'FindIndexServerResponse' and response['result'] == 'True':
                indexServerCounter[response['address']] += 1
        if len(indexServerCounter) > 0:
            self.cachedIndexServer = tuple(literal_eval(sorted(indexServerCounter)[0]))
        if self.cachedIndexServer == 'None' or self.cachedIndexServer == None:
            self.cachedIndexServer = (self.id, self.address)
            self.isFileIndexServer = True
        print('Update Cached Index Server to {}'.format(self.cachedIndexServer))

    def requestIndexServerFromPeer(self, address):
        return self.sendMessage(address, RequestAssembler.assembleFindIndexServerRequest())

    def downloadFile(self, fileName):
        rawResponse = self.requestFileIndex(fileName)
        response = json.loads(rawResponse)
        if response['head'] == 'FileIndexResponse':
            self.processDownloadResponse(response)
        elif response['head'] == 'errorResponse' and response['error'] == 'ResponseFileIndexError':
            self.requestFindIndexServer()

    def processDownloadResponse(self, response):
        fileName = response['fileName']
        fileMd5 = response['fileMd5']
        chunks = response['chunks']
        peerSet = set(literal_eval(response['peerSet']))
        targetFilePath = self.getDirectoryPath().joinpath(response['fileName'])
        if targetFilePath.exists():
            with targetFilePath.open('rb') as file:
                verifyMd5 = hashlib.md5(file.read()).hexdigest()
                if verifyMd5 == fileMd5:
                    print('file Already Exists')
                    return True
                else:
                    print('start download')
                    self.downloadFromPeers(fileName, fileMd5, chunks, peerSet, targetFilePath)
        else:
            self.downloadFromPeers(fileName, fileMd5, chunks, peerSet, targetFilePath)

    def downloadFromPeers(self, fileName, fileMd5, chunks, peerSet, targetFilePath):
        print('start download')
        fileChunks = []
        for i in range(0, len(peerSet)):
            print('download {} piece'.format(i))
            response = json.loads(
                self.requestDownloadFile(fileName, i, chunks, tuple(literal_eval(peerSet.pop()[1]))))
            if response['head'] == 'errorResponse':
                raise Exception('downloadFileException')
            else:
                fileChunks.append(bytes(response['fileContent'], 'utf-8'))
        print(fileChunks)
        with targetFilePath.open('wb') as file:
            for item in fileChunks:
                file.write(item)
        with targetFilePath.open('rb') as file:
            verifyMd5 = hashlib.md5(file.read()).hexdigest()
            print(verifyMd5)
            print(fileMd5)
            if verifyMd5 == fileMd5:
                return True
            raise Exception('download File')
        return True
