import threading

from gen.python.self.client.v1.message_pb2 import Message, PacketEnvelope, Tag


class DataManager:
    def __init__(self):
        self.incomingPacketQueue = [[], False]
        self.outgoingPacketQueue = [[], False]

        self.dataThread : threading.Thread 
        self.isDataThreadRunning = False

    def startThread(self):
        self.dataThread = threading.Thread()        


    def pushToIncomingQueue(self, packet: PacketEnvelope):
        self.incomingPacketQueue[0].append(packet)  # ty: ignore[unresolved-attribute]
        self.incomingPacketQueue[1] = True

    def pushToOutgoingQueue(self, packet: PacketEnvelope):
        self.outgoingPacketQueue[0].append(packet)  # ty: ignore[unresolved-attribute]
        self.outgoingPacketQueue[1] = True

    def popFromOutgoingQueue(self):
        self.outgoingPacketQueue[1] = True
        return self.outgoingPacketQueue[0].pop(0)  # ty: ignore[unresolved-attribute]

    def popFromIncomingQueue(self):
        self.incomingPacketQueue[1] = True
        return self.incomingPacketQueue[0].pop(0)  # ty: ignore[unresolved-attribute]



    def stop(self):
        if self.isDataThreadRunning:
            self.dataThread.join()

    
