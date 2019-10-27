from threading import Thread


class downloadThread(Thread):
    '''
    Download thread
    '''
    def __init__(self, client, fileName, index, chunks, targetPeerAddress, fileChunkResponses):
        Thread.__init__(self)
        self.client = client
        self.fileName = fileName
        self.index = index
        self.chunks = chunks
        self.targetPeerAddress = targetPeerAddress
        self.fileChunkResponses = fileChunkResponses

    def run(self):
        '''
        Send request to download a file chunk
        Add the chunk into download cache
        :return:
        '''
        self.fileChunkResponses.append(self.client.requestDownloadFile(self.fileName, self.index, self.chunks, self.targetPeerAddress))
