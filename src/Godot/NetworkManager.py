import asyncio
import threading


class TCPInterface:

    HOST, PORT = "127.0.0.1", 4001

    def __init__(self):
        self.streamWriter : asyncio.StreamWriter
        self.streamReader : asyncio.StreamReader

        self.clientID : int
        self.clientName : str
        self.isClientConnected = False

        self.networkThread : threading.Thread
        self.isNetworkThreadRunning = False


    def startThread(self):
        self.networkThread.start()
        self.isNetworkThreadRunning = True

     
    def stop(self):
        if self.isNetworkThreadRunning:
            self.networkThread.join()
