import os
import threading
import socketserver
import hashlib
import json
import traceback
import socket
import time
import shutil
from Util.SocketMessageManager import SocketMessageManager
from Util.statisticHelper import statisticHelper
from MessageAssembler.ResponseAssembler import ResponseAssembler
from pathlib import Path


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(SocketMessageManager.recvMessage(self.request, self.server.getP2PServer().messageSent,
                                                    self.server.getP2PServer().bytesSent), 'utf-8')
        startTime = time.time()
        print("Server {} Received: {}".format(self.server.getP2PServer().id, data))
        response = self.processRequest(json.loads(data), self.server.getP2PServer())
        self.request.settimeout(0.5)
        try:
            SocketMessageManager.sendMessage(self.request, bytes(response, 'utf-8'),
                                             self.server.getP2PServer().messageSent,
                                             self.server.getP2PServer().bytesSent)
            statisticHelper.computeAverageResponseTime(startTime, self.server.getP2PServer().avgResponseTime,
                                                       self.server.getP2PServer().messageSent)
        except socket.timeout:
            print("Peer {} timeout".format(self.request.address))
        print("Server {} send: {}".format(self.server.getP2PServer().id, response))

    def processRequest(self, request, server):
        requestHead = request['head']
        if requestHead == 'FileIndexRequest':
            fileName = request['fileName']
            return server.createFileIndexResponse(fileName)
        elif requestHead == 'DownloadRequest':
            fileName = request['fileName']
            index = request['index']
            chunks = request['chunks']
            return server.createDownloadResponse(fileName, index, chunks)
        elif requestHead == 'UpdateFileIndexRequest':
            fileName = request['fileName']
            fileMd5 = request['fileMd5']
            peerId = request['peerId']
            return server.createUpdateFileIndexResponse(fileName, fileMd5, peerId)
        elif requestHead == 'UpdatePeerAddressRequest':
            peerId = request['peerId']
            address = request['address']
            return server.createUpdatePeerAddressResponse(peerId, address)
        elif requestHead == 'JoinPeerNetworkRequest':
            peerId = request['peerId']
            address = request['address']
            return server.createJoinPeerNetworkResponse(peerId, address)
        elif requestHead == 'FindIndexServerRequest':
            return server.createFindIndexServerResponse()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def setup(self, server):
        self.P2PServer = server

    def getP2PServer(self):
        return self.P2PServer


class Server:
    def __init__(self, id, name, address, peerList, dnsServer, cachedIndexServer, messageSent, messageReceived,
                 bytesSent, bytesReceived, avgResponseTime, isFileIndexServer, isCentralized):
        self.id = id
        self.name = name
        self.address = address
        self.peerList = peerList
        self.dnsServer = dnsServer
        self.cachedIndexServer = cachedIndexServer
        self.isFileIndexServer = isFileIndexServer
        self.messageSent = messageSent
        self.messageReceived = messageReceived
        self.bytesSent = bytesSent
        self.bytesReceived = bytesReceived
        self.avgResponseTime = avgResponseTime
        self.isCentralized = isCentralized
        self.fileIndexTable = dict()
        self.peerFileTable = dict()
        self.fileMd5Table = dict()
        self.peerAddressTable = dict()
        self.server = ThreadedTCPServer(self.address, ThreadedTCPRequestHandler)
        self.server.setup(self)
        self.peerList = list()

    def startServer(self):
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
        print("Server " + str(self.id) + " loop running in thread:", server_thread.name)

    def shutdownServer(self):
        self.server.shutdown()
        print("Server" + str(self.id) + " shutdown")

    def getServer(self):
        return self.server

    def getAddress(self):
        return self.server.server_address

    def getDirectoryPath(self):
        return Path('./Files/' + str(self.id))

    def initFiles(self, num):
        self.cleanFileDirectory()
        for i in range(0, num):
            if not self.getDirectoryPath().exists():
                os.mkdir(self.getDirectoryPath())
            with self.getDirectoryPath().joinpath(str(i)).open('wb') as file:
                file.write(bytes(('Peer test File' + str(i)) * 100, 'utf-8'))

    def cleanFileDirectory(self):
        shutil.rmtree(self.getDirectoryPath())

    def createFileIndexResponse(self, fileName):
        if self.isFileIndexServer:
            peerSet = self.fileIndexTable[fileName]
            fileMd5 = self.fileMd5Table[fileName]
            chunks = len(peerSet)
            return ResponseAssembler.assembleFileIndexResponse(fileName, fileMd5, chunks, str(peerSet))
        else:
            return ResponseAssembler.assembleErrorResponse('ResponseFileIndexError')

    def createDownloadResponse(self, fileName, index, chunks):
        try:
            with self.getDirectoryPath().joinpath(fileName).open('rb') as file:
                fileContent = file.read()
                remainder = len(fileContent) % chunks
                chunkSize = int((len(fileContent) - remainder) / chunks)
                startIndex = index * chunkSize
                if (startIndex + chunkSize) < len(fileContent):
                    endIndex = startIndex + chunkSize
                else:
                    endIndex = len(fileContent)
                if index == chunks - 1:
                    endIndex = len(fileContent)
                print('request file chunk: ', index)
                print('file Length: ', len(fileContent))
                print('download piece: ', startIndex, endIndex)
                returnContent = fileContent[startIndex:endIndex]
                return ResponseAssembler.assembleDownloadResponse(fileName, index, chunks,
                                                                  hashlib.md5(returnContent).hexdigest(),
                                                                  str(returnContent, 'utf-8'))
        except Exception:
            traceback.print_exc()
            return ResponseAssembler.assembleErrorResponse('ResponseDownloadError')

    def createUpdateFileIndexResponse(self, fileName, fileMd5, peerId):
        try:
            try:
                self.fileIndexTable[fileName].add((peerId, str(self.peerAddressTable[peerId])))
            except KeyError:
                self.fileIndexTable[fileName] = set()
                self.fileIndexTable[fileName].add((peerId, str(self.peerAddressTable[peerId])))
            try:
                self.peerFileTable[peerId].add(fileName)
            except KeyError:
                self.peerFileTable[peerId] = set()
                self.peerFileTable[peerId].add(fileName)
            self.fileMd5Table[fileName] = fileMd5
            print(self.peerFileTable)
            print(self.peerAddressTable)
            print(self.fileIndexTable)
            print(self.fileMd5Table)
            return ResponseAssembler.assembleUpdateFileIndexResponse(fileName, fileMd5, True)
        except:
            return ResponseAssembler.assembleErrorResponse('updateFileIndexError')

    def createUpdatePeerAddressResponse(self, peerId, address):
        try:
            self.peerAddressTable[peerId] = address
            return ResponseAssembler.assembleUpdatePeerAddressResponse(peerId, address, True)
        except:
            return ResponseAssembler.assembleErrorResponse('updatePeerAddressError')

    def createJoinPeerNetworkResponse(self, peerId, address):
        try:
            self.peerList.append((peerId, address))
            return ResponseAssembler.assembleJoinPeerNetworkResponse(peerId, address, True)
        except:
            return ResponseAssembler.assembleErrorResponse('joinPeerNetworkError')

    def createFindIndexServerResponse(self):
        if self.cachedIndexServer[0] != 0:
            return ResponseAssembler.assembleFindIndexServerResponse(self.cachedIndexServer[0][0],
                                                                     self.cachedIndexServer[0][1], True)
        else:
            return ResponseAssembler.assembleFindIndexServerResponse(self.cachedIndexServer[0][0],
                                                                     self.cachedIndexServer[0][1], False)

    def quitIndexServer(self):
        self.isFileIndexServer = False
