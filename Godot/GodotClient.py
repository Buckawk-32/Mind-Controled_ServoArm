from queue import Queue
import time

import asyncio
import threading

#  TODO: Use better naming convention to shorten this import line
from gen.python.proto.self.client.v1.message_pb2 import *  # noqa: F403



class GodotClient:

    #  TODO: example Host and Port -> Will intend to use real connection other than localhost
    HOST, PORT = "127.0.0.1", 4001

    def __init__(self):
        self.streamWriter : asyncio.StreamWriter
        self.streamReader : asyncio.StreamReader
    
        self.clientID : int = self.getID()
        self.clientName : str = self.getClientName()
        self.isClientConnected = False

        self.dataThread : threading.Thread 
        self.isDataThreadRunning = False

        self.networkThread : threading.Thread
        self.isNetworkThreadRunning = False

        self.msgQueue = Queue(10)

        self._lock = asyncio.Lock()





         



    def getID(self):
        usrID = int(input("What is your ID: "))
        return usrID

    def getClientName(self):
        name = str(input("What is your name: "))
        return name
