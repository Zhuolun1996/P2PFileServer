import json


class RequestAssembler:
    @staticmethod
    def assembleFileIndexRequest(fileName):
        request = dict()
        request['head'] = 'FileIndexRequest'
        request['fileName'] = fileName
        return json.dumps(request)

    @staticmethod
    def assembleDownloadRequest(fileName, index, chunks):
        request = dict()
        request['head'] = 'DownloadRequest'
        request['fileName'] = fileName
        request['index'] = index
        request['chunks'] = chunks
        return json.dumps(request)

    @staticmethod
    def assembleUpdateFileIndexRequest(fileName, fileMd5, peerId):
        request = dict()
        request['head'] = 'UpdateFileIndexRequest'
        request['fileName'] = fileName
        request['fileMd5'] = fileMd5
        request['peerId'] = peerId
        return json.dumps(request)

    @staticmethod
    def assembleUpdatePeerAddressRequest(peerId, address):
        request = dict()
        request['head'] = 'UpdatePeerAddressRequest'
        request['peerId'] = peerId
        request['address'] = address
        return json.dumps(request)
