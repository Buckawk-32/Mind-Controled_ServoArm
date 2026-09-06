import ClientUI
import DataInterface
import NetworkManager
from blessed import Terminal


class GodotClient:
    def __init__(self):
        self.ui = ClientUI.UI(Terminal())
        self.data = DataInterface.DataManager()
        self.network = NetworkManager.TCPInterface()

    def startClientThreads(self):
        self.ui.startThread()
        self.data.startThread()
        self.network.startThread()

    def 

    
    def stopClientThreads(self):
        try:
            self.ui.stop()
            self.data.stop()
            self.network.stop()
        except Exception as e:  # noqa: BLE001
            print(e)
        finally:
            print("Stopped Client Threads")


