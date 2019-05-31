import threading
import time

class AbstractTranslator:
    def __init__(self):
        self.translateThread = None
        self.translateQueue = []
        self.sleepTime = 0.5
        self.retryDelayTime = 5 #retry every 5 second
        self.retryTimes = 5 #retry 5 times

        self.threadFlag = True

    def translate(self, word): pass
        
    def setParams(self, sleepTime = 0.5, retryDelayTime = 5, retryTimes = 5):
        self.sleepTime = sleepTime
        self.retryDelayTime = retryDelayTime
        self.retryTimes = retryTimes

    def checkAndTranslate(self):
        retryTimes = self.retryTimes
        while self.threadFlag:
            if len(self.translateQueue) > 0:
                next = self.translateQueue.pop(0)
                result = self.translate(next[0])
                
                if result is 'error':
                    print('An Error Occured. Retry After {} seconds, {} times left.'.format(self.retryDelayTime, retryTimes))
                    time.sleep(self.retryDelayTime)
                    if retryTimes > 0:
                        self.translateQueue.append(next)
                        retryTimes -= 1
                        continue
                    else:
                        break

                next[1](result)
                time.sleep(self.sleepTime)
            else:
                break
        #clear list. incase error break
        self.translateQueue.clear()
        
    def startTranslator(self):
        self.translateThread = threading.Thread(target = self.checkAndTranslate)
        self.translateThread.setDaemon(True)
        self.threadFlag = True
        self.translateThread.start()

    def stopTranslate(self):
        self.threadFlag = False

        self.translateQueue.clear()

    def addTranslate(self, text, updateMethod):
        #print('called')
        self.translateQueue.append((text, updateMethod))

        if not self.translateThread or not self.translateThread.is_alive():
            self.startTranslator()