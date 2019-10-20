import struct


class SocketMessageManager:

    @staticmethod
    def sendMessage(sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    @staticmethod
    def recvMessage(sock):
        # Read message length and unpasendMessageck it into an integer
        rawMessageLength = SocketMessageManager.recvAll(sock, 4)
        if not rawMessageLength:
            return None
        messageLength = struct.unpack('>I', rawMessageLength)[0]
        # Read the message data
        return SocketMessageManager.recvAll(sock, messageLength)

    @staticmethod
    def recvAll(sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data
