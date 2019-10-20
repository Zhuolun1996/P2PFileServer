import threading
import socketserver
import hashlib
import json
import traceback
from Util.SocketMessageManager import SocketMessageManager
from MessageAssembler.ResponseAssembler import ResponseAssembler
from pathlib import Path


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(SocketMessageManager.recvMessage(self.request), 'utf-8')
        print("Server {} Received: {}".format(self.server.getP2PServer().id, data))
        response = self.processRequest(json.loads(data), self.server.getP2PServer())
        SocketMessageManager.sendMessage(self.request, bytes(response, 'utf-8'))
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


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def setup(self, server):
        self.P2PServer = server

    def getP2PServer(self):
        return self.P2PServer


class Server:
    def __init__(self, id, name, host, port, isFileIndexServer=False):
        self.id = id
        self.name = name
        self.address = (host, port)
        self.isFileIndexServer = isFileIndexServer
        self.fileIndexTable = dict()
        self.peerFileTable = dict()
        self.fileMd5Table = dict()
        self.peerAddressTable = dict()
        self.server = ThreadedTCPServer(self.address, ThreadedTCPRequestHandler)
        self.server.setup(self)

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
                print('file Length: ', len(fileContent))
                print('download piece: ', startIndex, endIndex)
                returnContent = fileContent[startIndex:endIndex]
                return ResponseAssembler.assembleDownloadResponse(fileName, index, chunks,
                                                                  hashlib.md5(returnContent).hexdigest(),
                                                                  str(returnContent,'utf-8'))
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
