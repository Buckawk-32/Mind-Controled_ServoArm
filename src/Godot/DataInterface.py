# import threading
# import time
#
# # /home/buckawk32/Nethika/CODE/OfficalProjects/Mind-Controled_ServoArm/src/gen/python/proto/self/client/v1/message_pb2.py
# from gen.python.proto.self.client.v1.message_pb2 import PacketEnvelope
#
#
# class DataManager:
#     def __init__(self):
#         self.incomingPacketQueue = []
#         self.isIncomingPacketQueueChanged = False
#         self.outgoingPacketQueue = []
#         self.isOutgoingPacketQueueChanged = False
#
#         self.dataThread : threading.Thread 
#         self.isDataThreadRunning = False
#
#     def __del__(self):
#         if self.isDataThreadRunning:
#             self.stop()
#
#     def stop(self):
#         print("Stopping Data Interface...")
#         if self.isDataThreadRunning:
#             self.dataThread.join()
#
#     def startThread(self):
#         print("Data Interface Starting")
#         self.dataThread = threading.Thread()
#         self.dataThread.start()
#         self.isDataThreadRunning = True
#
#
#     def updateQueues(self):
#
#
#
#
#
#     def pushToIncomingQueue(self, packet: PacketEnvelope):
#         self.writeToLog(f"Pushed ({packet.client_id} + {packet.client_name})'s Packet to Incoming Queue.\n")
#         self.incomingPacketQueue.append(packet)
#         self.isIncomingPacketQueueChanged = True
#
#     def pushToOutgoingQueue(self, packet: PacketEnvelope):
#         self.writeToLog(f"Pushed ({packet.client_id} + {packet.client_name})'s Packet to Outgoing Queue.\n")
#         self.outgoingPacketQueue.append(packet)
#         self.isOutgoingPacketQueueChanged = True
#
#     def popFromOutgoingQueue(self):
#         packet = self.outgoingPacketQueue.pop(0)
#         self.writeToLog(f"Pop ({packet.client_id} + {packet.client_name})'s Packet to Outgoing Queue.\n")
#         self.isOutgoingPacketQueueChanged = True
#
#         return packet
#
#     def popFromIncomingQueue(self):
#         packet = self.incomingPacketQueue.pop(0)
#         self.writeToLog(f"Pop ({packet.client_id} + {packet.client_name})'s Packet to Incoming Queue.\n")
#         self.isIncomingPacketQueueChanged = True 
#
#         return packet
#
#     def writeToLog(self, s: str):
#         with open("logs/dataLogs/trafficLog.txt", "a+") as file:
#             file.write(f"{time.ctime()}: {s}")
#
#
#
