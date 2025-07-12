from Headset import Parser
from Arm import ArmController
from collections import deque
import time

headset = Parser.NeruoskyParser("COM6", 115200)

headset.start_serial()

time.sleep(10)

eegControl = ArmController.EEGControl_Mapped(headset.attention, 115200)

while True:
    eegControl.refreshData(headset.attention)
    time.sleep(0.6)