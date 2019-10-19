import os
import socket
import hashlib
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
            sock.sendall(bytes(message, 'utf-8'))
            response = str(sock.recv(1024), 'utf-8')
            print("Received: {}".format(response))

    def getDirectoryPath(self):
        try:
            return Path('./' + self.id)
        except Exception:
            os.mkdir('./' + self.id)
            return Path('./' + self.id)

    def initFileIndex(self):
        directory = self.getDirectoryPath()
        for file in os.listdir(directory):
            if file.is_file():
                self.requestUpdateFileIndex(file.name, hashlib.md5(file.read()))

    def requestFileIndex(self, fileName):
        self.sendMessage(DNSServer.getFileIndexServerAddress(),
                         RequestAssembler.assembleFileIndexRequest(fileName))

    def requestDownloadFile(self, fileName, index, chunks, targetPeerAddress):
        self.sendMessage(targetPeerAddress, RequestAssembler.assembleDownloadRequest(fileName, index, chunks))

    def requestUpdateFileIndex(self, fileName, fileMd5):
        self.sendMessage(DNSServer.getFileIndexServerAddress(),
                         RequestAssembler.assembleUpdateFileIndexRequest(fileName, fileMd5, self.id))
