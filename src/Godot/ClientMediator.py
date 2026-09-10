import ClientUI
import DataInterface
import NetworkManager
from blessed import Terminal

from gen.python.self.client.v1.message_pb2 import Message, PacketEnvelope, Tag

class GodotClient:
    def __init__(self):
        self.ui = ClientUI.UI(Terminal())
        self.data = DataInterface.DataManager()
        self.network = NetworkManager.TCPInterface()

    def startClientThreads(self):
        self.ui.startThread()
        self.data.startThread()
        self.network.startThread()

        while True:
            if self.ui.curPacket[1] == True:
                self.data.pushToOutgoingQueue(self.ui.curPacket[0])  # ty: ignore[invalid-argument-type]
                self.ui.curPacket[1] = False

    
    def stopClientThreads(self):
        try:
            self.ui.stop()
            self.data.stop()
            self.network.stop()
        except Exception as e:  # noqa: BLE001
            print(e)
        finally:
            print("Stopped Client Threads")


if __name__ == "__main__":
    testClient = GodotClient()
    testClient.startClientThreads()
