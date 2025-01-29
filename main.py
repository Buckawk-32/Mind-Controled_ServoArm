from Headset import Parser
from Arm import ArmManager
from collections import deque
import time

attentionList = deque(maxlen=1000)

headset = Parser.NeruoskyParser("COM6", 115200)

headset.start_serial()

time.sleep(10)

data_manager = ArmManager.DataManager(headset.attention, 115200)

data_manager.start()

while True:
    data_manager.refreshData(headset.attention)
    time.sleep(0.6)