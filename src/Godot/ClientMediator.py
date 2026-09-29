import threading
import time

import ClientUI
import NetworkManager
from blessed import Terminal

# /home/buckawk32/Nethika/CODE/OfficalProjects/Mind-Controled_ServoArm/src/gen/python/proto/self/client/v1/message_pb2.py
from gen.python.proto.self.client.v1.message_pb2 import PacketEnvelope


class GodotClient:
    def __init__(self):
        self.ui = ClientUI.UI(Terminal())
        self.network = NetworkManager.TCPInterface()

        self.masterThread : threading.Thread
        self.isMasterThreadRunning = False

        self.incomingPacketQueue = []
        self.isIncomingPacketQueueChanged = False
        self.outgoingPacketQueue = []
        self.isOutgoingPacketQueueChanged = False


    def __del__(self):
        self.stopClientThreads()

    
    def __startMasterThread(self):
        if not self.isMasterThreadRunning:
            self.masterThread = threading.Thread(self.startClientThreads())
            self.isMasterThreadRunning = True

            print("Client Master Thread Running...")



    def startClientThreads(self):
        try:
            self.ui.startThread()
            self.network.startThread()

            while True:
                if self.ui.iscurPacketChanged:
                    print("Packet Uploaded...")
                    self.pushToOutgoingQueue(self.ui.curPacket)
        except Exception as e:  # noqa: BLE001
            print(e)
        finally:
            self.stopClientThreads()
    
    def stopClientThreads(self):
        try:
            self.ui.stop()
            self.network.stop()

        except Exception as e:  # noqa: BLE001
            print(e)
        finally:
            print("Stopped Client Threads")


    def pushToIncomingQueue(self, packet: PacketEnvelope):
        self.writeToLog(f"Pushed ({packet.client_id} + {packet.client_name})'s Packet to Incoming Queue.\n")
        self.incomingPacketQueue.append(packet)
        self.isIncomingPacketQueueChanged = True

    def pushToOutgoingQueue(self, packet: PacketEnvelope):
        self.writeToLog(f"Pushed ({packet.client_id} + {packet.client_name})'s Packet to Outgoing Queue.\n")
        self.outgoingPacketQueue.append(packet)
        self.isOutgoingPacketQueueChanged = True

    def popFromOutgoingQueue(self):
        packet = self.outgoingPacketQueue.pop(0)
        self.writeToLog(f"Pop ({packet.client_id} + {packet.client_name})'s Packet to Outgoing Queue.\n")
        self.isOutgoingPacketQueueChanged = True

        return packet

    def popFromIncomingQueue(self):
        packet = self.incomingPacketQueue.pop(0)
        self.writeToLog(f"Pop ({packet.client_id} + {packet.client_name})'s Packet to Incoming Queue.\n")
        self.isIncomingPacketQueueChanged = True 

        return packet

    def writeToLog(self, s: str):
        with open("logs/dataLogs/trafficLog.txt", "a+") as file:
            file.write(f"{time.ctime()}: {s}")




if __name__ == "__main__":
    testClient = GodotClient()
    testClient.startClientThreads()
