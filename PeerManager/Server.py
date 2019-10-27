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
    '''
    Handler to process TCP connection
    '''

    def handle(self):
        '''
        Process coming in TCP message and send response
        :return:
        '''
        data = str(SocketMessageManager.recvMessage(self.request, self.server.getP2PServer().messageSent,
                                                    self.server.getP2PServer().bytesSent), 'utf-8')
        startTime = time.time() * 1000
        if self.server.getP2PServer().output == 'debug':
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
        if self.server.getP2PServer().output == 'debug':
            print("Server {} send: {}".format(self.server.getP2PServer().id, response))

    def processRequest(self, request, server):
        '''
        Create response based on the request head
        :param request: request
        :param server: P2PServer
        :return:
        '''
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
    '''
    Server class
    '''

    def __init__(self, id, name, address, peerList, dnsServer, cachedIndexServer, messageSent, messageReceived,
                 bytesSent, bytesReceived, avgResponseTime, isFileIndexServer, isCentralized, isTest, output):
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
        self.isTest = isTest
        self.output = output
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
        '''
        Shutdown server
        stop listening
        release resources
        :return:
        '''
        self.server.shutdown()
        self.server.server_close()
        print("Server" + str(self.id) + " shutdown")

    def getServer(self):
        return self.server

    def getAddress(self):
        return self.server.server_address

    def getDirectoryPath(self):
        return Path('./Files/' + str(self.id))

    def initFiles(self, num, length):
        '''
        Create files for peers (for test only)
        :param num: number of files
        :param length: each file length
        :return:
        '''
        for i in range(0, num):
            if not self.getDirectoryPath().exists():
                os.mkdir(self.getDirectoryPath())
            with self.getDirectoryPath().joinpath(str(i)).open('wb') as file:
                file.write(bytes(('Peer test File' + str(i)) * length, 'utf-8'))

    def cleanFileDirectory(self):
        '''
        Clean file directory
        :return:
        '''
        try:
            shutil.rmtree(self.getDirectoryPath())
            print('clean directory success')
        except:
            print('clean directory fail')

    def createFileIndexResponse(self, fileName):
        '''
        Create response for file index request
        :param fileName: file name
        :return: file index response
        '''
        if self.isFileIndexServer:
            peerSet = self.fileIndexTable[fileName]
            fileMd5 = self.fileMd5Table[fileName]
            chunks = len(peerSet)
            return ResponseAssembler.assembleFileIndexResponse(fileName, fileMd5, chunks, str(peerSet))
        else:
            return ResponseAssembler.assembleErrorResponse('ResponseFileIndexError')

    def createDownloadResponse(self, fileName, index, chunks):
        '''
        Create response for download request
        :param fileName: file name
        :param index: index
        :param chunks: chunks
        :return: download response
        '''
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
                if self.output == 'clean' or self.output == 'debug':
                    print('====================================')
                    print(
                        'download from peer {} for file {} \nrequest file chunk: {} \nfile Length: {} \ndownload piece from: {} to {} \n====================================\n'.format(
                            self.id, fileName, index, len(fileContent), startIndex, endIndex))
                returnContent = fileContent[startIndex:endIndex]
                return ResponseAssembler.assembleDownloadResponse(fileName, index, chunks,
                                                                  hashlib.md5(returnContent).hexdigest(),
                                                                  str(returnContent, 'utf-8'))
        except Exception:
            traceback.print_exc()
            return ResponseAssembler.assembleErrorResponse('ResponseDownloadError')

    def createUpdateFileIndexResponse(self, fileName, fileMd5, peerId):
        '''
        Create response for update file index request
        :param fileName: file name
        :param fileMd5: file md5
        :param peerId: peer id
        :return: update file index response
        '''
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
            if self.output == 'debug':
                print('peer file table: ', self.peerFileTable)
                print('peer address table: ', self.peerAddressTable)
                print('file index table: ', self.fileIndexTable)
                print('file md5 table: ', self.fileMd5Table)
            return ResponseAssembler.assembleUpdateFileIndexResponse(fileName, fileMd5, True)
        except:
            return ResponseAssembler.assembleErrorResponse('updateFileIndexError')

    def createUpdatePeerAddressResponse(self, peerId, address):
        '''
        Create response for update peer address response
        :param peerId: peer id
        :param address: peer address
        :return: update peer address response
        '''
        try:
            self.peerAddressTable[peerId] = address
            return ResponseAssembler.assembleUpdatePeerAddressResponse(peerId, address, True)
        except:
            return ResponseAssembler.assembleErrorResponse('updatePeerAddressError')

    def createJoinPeerNetworkResponse(self, peerId, address):
        '''
        Create response for join peer network request
        :param peerId: peer id
        :param address: peer address
        :return: join peer network response
        '''
        try:
            self.peerList.append((peerId, address))
            return ResponseAssembler.assembleJoinPeerNetworkResponse(peerId, address, True)
        except:
            return ResponseAssembler.assembleErrorResponse('joinPeerNetworkError')

    def createFindIndexServerResponse(self):
        '''
        Create response for find index server request
        :return: find index server response
        '''
        if self.cachedIndexServer[0] != 0:
            return ResponseAssembler.assembleFindIndexServerResponse(self.cachedIndexServer[0][0],
                                                                     self.cachedIndexServer[0][1], True)
        else:
            return ResponseAssembler.assembleFindIndexServerResponse(self.cachedIndexServer[0][0],
                                                                     self.cachedIndexServer[0][1], False)

    def quitIndexServer(self):
        self.isFileIndexServer = False
