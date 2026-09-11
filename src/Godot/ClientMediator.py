import threading

import ClientUI
import DataInterface
import NetworkManager
from blessed import Terminal


class GodotClient:
    def __init__(self):
        self.ui = ClientUI.UI(Terminal())
        self.data = DataInterface.DataManager()
        self.network = NetworkManager.TCPInterface()

        self.masterThread : threading.Thread

    def __del__(self):
        self.stopClientThreads()

    def _startOwnThread(self):
        self.masterThread = threading.Thread(self.startClientThreads())
        self.masterThread.start()

    def startClientThreads(self):
        try:
            self.ui.startThread()
            self.network.startThread()

            while True:
                if self.ui.iscurPacketChanged:
                    self.data.pushToOutgoingQueue(self.ui.curPacket)
        except Exception as e:  # noqa: BLE001
            print(e)
        finally:
            self.stopClientThreads()
    
    def stopClientThreads(self):
        try:
            self.ui.stop()
            self.network.stop()

            self._stopMasterThread()
        except Exception as e:  # noqa: BLE001
            print(e)
        finally:
            print("Stopped Client Threads")

    def _stopMasterThread(self):
        if self.masterThread.is_alive():
            self.masterThread.join()


if __name__ == "__main__":
    testClient = GodotClient()
    testClient._startOwnThread()
