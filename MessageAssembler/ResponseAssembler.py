import json


class ResponseAssembler:
    @staticmethod
    def assembleFileIndexResponse(fileName, fileMd5, chunks, peerSet):
        response = dict()
        response['head'] = 'FileIndexResponse'
        response['fileName'] = fileName
        response['fileMd5'] = fileMd5
        response['chunks'] = chunks
        response['peerSet'] = peerSet
        return json.dumps(response)

    @staticmethod
    def assembleDownloadResponse(fileName, index, chunks, chunkMd5, fileContent):
        response = dict()
        response['head'] = 'DownloadResponse'
        response['fileName'] = fileName
        response['index'] = index
        response['chunks'] = chunks
        response['chunkMd5'] = chunkMd5
        response['fileContent'] = fileContent
        return json.dumps(response)

    @staticmethod
    def assembleUpdateFileIndexResponse(fileName, fileMd5, result):
        response = dict()
        response['head'] = 'UpdateFileIndexResponse'
        response['fileName'] = fileName
        response['fileMd5'] = fileMd5
        response['result'] = result
        return json.dumps(response)

    @staticmethod
    def assembleUpdatePeerAddressResponse(PeerId, address, result):
        response = dict()
        response['head'] = 'UpdatePeerAddressResponse'
        response['PeerId'] = PeerId
        response['address'] = address
        response['result'] = result
        return json.dumps(response)

    @staticmethod
    def assembleErrorResponse(errorBody):
        response = dict()
        response['head'] = 'errorResponse'
        response['error'] = errorBody
        return json.dumps(response)
