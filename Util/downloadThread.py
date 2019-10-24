from threading import Thread


class downloadThread(Thread):
    def __init__(self, client, fileName, index, chunks, targetPeerAddress, fileChunkResponses):
        Thread.__init__(self)
        self.client = client
        self.fileName = fileName
        self.index = index
        self.chunks = chunks
        self.targetPeerAddress = targetPeerAddress
        self.fileChunkResponses = fileChunkResponses

    def run(self):
        self.fileChunkResponses.append(self.client.requestDownloadFile(self.fileName, self.index, self.chunks, self.targetPeerAddress))
