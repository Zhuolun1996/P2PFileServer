import time
class statisticHelper:
    @staticmethod
    def computeAverageResponseTime(startTime, averageTime, messageSentSum):
        currentTime = time.time_ns() // 1000000
        responseTime = currentTime - startTime
        averageTime[0] = (averageTime[0] * (messageSentSum[0] - 1) + responseTime) / messageSentSum[0]
        return