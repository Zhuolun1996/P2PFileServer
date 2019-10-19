import os
import threading
import socketserver
import hashlib
import json
from MessageAssembler.ResponseAssembler import ResponseAssembler
from pathlib import Path


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv()
        response = self.processRequest(json.load(data))
        self.request.sendall(response)

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
            return server.createFileIndexResponse(fileName, fileMd5, peerId)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class Server:
    def __init__(self, id, name, host, port, isFileIndexServer=False):
        self.id = id
        self.name = name
        self.address = (host, port)
        self.isFileIndexServer = isFileIndexServer
        self.fileIndexTable = dict()
        self.peerFileTable = dict()
        self.fileMd5Table = dict()
        self.server = ThreadedTCPServer(self.address, ThreadedTCPRequestHandler)

    def startServer(self):
        with self.server:
            # Start a thread with the server -- that thread will then start one
            # more thread for each request
            server_thread = threading.Thread(target=self.server.serve_forever)
            # Exit the server thread when the main thread terminates
            # server_thread.daemon = True
            server_thread.start()
            print("Server loop running in thread:", server_thread.name)

    def shutdownServer(self):
        self.server.shutdown()

    def getServer(self):
        return self.server

    def getAddress(self):
        return self.server.server_address

    def getDirectoryPath(self):
        try:
            return Path('./' + self.id)
        except Exception:
            os.mkdir('./' + self.id)
            return Path('./' + self.id)

    def createFileIndexResponse(self, fileName):
        if self.isFileIndexServer:
            peerSet = self.fileIndexTable[fileName]
            fileMd5 = self.fileMd5Table[fileName]
            chunks = len(peerSet)
            return ResponseAssembler.assembleFileIndexResponse(fileName, fileMd5, chunks, peerSet)
        else:
            return ResponseAssembler.assembleErrorResponse('ResponseFileIndexError')

    def createDownloadResponse(self, fileName, index, chunks):
        try:
            with self.getDirectoryPath().joinpath(fileName).open('rb') as file:
                fileContent = file.read()
                remainder = len(fileContent) % chunks
                chunkSize = (len(fileContent) - remainder) / chunks
                startIndex = index * chunkSize
                if (startIndex + chunkSize) > len(fileContent):
                    endIndex = startIndex + chunkSize
                else:
                    endIndex = len(fileContent)
                returnContent = fileContent[startIndex:endIndex]
                return ResponseAssembler.assembleDownloadResponse(fileName, index, chunks, hashlib.md5(returnContent),
                                                                  returnContent)
        except Exception:
            return ResponseAssembler.assembleErrorResponse('ResponseDownloadError')

    def createUpdateFileIndexResponseResponse(self, fileName, fileMd5, peerId):
        self.fileIndexTable[fileName].add(peerId)
        self.peerFileTable[peerId].add(fileName)
        self.fileMd5Table[fileName] = fileMd5
