import statistics
import copy
class testData:
    def __init__(self,messageSentData, messageReceivedData, bytesSentData, bytesReceivedData, avgResponseTimeData):
        self.messageSentData = copy.deepcopy(messageSentData)
        self.messageReceivedData = copy.deepcopy(messageReceivedData)
        self.bytesSentData = copy.deepcopy(bytesSentData)
        self.bytesReceivedData = copy.deepcopy(bytesReceivedData)
        self.avgResponseTimeData = copy.deepcopy(avgResponseTimeData)

    def getAvgMessageSentData(self):
        return statistics.mean(self.messageSentData)

    def getAvgMessageReceivedData(self):
        return statistics.mean(self.messageReceivedData)

    def getAvgBytesSentData(self):
        return statistics.mean(self.bytesReceivedData)

    def getAvgBytesReceivedData(self):
        return statistics.mean(self.bytesReceivedData)

    def getAvgAvgResponseTimeData(self):
        return statistics.mean(self.avgResponseTimeData)