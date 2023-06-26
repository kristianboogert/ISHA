from time import time

class Timer:
    def __init__(self):
        self.intervalMs = 0
        self.startTime = 0
        self.running = False
    def setIntervalMs(self, intervalMs):
        self.intervalMs = intervalMs
    def start(self):
        self.startTime = time()
        self.running = True
    def stop(self):
        self.running = False
    def isRunning(self):
        return self.running
    def hasElapsed(self):
        timeDiff = time()*1000-self.startTime*1000
        if timeDiff > self.intervalMs and self.running:
            self.running = False
            return True
        return False