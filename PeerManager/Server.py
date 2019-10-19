import threading
import socketserver
import hashlib
import socket
import json
from Util.SocketMessageManager import SocketMessageManager
from MessageAssembler.ResponseAssembler import ResponseAssembler
from pathlib import Path


# class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
#     def handle(self):
#         data = str(SocketMessageManager.recvMessage(self.request), 'utf-8')
#         print("Server Received: {}".format(data))
#         response = self.processRequest(json.load(data), self.server)
#         SocketMessageManager.sendMessage(self.request, bytes(response, 'utf-8'))
#         print("Server send: {}".format(response))
#
#     def processRequest(self, request, server):
#         requestHead = request['head']
#         if requestHead == 'FileIndexRequest':
#             fileName = request['fileName']
#             return server.createFileIndexResponse(fileName)
#         elif requestHead == 'DownloadRequest':
#             fileName = request['fileName']
#             index = request['index']
#             chunks = request['chunks']
#             return server.createDownloadResponse(fileName, index, chunks)
#         elif requestHead == 'UpdateFileIndexRequest':
#             fileName = request['fileName']
#             fileMd5 = request['fileMd5']
#             peerId = request['peerId']
#             return server.createFileIndexResponse(fileName, fileMd5, peerId)
#
#
# class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
#     pass
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'utf-8')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'utf-8')
        self.request.sendall(response)


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
            server_thread.daemon = True
            server_thread.start()
            print("Server " + str(self.id) + " loop running in thread:", server_thread.name)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', 8000))

            # Send the data
            message = b'Hello, world'
            len_sent = s.send(message)

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
                return ResponseAssembler.assembleDownloadResponse(fileName, index, chunks,
                                                                  hashlib.md5(returnContent).hexdigest(),
                                                                  returnContent)
        except Exception:
            return ResponseAssembler.assembleErrorResponse('ResponseDownloadError')

    def createUpdateFileIndexResponseResponse(self, fileName, fileMd5, peerId):
        self.fileIndexTable[fileName].add(peerId)
        self.peerFileTable[peerId].add(fileName)
        self.fileMd5Table[fileName] = fileMd5
