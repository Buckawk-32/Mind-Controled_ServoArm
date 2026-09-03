import threading
from gen.python.proto.self.client.v1.message_pb2 import *


class DataManager:
    def __init__(self):
        self.incomingPacketQueue = [[], False]
        self.outgoingPacketQueue = [[], False]

        self.dataThread : threading.Thread 
        self.isDataThreadRunning = False


    def startThread(self):
        self.dataThread = threading.Thread()        


    def addToIncomingQueue(self, packet: PacketEnvelope):
        self.incomingPacketQueue[0].append(packet)  # ty: ignore[unresolved-attribute]
        self.incomingPacketQueue[1] = True

    def addToOutgoingQueue(self, packet: PacketEnvelope):
        self.outgoingPacketQueue[0].append(packet)  # ty: ignore[unresolved-attribute]
        self.outgoingPacketQueue[1] = True

