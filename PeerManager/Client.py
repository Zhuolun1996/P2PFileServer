import os
import socket
import hashlib
import json
import time
from collections import Counter
from ast import literal_eval
from Util.SocketMessageManager import SocketMessageManager
from MessageAssembler.RequestAssembler import RequestAssembler
from Util.statisticHelper import statisticHelper
from pathlib import Path
from Util.downloadThread import downloadThread


class Client:
    def __init__(self, id, name, address, peerList, dnsServer, cachedIndexServer, messageSent, messageReceived,
                 bytesSent, bytesReceived, avgResponseTime, isFileIndexServer, isCentralized):
        self.id = id
        self.name = name
        self.address = address
        self.peerList = peerList
        self.dnsServer = dnsServer
        self.cachedIndexServer = cachedIndexServer
        self.messageSent = messageSent
        self.messageReceived = messageReceived
        self.bytesSent = bytesSent
        self.bytesReceived = bytesReceived
        self.avgResponseTime = avgResponseTime
        self.isFileIndexServer = isFileIndexServer
        self.isCentralized = isCentralized

    def sendMessage(self, address, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(address)
            try:
                SocketMessageManager.sendMessage(sock, bytes(message, 'utf-8'), self.messageSent, self.bytesSent)
                startTime = time.time()
            except:
                raise Exception('sent message fail')
            print("Client {} send: {} to {}".format(self.id, message, str(address)))
            sock.settimeout(0.5)
            try:
                response = str(SocketMessageManager.recvMessage(sock, self.messageReceived, self.bytesReceived),
                               'utf-8')
                statisticHelper.computeAverageResponseTime(startTime, self.avgResponseTime, self.messageSent)
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
        if (self.isCentralized):
            indexServerAddress = self.dnsServer.getFileIndexServerAddress()
        else:
            indexServerAddress = self.cachedIndexServer[0][1]
        return self.sendMessage(indexServerAddress,
                                RequestAssembler.assembleFileIndexRequest(fileName))

    def requestDownloadFile(self, fileName, index, chunks, targetPeerAddress):
        return self.sendMessage(targetPeerAddress, RequestAssembler.assembleDownloadRequest(fileName, index, chunks))

    def requestUpdateFileIndex(self, fileName, fileMd5):
        if (self.isCentralized):
            indexServerAddress = self.dnsServer.getFileIndexServerAddress()
        else:
            indexServerAddress = self.cachedIndexServer[0][1]
        return self.sendMessage(indexServerAddress,
                                RequestAssembler.assembleUpdateFileIndexRequest(fileName, fileMd5, self.id))

    def requestUpdatePeerAddress(self):
        if (self.isCentralized):
            indexServerAddress = self.dnsServer.getFileIndexServerAddress()
        else:
            indexServerAddress = self.cachedIndexServer[0][1]
        return self.sendMessage(indexServerAddress,
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
            if response['head'] == 'FindIndexServerResponse' and response['result'] == True:
                indexServerCounter[str((response['PeerId'],response['address']))] += 1
        if len(indexServerCounter) > 0:
            _cachedAddress = list(literal_eval(sorted(indexServerCounter)[0]))
            _cachedAddress[1] = tuple(_cachedAddress[1])
            _cachedAddress = tuple(_cachedAddress)
            self.cachedIndexServer[0] = _cachedAddress
        else:
            self.cachedIndexServer[0] = (self.id, self.address)
            self.isFileIndexServer = True
        print('Update Cached Index Server to {}'.format(self.cachedIndexServer[0]))

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
        cachedFileChunks = list()
        downloadThreadList = list()
        fileChunks = list()
        for i in range(0, len(peerSet)):
            downloadThreadList.append(
                downloadThread(self, fileName, i, chunks, tuple(literal_eval(peerSet.pop()[1])), cachedFileChunks))
            fileChunks.append(None)
        for _thread in downloadThreadList:
            print('Start download with {}'.format(_thread.name))
            _thread.start()
        for _thread in downloadThreadList:
            _thread.join()
        print(cachedFileChunks)
        for cachedChunk in cachedFileChunks:
            response = json.loads(cachedChunk)
            if response['head'] == 'errorResponse':
                raise Exception('downloadFileException')
            else:
                fileChunks[int(response['index'])] = bytes(response['fileContent'], 'utf-8')
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
