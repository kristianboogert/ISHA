from time import time

class Timer:
    def __init__(self):
        self.intervalMs = 0
        self.startTime = 0
    def setIntervalMs(self, intervalMs):
        self.intervalMs = intervalMs
    def start(self):
        self.startTime = time()
    def hasElapsed(self):
        timeDiff = time()*1000-self.startTime*1000
        print(timeDiff)
        print(self.intervalMs)
        return timeDiff > self.intervalMs