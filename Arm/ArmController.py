import serial
import threading
import time
import keyboard
from collections import deque

import serial.tools
import serial.tools.list_ports


# * https://forum.arduino.cc/t/two-ways-communication-between-python3-and-arduino/1219738
# * This is a forum post for a polished 2 way echo from python to arduino
# * Check this when you want to polish up the UI of this program or when you want to add threading to this program

class DataManager(object):

    def __init__(self, com, baudrate=int):
        self.baudrate = baudrate

        self.COM = com
        self.devID = None

        self.isS_ThreadRunning = False
        self.isL_ThreadRunning = False

        self.SenderThread = None
        self.ListenerThread = None

        self.srl = None

        # self.HeadsetDataTerm = manyterm.Terminal("Headset Data (Before Lerp)")
        # self.ArdunioInputTerm = manyterm.Terminal("Ardunio Input (After Lerp)")
        # self.ArdunioOutputTerm = manyterm.Terminal("Ardunio Output")

        if com == None:
            self.findDevice()

    def __del__(self):
        if self.isS_ThreadRunning == True or self.isL_ThreadRunning == True:
            self.stop()

    def stop(self):
        if self.isL_ThreadRunning == True:
            self.isL_ThreadRunning == False
            self.ListenerThread.join()

        if self.isS_ThreadRunning == True:
            self.isS_ThreadRunning == False
            self.SenderThread.join()

        if self.srl:
            self.srl.close()


    def findDevice(self):
        ports = serial.tools.list_ports.comports()
        choices = []
        print("")
        print('PORT\tDEVICE\t\t\tMANUFACTURER')
        for index, vaule in enumerate(sorted(ports)):
            if (vaule.hwid != 'n/a'):
                choices.append(index)
                print(index, '\t', vaule.name, '\t', vaule.manufacturer)

        choice = -1
        while choice not in choices:
            selectedPort = input("Select Which Port >> ")
            
            if selectedPort == "q":
                exit(0)

            if selectedPort.isnumeric and int(selectedPort) <= int(max(choices)):
                choice = int(selectedPort)

        print("Selecting >> ", ports[choice].name)
        print("")
        print("Device Port >> ", ports[choice].device)
        print("Device ID >> ", ports[choice].hwid)
        print("")

        self.COM = ports[choice].device
        self.devID = ports[choice].hwid

    def forcePort(self, com):
        self.COM = com


    def start(self, senderFunc, listenerFunc):
        if self.srl == None:
            print("Intizalizing Arudnio Serial Port...")
            self.srl = serial.Serial(port=self.COM, baudrate=self.baudrate, timeout=0.1)
            print("done")
        else:
            print("Opening Arudnio Serial port...")
            self.srl.open()
        
        self.SenderThread = threading.Thread(target=senderFunc)
        self.ListenerThread = threading.Thread(target=listenerFunc) 

        print("Arduino Threads Made...")
        print("")

        if senderFunc != None:
            self.isS_ThreadRunning = True
            self.SenderThread.start()
        
        if listenerFunc != None:
            self.isL_ThreadRunning = True
            self.ListenerThread.start()
        
        print("")



class ManualControl:

    def __init__(self, baudrate):
        self.baudrate = baudrate

        self.dataManager = DataManager(None, baudrate)
        self.dataManager.start(senderFunc=self.sendLabels, listenerFunc=None)

    def __del__(self):
        self.dataManager.__del__()

    
    def sendLabels(self):
        print("""
Use the arrow keys to control the Prosthetic
              
Right -> Move to Finger, Pinky to Thumb
Left -> Move to Finger, Thumb to Pinky
Up -> Move Finger up (0 degrees)
Down -> Move Finger down (180 degrees)""")
        
        while True:
            keyEvent = keyboard.read_event()
            if keyEvent.event_type == "down":
                self.dataManager.srl.write(bytes(f"{keyEvent.name}", "utf-8"))
            if keyEvent.name == "q":
                exit(1)

    def receiveFeedback(self):
        pass


class EEGControl_Mapped:

    def __init__(self, eegData, baudrate):
        self.eegData = eegData
        self.baudrate = baudrate
        self.dataManager = DataManager(None, baudrate)

        self.srl = self.dataManager.srl
        
        self.dataManager.start(senderFunc=self.sendData(), listenerFunc=None)

    def __del__(self):
        self.dataManager.__del__()


    def sendData(self):
        list = deque(maxlen=3)
        x = 0

        for i in range(len(list)):
            list.append(self.eegData)
            time.sleep(0.6)

        while True:

            list.append(self.eegData)

            print(list)

            x = sum(list, 0)
            x = x/len(list)
            print(f"Average of Data: {x}")
            print("")

            x = self.lerp(x, 0, 100, 0, 180)
            self.srl.write(bytes(f"{x}", "utf-8"))
            print(f"sending data >> {x}")
            x = 0
            time.sleep(0.6)


    def receiveData(self): # TODO: Add a listener function and chanage ListenerThread's target to that
        msgList = deque(maxlen=10)

        for i in range(10):
            msgList.append(0)

        print(msgList)

        while True:
            x = self.srl.readline().decode("utf-8")
            print(f"Arduino Feedback: {x}")
            msgList.append(x)
            time.sleep(0.6)
                

    def refreshData(self, data):
        print("")
        print(f"Raw Attention Data >> {data}")
        print("")
        self.eegData = data

    
    def lerp(self, data, in_min, in_max, out_min, out_max):
        return (data - in_min) * (out_max - out_min) / (in_max - in_min) + out_min



class TwinControl:
    
    def __init__(self, data, baudrate):
        self.positionalData = data
        self.baudrate = baudrate
        
        self.dataManager = DataManager("COM3", 115200)

        self.srl = self.dataManager.srl

        self.dataManager.start(senderFunc=self.grabPositions, listenerFunc=None)

    def __del__(self):
        self.dataManager.__del__()

    
    def grabPositions(self):
        self.sendConnectionID


    #! Testing only
    def sendConnectionID(self):
        self.srl.write(bytes(f"Con: {self.dataManager.devID}", "utf-8"))
        print("Sent Connection Identifier")
