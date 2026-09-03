import threading



class DataManager:
    def __init__(self):
        self.incomingPacketQueue = [[], False]
        self.outgoingPacketQueue = [[], False]

        self.dataThread : threading.Thread 
        self.isDataThreadRunning = False


    def startThread(self):


    def publishToUI(self):
        
