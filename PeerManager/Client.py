import os
import socket
import hashlib
from Util.SocketMessageManager import SocketMessageManager
from MessageAssembler.RequestAssembler import RequestAssembler
from DNSManager.DNSServer import DNSServer
from pathlib import Path


class Client:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def sendMessage(self, address, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(address)
            SocketMessageManager.sendMessage(sock, bytes(message, 'utf-8'))
            print("Client send: {} to {}".format(message, str(address)))
            # response = str(SocketMessageManager.recvMessage(sock), 'utf-8')
            # print("Client Received: {}".format(response))

    def getDirectoryPath(self):
        return Path('./Files/' + str(self.id))

    def initFileIndex(self):
        directory = self.getDirectoryPath()
        try:
            directory.exists()
        except Exception:
            os.mkdir(directory)
        for file in directory.iterdir():
            self.requestUpdateFileIndex(file.name, hashlib.md5(file.read_bytes()).hexdigest())

    def requestFileIndex(self, fileName):
        self.sendMessage(DNSServer.getFileIndexServerAddress(),
                         RequestAssembler.assembleFileIndexRequest(fileName))

    def requestDownloadFile(self, fileName, index, chunks, targetPeerAddress):
        self.sendMessage(targetPeerAddress, RequestAssembler.assembleDownloadRequest(fileName, index, chunks))

    def requestUpdateFileIndex(self, fileName, fileMd5):
        self.sendMessage(DNSServer.getFileIndexServerAddress(),
                         RequestAssembler.assembleUpdateFileIndexRequest(fileName, fileMd5, self.id))
